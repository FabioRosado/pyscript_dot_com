import io
import json
from typing import Optional, Union

from pyscript import window

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


class BaseStorage:
    def __init__(self):
        self.project_id = _get_project_by_slug()
        self.cookies = get_page_cookies()
        self.browser_storage = browser_storage()

    def get(self, key: str, use_browser_storage: bool = True) -> dict:
        """Get state by key."""
        if not isinstance(key, str):
            raise ValueError("Key must be a string.")

        key = self._transform_key(key)
        if use_browser_storage:
            return self.browser_storage.get(key) or {}
        else:

            # TODO: Pseudo code
            # response = request(f"{PSDC_DOMAIN}/api/projects/{self.project_id}/state/{key}", cookies=self.cookies)
            # return response
            raise NotImplementedError

    def set(
        self, payload: Union[str, dict], key: str, use_browser_storage: bool = True
    ):
        """Set state."""
        if not isinstance(key, str):
            raise ValueError("Key must be a string.")

        if isinstance(payload, dict):
            payload = json.dumps(payload)
        elif isinstance(payload, str):
            payload = payload
        else:
            raise ValueError("Payload must be a dictionary or a string.")

        key = self._transform_key(key)
        if use_browser_storage:
            self.browser_storage.set(key, payload)
        else:
            # TODO: Pseudo code
            # response = request(f"{PSDC_DOMAIN}/api/projects/{self.project_id}/state/{key}", method="POST", body=state)
            # return response
            raise NotImplementedError

    def delete(self, key: str, use_browser_storage: bool = True):
        """Delete state by key."""
        if not isinstance(key, str):
            raise ValueError("Key must be a string.")

        key = self._transform_key(key)
        if use_browser_storage:
            self.browser_storage.delete(key)
        else:
            # TODO: Pseudo code
            # response = request(f"{PSDC_DOMAIN}/api/projects/{self.project_id}/state/{key}", method="DELETE", cookies=self.cookies)
            # return response
            raise NotImplementedError

    def _transform_key(self, key: str):
        return f"{self.__class__.__name__}_{key}"


class state(BaseStorage):
    pass


class store(BaseStorage):
    pass
    # def __init__(self):
    #     self.project_id = _get_project_by_slug()
    #     self.cookies = get_page_cookies()
    #     self.browser_storage = browser_storage()

    # def get(self, key: str, use_browser_storage: bool = True) -> dict:
    #     """Get state by key."""
    #     if not isinstance(key, str):
    #         raise ValueError("Key must be a string.")

    #     if use_browser_storage:
    #         return self.browser_storage.get(key) or {}
    #     else:

    #         # TODO: Pseudo code
    #         # response = request(f"{PSDC_DOMAIN}/api/projects/{self.project_id}/state/{key}", cookies=self.cookies)
    #         # return response
    #         raise NotImplementedError

    # def set(self, state: dict, key: str, use_browser_storage: bool = True):
    #     """Set state."""
    #     if not isinstance(state, dict):
    #         raise ValueError("State must be a dictionary.")

    #     if not isinstance(key, str):
    #         raise ValueError("Key must be a string.")

    #     if use_browser_storage:
    #         self.browser_storage.set(key, state)
    #     else:
    #         # TODO: Pseudo code
    #         # response = request(f"{PSDC_DOMAIN}/api/projects/{self.project_id}/state/{key}", method="POST", body=state)
    #         # return response
    #         raise NotImplementedError

    # def delete(self, key: str, use_browser_storage: bool = True):
    #     """Delete state by key."""
    #     if not isinstance(key, str):
    #         raise ValueError("Key must be a string.")

    #     if use_browser_storage:
    #         self.browser_storage.delete(key)
    #     else:
    #         # TODO: Pseudo code
    #         # response = request(f"{PSDC_DOMAIN}/api/projects/{self.project_id}/state/{key}", method="DELETE", cookies=self.cookies)
    #         # return response
    #         raise NotImplementedError


# class store:
#     def __init__(self):
#         self.project_id = _get_project_by_slug()
#         self.cookies = get_page_cookies()
#         self.browser_storage = browser_storage()

#     def get(self, key: str, use_browser_storage: bool = True) -> dict:
#         """Get the project storage contents."""
#         if not isinstance(key, str):
#             raise ValueError("Key must be a string.")

#         if use_browser_storage:
#             return self.browser_storage.get(key) or {}
#         else:
#             # TODO: Pseudo code
#             # response = request(f"https://pyscript.com/api/projects/{self.project_id}/storage/{key}", method="GET", cookies=self.cookies)
#             # return response
#             raise NotImplementedError

#     def set(
#         self, key: str, payload: Union[dict, str], use_browser_storage: bool = True
#     ):
#         """Set payload in store."""
#         if not isinstance(key, str):
#             raise ValueError("Key must be a string.")

#         if isinstance(payload, dict):
#             payload = json.dumps(payload)
#         elif isinstance(payload, str):
#             payload = payload
#         else:
#             raise ValueError("Payload must be a dictionary or a string.")

#         if use_browser_storage:
#             self.browser_storage.set(key, payload)
#         else:
#             # TODO: Pseudo code
#             # response = request(f"https://pyscript.com/api/projects/{self.project_id}/storage/{key}"", method="POST", body=state, cookies=self.cookies)
#             # return response
#             raise NotImplementedError

#     def delete(self, key: str, use_browser_storage: bool = True):
#         """Delete store by key."""
#         if not isinstance(key, str):
#             raise ValueError("Key must be a string.")

#         if use_browser_storage:
#             self.browser_storage.delete(key)
#         else:
#             # TODO: Pseudo code
#             # response = request(f"https://pyscript.com/api/projects/{self.project_id}/storage/{key}", method="DELETE", cookies=self.cookies)
#             # return response
#             raise NotImplementedError


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


class browser_storage:

    def get(self, key: str) -> Optional[dict]:
        """Get the browser storage contents."""
        if not isinstance(key, str):
            raise ValueError("Key must be a string.")

        item = window.localStorage.getItem(key)
        if item:
            try:
                return json.loads(item)
            except json.JSONDecodeError:
                return item
        else:
            return None

    def set(self, key: str, payload: Union[dict, str]):
        """Set payload in browser storage."""
        if not isinstance(key, str):
            raise ValueError("Key must be a string.")

        if isinstance(payload, dict):
            payload = json.dumps(payload)
        elif isinstance(payload, str):
            payload = payload
        else:
            raise ValueError("Payload must be a dictionary or a string.")

        window.localStorage.setItem(key, payload)

    def delete(self, key: str):
        """Delete browser storage by key."""
        if not isinstance(key, str):
            raise ValueError("Key must be a string.")

        window.localStorage.removeItem(key)
