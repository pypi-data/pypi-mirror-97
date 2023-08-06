"""Flywheel Core HTTP API Client."""
# pylint: disable=too-few-public-methods
import copy
import functools
import os
import re
import typing as t
import warnings

import orjson
from fw_http_client import HttpClient, HttpConfig
from memoization import cached
from packaging import version
from pydantic import AnyHttpUrl, root_validator

__all__ = ["CoreConfig", "CoreClient", "get_client"]


class CoreConfig(HttpConfig):
    """Flywheel Core API connection and authentication configuration."""

    class Config:
        """Enable envvar config using prefix 'FW_CORE_'."""

        env_prefix = "fw_core_"

    api_key: t.Optional[str]
    auth_token: t.Optional[str]
    secure: bool = True
    url: t.Optional[AnyHttpUrl]
    drone_secret: t.Optional[str]
    drone_method: t.Optional[str]
    drone_name: t.Optional[str]

    @root_validator
    @classmethod
    def validate_config(cls, values: dict) -> dict:
        """Check if all required config params were set or raise AssertionError.

        Acceptable options:
         * api_key including the site URL as shown on the UI (profile page)
         * url and api_key
         * url and auth_token
         * url and drone_secret, drone_method, drone_name
        """
        api_key, url = values.get("api_key"), values.get("url")
        assert api_key or url, "api_key or url required"

        # extract url from api_key assuming standard format "host[:port]:key"
        if api_key and not url:
            match = re.match(r"(?P<host>[^:]+)(:(?P<port>\d+))?:(?P<key>)", api_key)
            assert match, "url required"
            scheme = "https" if values["secure"] else "http"
            host, port = match.group("host"), match.group("port")
            url = f"{scheme}://{host}"
            if port:
                url += f":{port}"
            values["url"] = url

        # get the auth params: api_key or auth_token or drone_secret + _method + _name
        auth_token = values.get("auth_token")
        drone_secret = values.get("drone_secret")
        if not (api_key or auth_token or drone_secret):
            raise ValueError("api_key or auth_token or drone_secret required")
        if drone_secret and not api_key:
            warnings.warn(
                "drone_secret is deprecated - use api_key instead",
                category=DeprecationWarning,
                stacklevel=2,
            )
            method, name = values.get("drone_method"), values.get("drone_name")
            assert method and name, "drone_method and drone_name required"

        return values


class CoreClient(HttpClient):
    """Flywheel Core HTTP API Client."""

    def __init__(self, config: t.Optional[CoreConfig] = None) -> None:
        """Init Core client with base URL and API key or drone secret auth."""
        config = config or CoreConfig()
        config.baseurl = f"{config.url}/api"
        if config.api_key:
            config.headers["Authorization"] = f"scitran-user {config.api_key}"
        elif config.auth_token:
            config.headers["Authorization"] = config.auth_token
        else:
            config.headers["X-SciTran-Auth"] = config.drone_secret
            config.headers["X-SciTran-Method"] = config.drone_method
            config.headers["X-SciTran-Name"] = config.drone_name
        super().__init__(config)

    @functools.cached_property
    def config(self) -> dict:
        """Return Core's configuration."""
        return self.get("/config")

    @functools.cached_property
    def version(self) -> t.Optional[str]:
        """Return Core's release version."""
        return self.get("/version").release

    @functools.cached_property
    def status(self) -> dict:
        """Return the client's auth status."""
        status = self.get("/auth/status")
        if status.is_device:
            status["info"] = self.get(f"/devices/{status.origin.id}")
        else:
            status["info"] = self.get("/users/self")
        return status

    def check_feature(self, feature: str) -> bool:
        """Return True if Core has the given feature and it's enabled."""
        return bool(self.config.features.get(feature))  # type: ignore

    def check_version(self, min_ver: str) -> bool:
        """Return True if Core's version is greater or equal to 'min_ver'."""
        if not self.version:
            # assume latest on dev deployments without a version
            return True
        return version.parse(self.version) >= version.parse(min_ver)

    def upload(
        self,
        filepath: str,
        metadata: dict,
        method: str = "label",
        fill: bool = False,
    ) -> dict:
        """Upload a file using the label or reaper /upload endpoint."""
        assert method in ("label", "reaper"), f"Invalid upload method {method!r}"
        endpoint = f"/upload/{method}"
        filename, metadata = get_upload_info(filepath, metadata, method, fill)
        with open(filepath, "rb") as file:
            if self.config.get("signed_url"):
                payload = {"filenames": [filename], "metadata": metadata}
                upload = self.post(endpoint, params={"ticket": ""}, json=payload)
                self.put(upload.urls[filename], data=file)
                response = self.post(endpoint, params={"ticket": upload.ticket})
            else:
                meta = orjson.dumps(metadata)
                response = self.post(endpoint, files={filename: file, "metadata": meta})
        return response


@cached
def get_client(**kwargs: t.Any) -> CoreClient:
    """Return (cached) CoreClient configured via kwargs."""
    return CoreClient(CoreConfig(**kwargs))


def get_upload_info(
    filepath: str, meta: dict, method: str, fill: bool
) -> t.Tuple[str, dict]:
    """Return (filename, meta) tuple for given upload parameters.

    Core expects label- and reaper uploads as file forms with two files:
      * filename: with the actual file contents
      * metadata: json describing hierarchy placement and additional meta

    Core requires that the metadata has:
      * group._id set to a string ("" allowed)
      * project.label set to a string ("" allowed)
      * subject - if present - embedded under the session
      * uids in case of reaper uploads:
        * session.uid set to a string ("" allowed)
        * acquisition.uid set to a string if the acquisition is present ("" allowed)
      * the filename referenced on some hierarchy level (project or below)

    This function helps getting a correct (filename, metadata) pair where the
    filename is set appropriately if it was present in the metadata, or defaults
    to using the file's basename while making sure it is referenced in the meta.
    The subject - if present - is automatically embedded into the session.

    If fill=True then group._id and project.label, session.uid and acquisition.uid
    are auto-populated with empty strings as necessary to avoid rejected uploads.
    """
    meta = copy.deepcopy(meta)
    # populate group._id and project.label if not set
    if fill:
        if not meta.setdefault("group", {}).get("_id"):
            meta["group"]["_id"] = ""
        if not meta.setdefault("project", {}).get("label"):
            meta["project"]["label"] = ""
    # try to get filename from the meta (going bottom up, looking for files)
    filename = meta.get("file", {}).get("name")
    for level in ("acquisition", "session", "subject", "project"):
        if not meta.get(level):
            continue
        cont = meta[level]
        if filename:
            # using fw-meta file info
            cont["files"] = [meta.pop("file")]
            break
        if cont.get("files"):
            filename = cont["files"][0].get("name")
            break
    # use basename by default and set it in the meta at acquisition level
    if not filename:
        filename = os.path.basename(filepath)
        files = meta.setdefault("acquisition", {}).setdefault("files", [{}])
        files[0]["name"] = filename
    # embed subject meta under session
    if "subject" in meta:
        meta.setdefault("session", {})["subject"] = meta.pop("subject")
    # populate session.uid and acquisition.uid on reaper uploads
    if fill and method == "reaper":
        meta.setdefault("session", {}).setdefault("uid", "")
        if "acquisition" in meta:  # acquisition may be omitted
            meta.setdefault("acquisition", {}).setdefault("uid", "")
    return filename, meta
