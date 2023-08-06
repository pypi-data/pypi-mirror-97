import os
import requests
import shutil
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from tempfile import gettempdir
from tqdm import tqdm
from math import pow
import re
import sys
from typing_extensions import Literal
from typing import Any, Dict, List, Optional
import uuid
import datetime
from google.resumable_media.requests import ResumableUpload
from google.resumable_media.common import InvalidResponse, DataCorruption

retry_strategy = Retry(
    total=4,
    backoff_factor=1,
    status_forcelist=[404, 429, 500, 502, 503, 504],
    method_whitelist=["HEAD", "GET", "PUT", "POST", "DELETE", "OPTIONS", "TRACE"],
)
retry_adapter = HTTPAdapter(max_retries=retry_strategy)
requests_retry = requests.Session()
requests_retry.mount("https://", retry_adapter)
requests_retry.mount("http://", retry_adapter)
tempdir_ttl_days = 1

MAX_FRAMES_PER_BATCH = 1000
MAX_CHUNK_SIZE = int(pow(2, 23))  # 8 MiB


def _upload_local_files(
    file_names: List[str],
    get_upload_path: str,
    headers: Dict[str, Any],
    upload_prefix: str,
    upload_suffix: str,
    delete_after_upload: bool = True,
) -> None:
    """This uploads a set of files with a reader, and then deletes it.

    Args:
        file_names (str): The local file_names (files to be uploaded)
        get_upload_path (str): The URL that generates upload URLs
        headers (Dict[str, Any]): Headers for the get_upload_path request
        upload_prefix (str): Prefix for the filepath (once uploaded)
        upload_suffix (str): Suffix for the filepath (once uploaded)
        delete_after_upload (bool): Whether to delete the file after upload

    Return:
        A list of download URLs for the uploaded files
    """
    xml_api_headers = {
        "x-goog-resumable": "start",
        "content-type": "application/octet-stream",
    }

    download_urls = []
    if len(file_names) == 0:
        return download_urls

    all_files_bytes = sum([os.path.getsize(file_name) for file_name in file_names])
    with tqdm(
        total=all_files_bytes,
        file=sys.stdout,
        unit="B",
        unit_scale=True,
        desc="Upload Progress",
    ) as pbar:
        for count, file_name in enumerate(file_names, start=1):
            upload_filename = (
                f"{upload_prefix}_batch_{str(count).zfill(6)}{upload_suffix}"
            )

            params = {
                "upload_filename": upload_filename,
                "resumable_upload": "true",
            }
            upload_url_resp = requests_retry.get(
                get_upload_path, headers=headers, params=params
            )
            raise_resp_exception_error(upload_url_resp)
            urls = upload_url_resp.json()
            put_url = urls["put_url"]
            download_url = urls["download_url"]
            download_urls.append(download_url)

            pbar.write(
                f"Uploading file {str(count).zfill(len(str(len(file_names))))}/{str(len(file_names))}"
            )

            upload = ResumableUpload(put_url, MAX_CHUNK_SIZE, headers=xml_api_headers)

            with open(file_name, "rb") as content_reader:
                upload.initiate(
                    requests_retry, content_reader, {}, "application/octet-stream"
                )
                last_upload_bytes = 0
                while not upload.finished:
                    try:
                        upload.transmit_next_chunk(requests_retry)
                    except (InvalidResponse, DataCorruption):
                        if upload.invalid:
                            upload.recover(requests_retry)
                        continue
                    except ConnectionError:
                        upload.recover(requests_retry)
                        continue
                    pbar.update(upload.bytes_uploaded - last_upload_bytes)
                    last_upload_bytes = upload.bytes_uploaded

            if delete_after_upload:
                os.remove(file_name)

    return download_urls


def _cleanup_temp_dirs(root_dir: str) -> None:
    sessions = os.listdir(root_dir)
    for session in sessions:
        session_dir = os.path.join(root_dir, session)
        lock_dir = os.path.join(session_dir, "lock")
        # clear session cache if no lockfile or past TTL
        if not os.path.exists(lock_dir):
            if os.path.isdir(session_dir):
                shutil.rmtree(session_dir)
            else:
                os.remove(session_dir)
        else:
            lockfiles = os.listdir(lock_dir)
            if len(lockfiles) == 0:
                shutil.rmtree(session_dir)
            else:
                date = os.path.splitext(lockfiles[0])[0]
                if int(date) < int(datetime.datetime.today().timestamp()):
                    shutil.rmtree(session_dir)


