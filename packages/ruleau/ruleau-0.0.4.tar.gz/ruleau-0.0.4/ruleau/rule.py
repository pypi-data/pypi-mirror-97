import uuid
from ruleau.constants import OverrideLevel


class Rule:
    def __init__(
        self, logic_func, depends_on, override_name, override_level, lazy_dependencies
    ):
        self.id = str(uuid.uuid4())
        self.logic_func = logic_func
        self.depends_on = depends_on
        self.override_name = override_name
        self.override_level = override_level
        self.__name__ = logic_func.__name__
        self.lazy_dependencies = lazy_dependencies

    def __str__(self):
        return self.__name__

    def __call__(self, *args, **kwargs):
        return self.logic_func(*args, **kwargs)


def rule(
    depends_on=None,
    override_name=None,
    override_level=OverrideLevel.ANY_OVERRIDE,
    lazy_dependencies=False,
):
    """
    Creates a rule from a function
    """
    depends_on = depends_on or []
    override_name = override_name or uuid.uuid4().hex

    def rule_decorator(func):
        return Rule(func, depends_on, override_name, override_level, lazy_dependencies)

    return rule_decorator
