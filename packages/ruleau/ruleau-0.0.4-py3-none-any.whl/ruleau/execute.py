import logging
from json import dumps
from typing import Iterable, Optional, Dict
from typing import Any, AnyStr
from collections import OrderedDict
from ruleau.constants import OverrideLevel
from copy import deepcopy
from ruleau.rule import Rule

logger = logging.getLogger(__name__)


class DependantResults:
    def __init__(self, dependants: Iterable[Rule], payload, overrides, lazy=False):
        self.dependants = {dep.__name__: dep for dep in dependants}
        self.payload = deepcopy(payload)
        self.overrides = overrides
        if not lazy:
            self.results = {
                depend.__name__: execute(depend, self.payload, self.overrides)
                for depend in dependants
            }
        else:
            self.results = {}

    def run(self, name):
        """
        Run and store the result of a rule dependency
        :param name:
        :return:
        """

        if name not in self.dependants:
            raise AttributeError(
                f"Result for rule '{name}' not available, as it was not "
                f"declared as a dependency. "
                f"depends_on={dumps(list(self.dependants.keys()))}"
            )

        if name not in self.results:
            self.results[name] = execute(
                self.dependants[name], self.payload, self.overrides
            )
        return self.results[name]

    def __getattr__(self, name):
        try:
            # Enable access to normal python properties
            return super().__getattr__(name)
        except AttributeError:
            # If an attribute wasn't found, check for the dependency
            return self.run(name)

    def __iter__(self):
        for dep in self.dependants:
            yield self.__getattr__(dep)


class ExecutionResult:
    def __init__(
        self,
        executed_rule: Rule,
        value,
        dependant_results: DependantResults,
        is_overridden: bool = False,
        original_value=None,
    ):
        self.executed_rule = executed_rule
        self.value = value
        self.is_overridden = is_overridden
        self.original_value = original_value
        self.dependant_results = dependant_results


def execute(
    executable_rule: Rule,
    payload,
    overrides: Optional[Dict[AnyStr, Any]] = None,
    api_config: Optional[Dict[AnyStr, Any]] = None,
) -> ExecutionResult:
    """
    Executes the provided rule, following dependencies and
    passing in results accordingly
    """
    payload_copy = OrderedDict(payload)

    depend_results = DependantResults(
        executable_rule.depends_on,
        payload_copy,
        overrides,
        lazy=executable_rule.lazy_dependencies,
    )
    context = ExecutionResult(executable_rule, None, depend_results)

    result = ExecutionResult(
        executable_rule, executable_rule(context, payload_copy), depend_results
    )

    if overrides and executable_rule.override_name in overrides:
        # TODO: We should check on the first call to execute that
        # the overrides specified will actually be used, i.e. it
        # is an error to pass in an override for a rule which doesn't
        # exist

        if executable_rule.override_level == OverrideLevel.NO_OVERRIDE:
            raise Exception(
                "Tried to override rule '{rule.override_name}' "
                "(function '{rule.__name__}'), but override level is "
                "set to NO_OVERRIDE"
            )

        override_result = overrides[executable_rule.override_name]

        logger.info(
            "Overriding result for rule '%s' (function '%s'): new value = '%s'",
            executable_rule.override_name,
            executable_rule.__name__,
            override_result,
        )

        result.is_overridden = True
        result.original_value = result.value
        result.value = override_result
    if api_config:
        from ruleau.adapter import ApiAdapter

        ApiAdapter(payload=payload, result=result, **api_config).send()
    return result
