# https://pydantic-docs.helpmanual.io/
import numpy as np
import uuid
from datetime import datetime
from typing import List, Union
from attr import attrib, attrs


def list_of_humans_converter(
        possible_humans: Union[List[dict], List['Human']]) -> List['Human']:
    return [
        Human(**x) if isinstance(x, dict) else x
        for x in possible_humans
        if isinstance(x, (Human, dict))
    ]


@attrs(frozen=True)
class Human(object):
    """
    Represents the type of a value an attribute can hold
    """
    name = attrib(type=str)
    dob = attrib(type=datetime)
    friends = attrib(
        type=List['Human'],
        converter=list_of_humans_converter,
        factory=list
    )


def generate_alt_1(num_to_generate):
    for x in range(num_to_generate):
        yield Human(
            name=str(uuid.uuid4()),
            dob=datetime.utcnow(),
            friends=[
                dict(name=str(uuid.uuid4()), dob=datetime.utcnow())
            ]
        )


def generate_alt_2(num_to_generate):
    return map(
        lambda x: Human(
            name=str(uuid.uuid4()),
            dob=datetime.utcnow(),
            friends=[
                dict(name=str(uuid.uuid4()), dob=datetime.utcnow())
            ]
        ),
        np.ones((num_to_generate, 1))
    )


if __name__ == "__main__":
    jack = Human(name=str(uuid.uuid4()), dob=datetime.utcnow())
    jill = Human(name="jill", dob=datetime.utcnow(), friends=[jack])
    print(jack)
    print(jill)
