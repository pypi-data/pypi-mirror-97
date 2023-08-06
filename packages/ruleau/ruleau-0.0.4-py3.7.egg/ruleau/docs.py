from os import mkdir, path
import sys
import importlib
import argparse
import inspect
from jinja2 import Template
from typing import Dict
import re


def _description_for(rst: str) -> str:
    """
    Takes a rule docstring as ReStructuredText, and returns just the line
    representing a description
    """
    # TODO - this can be better achieved by parsing using the actual docutils rst parser
    rst = rst or ""
    if "\n\n" in rst:
        return rst[: rst.index("\n\n")]
    return rst


def _properties_for(rst: str) -> Dict[str, str]:
    """
    Takes a rule docstring as ReStructuredText, and returns
    a dictionary of `property name`: `property value` pairs
    """
    # TODO - this can be better achieved by parsing using the actual docutils rst parser
    properties_regex = r"\.\. prop::\s+(?P<key>[^\n]*)\s+\n\s+(?P<value>[^\n]+)"

    rst = rst or ""
    return {k: v for (k, v) in re.findall(properties_regex, rst)}


def _title_for(name: str) -> str:
    return name.replace("_", " ").title()


def generate_documentation(rules) -> str:
    """
    Returns a HTML string, documenting the passed in rule and its
    dependants
    """

    with open(
        path.join(path.dirname(path.realpath(__file__)), "html", "documentation.html")
    ) as f:
        doc_template = Template(f.read())
    # Add more information to rules

    def _enrich_rule(rule):
        return {
            "name": rule.__name__,
            "title": _title_for(rule.__name__),
            "override_name": rule.override_name,
            "override_level": rule.override_level.name,
            "sourcecode": inspect.getsource(rule.logic_func),
            "unparsed_doc": rule.logic_func.__doc__,
            "description": _description_for(rule.logic_func.__doc__),
            "doc_properties": _properties_for(rule.logic_func.__doc__),
            "dependencies": [_enrich_rule(dependent) for dependent in rule.depends_on],
        }

    enriched_rules = [_enrich_rule(rule) for rule in rules]

    return doc_template.render(rules=enriched_rules)


def render_doc_for_module(module_file):
    spec = importlib.util.spec_from_file_location(module_file, module_file)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)

    # Pick rules to document
    rules = [
        rule
        for rule in vars(config).values()
        if getattr(type(rule), "__name__", None) == "Rule"
    ]
    if not rules:
        raise Exception("No rules found in {}.".format(module_file))

    return generate_documentation(rules)


def generate_and_save_to_file(input_files, output_dir):
    generated_docs = []

    if len(input_files) == 0:
        raise Exception("No file(s) supplied to generate documentation for.")

    if not path.exists(output_dir):
        mkdir(output_dir)

    for target_file in input_files:
        if not path.exists(target_file):
            raise ValueError(f"{target_file} does not exist")

        documentation = render_doc_for_module(target_file)

        output_filename = path.join(
            output_dir, "{}.html".format(path.basename(target_file).split(".")[0])
        )

        with open(output_filename, "w") as f:
            f.write(documentation)
        generated_docs.append(output_filename)

    print(
        f"{len(generated_docs)} doc{'s' if len(generated_docs) > 1 else ''} generated."
    )
    print("\n".join(generated_docs))

    return 0


def get_arguments(args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        dest="output_dir",
        default="./",
        help="Directory for generated documents",
    )
    parser.add_argument("files", nargs="*")
    return parser.parse_args(args)


def main():  # pragma: no cover
    """Console script for deft document generation.
    USAGE:
    ```bash
    $ ruleau-docs [--output-dir=<argument>] filename ...
    ```
    """
    args = get_arguments(sys.argv[1:])
    return generate_and_save_to_file(args.files, args.output_dir)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
