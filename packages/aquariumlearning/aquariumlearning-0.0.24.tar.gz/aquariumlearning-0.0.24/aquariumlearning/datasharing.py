import requests
from google.cloud import storage
from http import HTTPStatus


def check_urls(urls, gs_client):
    result = {}
    for url in urls:
        result[url] = check_url(url, gs_client)
    return result


def check_url(url, gs_client):
    if url.lower().startswith("gs://"):
        if gs_client is None:
            return "SKIPPED"
        else:
            bucket_name, path = url.replace("gs://", "").split("/", 1)
            try:
                bucket = gs_client.get_bucket(bucket_name)
                blob = bucket.get_blob(path)

                if blob is None:
                    return "FAILURE"
                else:
                    return "SUCCESS"
            except:
                return "FAILURE"
    elif url.lower().startswith("http"):
        try:
            code = requests.get(url, timeout=5).status_code
            if code == HTTPStatus.OK:
                return "SUCCESS"
            else:
                return "FAILURE"
        except:
            return "FAILURE"
    else:
        return "INVALID_URL"


def get_mode(urls, local_results, server_results):
    modes = {}
    for url in urls:
        if server_results[url] == "FAILURE":
            if local_results[url] == "SUCCESS":
                modes[url] = "ANONYMOUS"
            elif local_results[url] == "SKIPPED":
                modes[url] = "INACCESSIBLE"
            elif local_results[url] == "FAILURE":
                modes[url] = "INACCESSIBLE"
        elif server_results[url] == "SUCCESS":
            modes[url] = "VALID"
        elif server_results[url] == "INVALID_URL":
            modes[url] = "INVALID_URL"
    return modes


def get_errors(mode, dataset):
    errors = []

    is_anon = False
    for url in mode:
        if mode[url] == "INVALID_URL":
            errors += [
                f"{url} is not a supported URL format. Please provide a URL starting with gs://, http://, or https://"
            ]
        elif mode[url] == "INACCESSIBLE":
            errors += [
                f"{url} is not an accessible URL from Aquarium servers or this machine. Please verify the URL path."
            ]
        elif mode[url] == "ANONYMOUS":
            is_anon = True

    if is_anon:
        if len(dataset._temp_frame_embeddings_file_names) == 0:
            errors += [
                "Anonymous mode detected without embeddings. Please provide your own embeddings. Aquarium cannot compute embeddings in anonymous mode since images are inaccessible from the server."
            ]

    return errors
