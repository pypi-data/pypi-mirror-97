from ruleau.rule import rule
from ruleau.execute import ExecutionResult


def Any(*args):
    @rule(depends_on=args)
    def any_aggregator(context: ExecutionResult, _):
        results = [result.value for result in context.dependant_results]
        return any(results)

    return any_aggregator


def All(*args):
    @rule(depends_on=args)
    def all_aggregator(context: ExecutionResult, _):
        return all(result.value for result in context.dependant_results)

    return all_aggregator
