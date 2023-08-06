from dataclasses import dataclass
from enum import Enum


class Action(str, Enum):
    AUTH = 'auth'

    def __str__(self) -> str:
        return str.__str__(self)


@dataclass
class PastaportoAction:
    action: Action
    payload: dict[str, str]


def create_pastaporto_action(action: Action, payload: dict[str, str]) -> PastaportoAction:
    return PastaportoAction(action=action, payload=payload)


def create_user_auth_pastaporto_action(user_id: int) -> PastaportoAction:
    return create_pastaporto_action(
        Action.AUTH,
        {
            'id': user_id
        }
    )
