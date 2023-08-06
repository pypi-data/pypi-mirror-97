"""issues.py
============
Functionality related to issue management
"""

import requests
from collections.abc import Iterable
from .util import raise_resp_exception_error


class IssueElement:
    """Definition for issue element.

    Args:
        element_id (str): The element id.
        frame_id (str): The frame id of the element.
        element_type (str): The element type of the issue element ("frame" or "crop").
        dataset (str): (*For read purposes, not element modification*). The base dataset an element is from.
        inference_set (str): (*For read purposes, not element modification*). The inference set an element is from (if any).
        status (str): (*For read purposes, not element modification*). The status of the element.
        frame_data: (*For read purposes, not element modification*). JSON object that is based on either a LabeledFrame or InferencesFrame
        crop_data: (*For read purposes, not element modification*). JSON object for the specific "frame_data" crop that a "crop"-type element is based on.
        label_metadata: (*For read purposes, not element modification*). JSON object with confidence and IOU info if the element was created from a ground truth/inference comparison.
    """

    def __init__(
        self,
        element_id,
        frame_id,
        element_type,
        status=None,
        dataset=None,
        inference_set=None,
        frame_data=None,
        crop_data=None,
        label_metadata=None,
    ):
        if element_type != "crop" and element_type != "frame":
            raise Exception('element_type must be either "crop" or "frame"')

        self.element_id = element_id
        self.frame_id = frame_id
        self.element_type = element_type
        self.status = status
        self.dataset = dataset
        self.inference_set = inference_set
        self.frame_data = frame_data
        self.crop_data = crop_data
        self.label_metadata = label_metadata

    def to_dict(self):
        return {
            "element_id": self.element_id,
            "frame_id": self.frame_id,
            "element_type": self.element_type,
            "status": self.status,
            "dataset": self.dataset,
            "inference_set": self.inference_set,
            "frame_data": self.frame_data,
            "crop_data": self.crop_data,
            "label_metadata": self.label_metadata,
        }

    # For element modification
    def _to_api_format(self):
        return {
            "id": self.element_id,
            "frameId": self.frame_id,
            "type": self.element_type,
        }


class Issue:
    """Definition for issue.

    Args:
        name (str): The issue name.
        dataset (str): The dataset for this issue.
        elements (List[IssueElement]): The elements of the issue.
        element_type (str): The element type of the issue ("frame", "crop").
        created_at (datetime): The time of issue creation.
        updated_at (datetime): The time of last issue update.
        reporter (str): Email of issue creator.
        assignee (Optional[str], optional): Email of the person assigned the issue. Defaults to None.
        state (str): Current state of issue ("triage", "inProgress", "inReview", "resolved", "cancelled"). Defaults to "triage".
        issue_id (str): The issue id.
        inference_set (Optional[str], optional): The inference set for this issue. Defaults to None.
    """

    def __init__(
        self,
        name,
        dataset,
        elements,
        element_type,
        created_at=None,
        updated_at=None,
        reporter=None,
        assignee=None,
        state=None,
        issue_id=None,
        inference_set=None,
    ):

        self.name = name
        self.dataset = dataset
        self.elements = elements
        self.element_type = element_type
        self.created_at = created_at
        self.updated_at = updated_at
        self.reporter = reporter
        self.assignee = assignee
        self.state = state
        self.issue_id = issue_id
        self.inference_set = inference_set

    def __repr__(self):
        return "Issue {} ({})".format(self.issue_id, self.name)

    def __str__(self):
        return "Issue {} ({})".format(self.issue_id, self.name)

    def to_dict(self):
        return {
            "name": self.name,
            "dataset": self.dataset,
            "elements": [x.to_dict() for x in self.elements],
            "element_type": self.element_type,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "reporter": self.reporter,
            "assignee": self.assignee,
            "state": self.state,
            "issue_id": self.issue_id,
            "inference_set": self.inference_set,
        }


