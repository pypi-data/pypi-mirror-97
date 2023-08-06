"""JSON serialization/deserialization functions.

.. module:: serialize
    :synopsis: JSON serialization/deserialization functions.
"""
import json
from typing import Mapping, List

from repobee_plug.hook import Result, Status


def result_mapping_to_json(result_mapping: Mapping[str, List[Result]]) -> str:
    """Serialize a result mapping ``repo_name: str -> hook_results:
    List[Result]`` to JSON.
    """
    hook_results_as_dicts = {
        repo_name: {
            h.name: {"status": h.status.value, "msg": h.msg, "data": h.data}
            for h in hook_results
        }
        for repo_name, hook_results in result_mapping.items()
    }
    return json.dumps(hook_results_as_dicts, indent=4, ensure_ascii=False)


def json_to_result_mapping(json_string: str,) -> Mapping[str, List[Result]]:
    """Deserialize a JSON string to a mapping ``repo_name: str -> hook_results:
    List[Result]``
    """
    json_dict = json.loads(json_string)
    return {
        repo_name: [
            Result(
                name=hook,
                status=Status(val["status"]),
                msg=val["msg"],
                data=val["data"],
            )
            for hook, val in hook_dicts.items()
        ]
        for repo_name, hook_dicts in json_dict.items()
    }