def _create_lock_file(temp_dir: str) -> None:
    """Creates lockfile at <TEMP_DIR>/lock/<EXPIRE_DATE>.lock"""
    lock_dir = os.path.join(temp_dir, "lock")
    os.makedirs(lock_dir)
    expire_date = datetime.datetime.today() + datetime.timedelta(days=tempdir_ttl_days)
    lock_file = os.path.join(lock_dir, str(int(expire_date.timestamp())) + ".lock")
    f = open(lock_file, "w")
    f.close()


def create_root_temp_directory() -> str:
    current_temp_directory = gettempdir()
    root_temp_path = os.path.join(
        current_temp_directory, "aquarium_learning_disk_cache"
    )
    os.makedirs(root_temp_path, exist_ok=True)
    _cleanup_temp_dirs(root_temp_path)

    return root_temp_path


ROOT_TEMP_FILE_PATH = create_root_temp_directory()


def create_temp_directory() -> str:
    temp_path = os.path.join(ROOT_TEMP_FILE_PATH, str(uuid.uuid4()))
    os.makedirs(temp_path)

    _create_lock_file(temp_path)

    return temp_path


def mark_temp_directory_complete(temp_dir):
    lock_dir = os.path.join(temp_dir, "lock")
    if os.path.exists(lock_dir):
        shutil.rmtree(lock_dir)


def _is_one_gb_available() -> bool:
    """Returns true if there is more than 1 GB available on the current filesystem"""
    return shutil.disk_usage("/").free > pow(1024, 3)  # 1 GB


def assert_valid_name(name: str) -> None:
    is_valid = re.match(r"^[A-Za-z0-9_]+$", name)
    if not is_valid:
        raise Exception(
            "Name {} must only contain alphanumeric and underscore characters".format(
                name
            )
        )


def raise_resp_exception_error(resp):
    if not resp.ok:
        message = None
        try:
            r_body = resp.json()
            message = r_body.get("message") or r_body.get("msg")
        except:
            # If we failed for whatever reason (parsing body, etc.)
            # Just return the code
            raise Exception(
                "HTTP Error received: {}".format(str(resp.status_code))
            ) from None

        if message:
            raise Exception("Error: {}".format(message))
        else:
            raise Exception(
                "HTTP Error received: {}".format(str(resp.status_code))
            ) from None


def determine_latest_version():
    from bs4 import BeautifulSoup
    from http import HTTPStatus
    import requests
    import re

    PACKAGE_REPO_URL = "https://aquarium-not-pypi.web.app/{}".format(__package__)
    SEM_VER_MATCHER = re.compile(
        f"{__package__}-(.*)\.tar\.gz"  # noqa: W605 (invalid escape seq)
    )

    r = requests.get(PACKAGE_REPO_URL)
    if r.status_code == HTTPStatus.OK:
        # Python package repos have a standard layout:
        # https://packaging.python.org/guides/hosting-your-own-index/
        versions = BeautifulSoup(r.text, "html.parser").find_all("a")
        if len(versions) > 0:
            version_match = SEM_VER_MATCHER.match(versions[-1]["href"])
            if version_match != None:
                return version_match.group(1)
    return None


def check_if_update_needed():
    from importlib_metadata import version
    from termcolor import colored

    current_version = version(__package__)
    latest_version = determine_latest_version()

    if latest_version != None and current_version != latest_version:
        print(
            colored(
                f"aquariumlearning: Please upgrade from version {current_version} to latest version {latest_version}.",
                "yellow",
            )
        )


def add_object_user_attrs(
    attrs: Dict[str, Any], user_attrs: Optional[Dict[str, Any]]
) -> None:
    if user_attrs is not None:
        for k, v in user_attrs.items():
            if "user__" not in k:
                k = "user__" + k
            attrs[k] = v


TYPE_PRIMITIVE_TO_STRING_MAP = {
    str: "str",
    int: "int",
    float: "float",
    bool: "bool",
}

USER_METADATA_TYPES = Literal["str", "int", "float", "bool"]
POLYGON_VERTICES_KEYS = Literal["vertices"]
POSITION_KEYS = Literal["x", "y", "z"]
ORIENTATION_KEYS = Literal["w", "x", "y", "z"]
KEYPOINT_KEYS = Literal["x", "y", "name"]
