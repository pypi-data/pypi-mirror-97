from typing import Union, Optional

from pydantic import BaseModel
import requests


class SDKConfiguration(BaseModel):
    access_token: str
    secret_token: str
    project_identifier: str
    partition_identifier: Optional[str] = None # Required for the AccessSDK in particular
    base_url_override: Optional[str] = None


def make_requests(sdk_configuration: SDKConfiguration) -> requests.Session:
    requests_session: requests.Session = requests.Session()

    requests_session.headers.update({
        'X-Access-Token': sdk_configuration.access_token,
        'X-Secret-Token': sdk_configuration.secret_token,
        'Ehelply-Project': sdk_configuration.project_identifier
    })

    return requests_session
