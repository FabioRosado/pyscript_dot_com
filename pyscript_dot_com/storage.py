import io
import json
from typing import Optional, Union

from pyscript_dot_com.const import PSDC_DOMAIN
from pyscript_dot_com.requests import request
from pyscript_dot_com.utils import get_page_cookies, get_project_slug_and_user_from_url


def save_file_to_project(file: io.BytesIO, name: Optional[str] = None):
    """Save a file to the project's storage.

    Args:
        file: The file to save.
        name: The name of the file to save.

    """
    cookies = get_page_cookies()
    project_id = _get_project_by_slug()

    if not name:
        name = file.name

    url = f"{PSDC_DOMAIN}/api/projects/{project_id}/files"
    files = {"file": (name, file)}
    response = request(url, method="POST", files=files, cookies=cookies)

    if isinstance(response, dict) and response.get("error"):
        raise Exception(response["error"])
    return True


# TODO: Maybe Storage should be a single class with methods for state and storage?


class state:
    def __init__(self):
        self.project_id = _get_project_by_slug()
        self.cookies = get_page_cookies()

    def get(self, key: str) -> dict:
        """Get state by key."""
        if not isinstance(key, str):
            raise ValueError("Key must be a string.")
        # TODO: Pseudo code
        # response = request(f"{PSDC_DOMAIN}/api/projects/{self.project_id}/state/{key}", cookies=self.cookies)
        # return response
        raise NotImplementedError

    def set(self, state: dict, key: str):
        """Set state."""
        if not isinstance(state, dict):
            raise ValueError("State must be a dictionary.")

        if not isinstance(key, str):
            raise ValueError("Key must be a string.")

        # TODO: Pseudo code
        # response = request(f"{PSDC_DOMAIN}/api/projects/{self.project_id}/state/{key}", method="POST", body=state)
        # return response
        raise NotImplementedError

    def delete(self, key: str):
        """Delete state by key."""
        if not isinstance(key, str):
            raise ValueError("Key must be a string.")
        # TODO: Pseudo code
        # response = request(f"{PSDC_DOMAIN}/api/projects/{self.project_id}/state/{key}", method="DELETE", cookies=self.cookies)
        # return response
        raise NotImplementedError


class store:
    def __init__(self):
        self.project_id = _get_project_by_slug()
        self.cookies = get_page_cookies()

    def get(self, key: str) -> dict:
        """Get the project storage contents."""
        if not isinstance(key, str):
            raise ValueError("Key must be a string.")

        # TODO: Pseudo code
        # response = request(f"https://pyscript.com/api/projects/{self.project_id}/storage/{key}", method="GET", cookies=self.cookies)
        # return response
        raise NotImplementedError

    def set(self, key: str, payload: Union[dict, str]):
        """Set payload in store."""
        if not isinstance(key, str):
            raise ValueError("Key must be a string.")

        if isinstance(payload, dict):
            payload = json.dumps(payload)
        elif isinstance(payload, str):
            payload = payload
        else:
            raise ValueError("Payload must be a dictionary or a string.")

        # TODO: Pseudo code
        # response = request(f"https://pyscript.com/api/projects/{self.project_id}/storage/{key}"", method="POST", body=state, cookies=self.cookies)
        # return response
        raise NotImplementedError

    def delete(self, key: str):
        """Delete store by key."""
        if not isinstance(key, str):
            raise ValueError("Key must be a string.")

        # TODO: Pseudo code
        # response = request(f"https://pyscript.com/api/projects/{self.project_id}/storage/{key}", method="DELETE", cookies=self.cookies)
        # return response
        raise NotImplementedError


def _get_project_by_slug() -> str:
    """Get the project by slug."""
    project_slug, user = get_project_slug_and_user_from_url()

    response = request(f"{PSDC_DOMAIN}/api/projects/{user}/{project_slug}")

    if not isinstance(response, dict):
        raise Exception("Error getting project by slug.")

    if isinstance(response, dict) and response.get("error"):
        raise Exception(response["error"])

    project_id = response.get("id")
    if not project_id:
        raise Exception("Error getting project by slug.")

    return project_id
