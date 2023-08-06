import os
import json
import requests
from typing import Dict
import logging

logger = logging.getLogger(__name__)


def local_crawler_post(link: str, data: Dict):
    link_url = os.environ.get("LOCAL_FPCRAWLER_URL")
    url = f'{link_url}{link}'
    response = requests.post(url, json=data)
    response_text = response.text
    if response.status_code != 200:
        logger.error(response_text)
        raise ValueError(f"Invalid response {response_text}")
    data = json.loads(response_text)
    return data


def external_crawler_post(link: str, data: Dict):
    link_url = os.environ.get("FPCRAWLER_URL")
    url = f'{link_url}{link}'
    response = requests.post(url, json=data)
    response_text = response.text
    if response.status_code != 200:
        logger.error(response_text)
        raise ValueError(f"Invalid response {response_text}")
    data = json.loads(response_text)
    return data

