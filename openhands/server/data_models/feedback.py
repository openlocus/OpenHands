import json
from typing import Any, Literal

import requests
from pydantic import BaseModel

from openhands.core.logger import openhands_logger as logger


class FeedbackDataModel(BaseModel):
    version: str
    email: str
    token: str
    feedback: Literal['positive', 'negative']
    permissions: Literal['public', 'private']
    trajectory: list[dict[str, Any]]


FEEDBACK_URL = 'https://share-od-trajectory-3u9bw9tx.uc.gateway.dev/share_od_trajectory'


def store_feedback(feedback: FeedbackDataModel) -> dict[str, str]:
    # Start logging
    display_feedback = feedback.model_dump()
    if 'trajectory' in display_feedback:
        display_feedback['trajectory'] = (
            f"elided [length: {len(display_feedback['trajectory'])}"
        )
    if 'token' in display_feedback:
        display_feedback['token'] = 'elided'
    logger.debug(f'Got feedback: {display_feedback}')
    # Start actual request
    response = requests.post(
        FEEDBACK_URL,
        headers={'Content-Type': 'application/json'},
        json=feedback.model_dump(),
    )
    if response.status_code != 200:
        raise ValueError(f'Failed to store feedback: {response.text}')
    response_data = json.loads(response.text)
    logger.debug(f'Stored feedback: {response.text}')
    return response_data
