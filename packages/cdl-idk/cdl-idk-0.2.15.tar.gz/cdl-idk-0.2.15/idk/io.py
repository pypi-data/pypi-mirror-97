import json
from dataclasses import dataclass
from typing import List


@dataclass
class InsightData:
    """A container class for an actualized insight "payload".

    Constituants:
        tags (List[str]): A set of string tags comprissed of entities in the data (e.g. relevant string values in data dict).
        significance (float): This is the statictical significance of this instance of this insight result. From 0.0 being 
            insignificant to a 1.0 being most significant.
        data (dict): The result of your insight ready to be parsed by your transcribe function.
    """
    tags: List[str]
    significance: float
    data: dict


class _InsightDataEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, InsightData):
            return {"Payload": obj.data,
                    "Significance": obj.significance,
                    "Tags": obj.tags}
        return json.JSONEncoder.default(self, obj)