class IssueManager:
    """An issue manager for interacting with issues within a given project.

    Args:
        client (Client): An Aquarium Learning Python Client object.
        project_id (str): The project id associated with this manager.
    """

    def __init__(self, client, project_id):
        self.client = client
        self.project_id = project_id

    def _issue_from_api_resp(self, api_resp):
        # TODO: Hack because internal data model for issues is still dataset/compare dataset,
        # not dataset + inference set + other inference set.
        if api_resp.get("compare_dataset"):
            dataset = api_resp.get("compare_dataset").split(".")[1]
            inference_set = api_resp.get("dataset").split(".")[1]
        elif api_resp.get("dataset"):
            dataset = api_resp.get("dataset").split(".")[1]
            inference_set = None
        else:  # in the case of an issue with no elements
            dataset = None
            inference_set = None

        elements = []
        for raw_el in api_resp.get("elements"):
            elements.append(
                IssueElement(
                    element_id=raw_el.get("id"),
                    frame_id=raw_el.get("frameId"),
                    element_type=raw_el.get("type"),
                    status=raw_el.get("status"),
                    dataset=raw_el.get("dataset"),
                    inference_set=raw_el.get("inferenceSet"),
                    frame_data=raw_el.get("frameData"),
                    crop_data=raw_el.get("cropData"),
                    label_metadata=raw_el.get("labelMetadata"),
                )
            )

        return Issue(
            name=api_resp.get("name"),
            element_type=api_resp.get("element_type"),
            created_at=api_resp.get("created_at"),
            updated_at=api_resp.get("updated_at"),
            reporter=api_resp.get("reporter"),
            assignee=api_resp.get("assignee"),
            state=api_resp.get("state"),
            issue_id=api_resp.get("id"),
            dataset=dataset,
            inference_set=inference_set,
            elements=elements,
        )

    def add_elements_to_issue(self, issue_id, elements):
        """Add elements to an issue.

        Args:
            issue_id (str): The issue id.
            elements (List[IssueElement]): The elements to add to the issue.
        """
        if not isinstance(elements, Iterable):
            raise Exception("elements must be an iterable of IssueElement")

        # Validate contents of iterables:
        element_type_set = set()
        for element in elements:
            if not isinstance(element, IssueElement):
                raise Exception("elements must be an iterable of IssueElement")
            element_type_set.add(element.element_type)

        if len(element_type_set) != 1:
            raise Exception("Elements must contain exactly one element type")

        element_type = next(iter(element_type_set))
        payload = {
            "element_type": element_type,
            "elements": [x._to_api_format() for x in elements],
            "edit_type": "add",
        }

        url = "/projects/{}/issues/{}/elements".format(self.project_id, issue_id)
        r = requests.patch(
            self.client.api_endpoint + url,
            headers=self.client._get_creds_headers(),
            json=payload,
        )

        raise_resp_exception_error(r)

    def remove_elements_from_issue(self, issue_id, elements):
        """Remove elements from an issue.

        Args:
            issue_id (str): The issue id.
            elements (List[IssueElement]): The elements to remove from the issue.
        """
        if not isinstance(elements, Iterable):
            raise Exception("elements must be an iterable of IssueElement")

        # Validate contents of iterables:
        element_type_set = set()
        for element in elements:
            if not isinstance(element, IssueElement):
                raise Exception("elements must be an iterable of IssueElement")
            element_type_set.add(element.element_type)

        if len(element_type_set) != 1:
            raise Exception("Elements must contain exactly one element type")

        element_type = next(iter(element_type_set))
        payload = {
            "element_type": element_type,
            "elements": [x._to_api_format() for x in elements],
            "edit_type": "remove",
        }

        url = "/projects/{}/issues/{}/elements".format(self.project_id, issue_id)
        r = requests.patch(
            self.client.api_endpoint + url,
            headers=self.client._get_creds_headers(),
            json=payload,
        )

        raise_resp_exception_error(r)

    def list_issues(self):
        """List issues in the associated project.

        NOTE: this does NOT include the `frame_data` or `crop_data` information for the issue elements.
        (Use `get_issue` instead to see that info).

        Returns:
            List[Issue]: List of all issues data.
        """
        url = "/projects/{}/issues".format(self.project_id)
        r = requests.get(
            self.client.api_endpoint + url, headers=self.client._get_creds_headers()
        )

        raise_resp_exception_error(r)
        return [self._issue_from_api_resp(x) for x in r.json()]

    def create_issue(self, name, dataset, elements, element_type, inference_set=None):
        """Create an issue.

        Args:
            name (str): The issue name.
            dataset (str): The dataset for this issue.
            elements (List[IssueElement]): The initial elements of the issue.
            element_type (str): The element type of the issue ("frame" or "crop").
            inference_set (Optional[str], optional): The inference set for this issue. Defaults to None.
        Returns:
            str: The created issue id.
        """
        if not isinstance(name, str):
            raise Exception("Issue names must be strings")

        if not self.client.dataset_exists(self.project_id, dataset):
            raise Exception("Dataset {} does not exist".format(dataset))

        if inference_set is not None:
            if not self.client.dataset_exists(self.project_id, inference_set):
                raise Exception("Inference set {} does not exist".format(inference_set))

        if element_type != "frame" and element_type != "crop":
            raise Exception('element type must be "frame" or "crop"')

        if not isinstance(elements, Iterable):
            raise Exception("elements must be an iterable of IssueElement")

        # Validate contents of iterables:
        for element in elements:
            if not isinstance(element, IssueElement):
                raise Exception("elements must be an iterable of IssueElement")
            if element.element_type != element_type:
                raise Exception(
                    "Child element {} has element type {} which conflicts with issue element type {}".format(
                        element.element_id, element.element_type, element_type
                    )
                )

        payload = {
            "name": name,
            "elements": [x._to_api_format() for x in elements],
            "element_type": element_type,
        }

        # TODO: Hack because internal data model for issues is still dataset/compare dataset,
        # not dataset + inference set + other inference set.

        if inference_set is None:
            payload["dataset"] = ".".join([self.project_id, dataset])
        else:
            payload["dataset"] = ".".join([self.project_id, inference_set])
            payload["compare_dataset"] = ".".join([self.project_id, dataset])

        url = "/projects/{}/issues".format(self.project_id)
        r = requests.post(
            self.client.api_endpoint + url,
            headers=self.client._get_creds_headers(),
            json=payload,
        )

        raise_resp_exception_error(r)
        resp_data = r.json()

        return resp_data["id"]

    def get_issue(self, issue_id):
        """Get a specific issue in the associated project.
        This will also include all associated frame metadata associated with each element.

        Args:
            issue_id (str): The issue id.

        Returns:
            Issue: The issue data (including frame_data, crop_data, and label_metadata).
        """
        url = "/projects/{}/issues/{}/download_elements".format(
            self.project_id, issue_id
        )
        r = requests.get(
            self.client.api_endpoint + url, headers=self.client._get_creds_headers()
        )

        raise_resp_exception_error(r)
        return self._issue_from_api_resp(r.json())

    def delete_issue(self, issue_id):
        """Delete an issue.

        Args:
            issue_id (str): The issue id.
        """
        url = "/projects/{}/issues/{}".format(self.project_id, issue_id)
        r = requests.delete(
            self.client.api_endpoint + url, headers=self.client._get_creds_headers()
        )

        raise_resp_exception_error(r)
