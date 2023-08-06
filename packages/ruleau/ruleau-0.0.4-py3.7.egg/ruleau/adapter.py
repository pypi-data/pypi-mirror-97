from typing import AnyStr, Any, List, Dict, Optional
from ruleau.execute import ExecutionResult
from urllib.parse import urljoin
import requests


class ApiAdapter:

    base_url: AnyStr
    api_key: Optional[AnyStr]
    result: ExecutionResult
    payload: Dict[AnyStr, Any]

    def __init__(
        self,
        base_url: AnyStr,
        payload: Dict[AnyStr, Any],
        result: ExecutionResult,
        api_key: Optional[AnyStr] = None,
    ):
        self.base_url = base_url
        self.api_key = api_key
        self.result = result
        self.payload = payload

    @staticmethod
    def flatten(
        results: dict, output: list = [], order: int = 0
    ) -> List[Dict[AnyStr, Any]]:
        """
        Flatten the processed execution result
        :param results:
        :param output:
        :param order:
        :return:
        """
        if len(results["dependencies"]):
            # If there are dependencies in the list, recurse, flatten, order
            for dependency in results["dependencies"]:
                ApiAdapter.flatten(dependency, output, order + 1)
            results["dependencies"] = [x["name"] for x in results["dependencies"]]
        # Add the order to store in the API
        results["order"] = order
        # Append processed output to the final output
        output.append(results)
        return output

    @staticmethod
    def process(result: ExecutionResult) -> Dict[AnyStr, Any]:
        """
        Process the execution result into a dictionary
        :param result:
        :return:
        """
        return {
            "id": result.executed_rule.id,
            "name": result.executed_rule.__name__,
            "description": result.executed_rule.__doc__,
            "dependencies": [
                ApiAdapter.process(result.dependant_results.results[rule.__name__])
                for rule in result.executed_rule.depends_on
            ],
            "result": {
                "result": result.value,
            },
        }

    def send(self) -> bool:
        """
        Send the case payload to the the API
        :return:
        """
        rules = ApiAdapter.flatten(ApiAdapter.process(self.result), [])
        request_payload = {"payload": self.payload, "rules": rules}
        # Post the case results to the API
        response = requests.post(
            urljoin(self.base_url, "/api/v1/cases"), json=request_payload
        )
        return response.status_code == 201
