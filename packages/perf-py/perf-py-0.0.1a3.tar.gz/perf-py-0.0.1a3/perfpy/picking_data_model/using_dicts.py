# https://pydantic-docs.helpmanual.io/
import numpy as np
import uuid
from datetime import datetime


def generate_alt_1(num_to_generate):
    for x in range(num_to_generate):
        yield {
            "name": str(uuid.uuid4()),
            "dob": datetime.utcnow(),
            "friends": [
                {
                    "name": str(uuid.uuid4()),
                    "dob": datetime.utcnow(),
                    "friends": []
                }
            ]
        }


def generate_alt_2(num_to_generate):
    return map(
        lambda x: (
            {
                "name": str(uuid.uuid4()),
                "dob": datetime.utcnow(),
                "friends": [
                    {
                        "name": str(uuid.uuid4()),
                        "dob": datetime.utcnow(),
                        "friends": []
                    }
                ]
            }
        ),
        np.ones((num_to_generate, 1))
    )


if __name__ == "__main__":
    print(next(generate_alt_1(1)))
    print(next(generate_alt_2(1)))
