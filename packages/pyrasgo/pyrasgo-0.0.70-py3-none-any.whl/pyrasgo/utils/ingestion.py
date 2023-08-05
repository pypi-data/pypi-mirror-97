from types import FunctionType

from collections import OrderedDict
import logging
import os
import yaml

from uncompyle6.semantics import pysource

from pyrasgo.schemas.feature_set import v1


def load_feature_set_from_yaml(*, file_name: str, directory: str = None) -> v1.FeatureSet:
    if directory is None:
        directory = os.getcwd()

    if os.path.splitext(f"{directory}/{file_name}")[1] in ['yaml', 'yml']:
        raise ValueError("Must provide valid yaml file")

    with open(f"{directory}/{file_name}") as _yaml:
        return v1.FeatureSet.parse_obj(yaml.load(_yaml, Loader=yaml.SafeLoader)[0])


def save_feature_set_to_yaml(feature_set: v1.FeatureSet, *,
                             file_name: str, directory: str = None, overwrite: bool = True) -> None:
    if directory is None:
        directory = os.getcwd()

    if directory[-1] == "/":
        directory = directory[:-1]

    if file_name.split(".")[-1] not in ['yaml', 'yml']:
        file_name += ".yaml"

    if os.path.exists(f"{directory}/{file_name}") and overwrite:
        logging.warning(f"Overwriting existing file {file_name} in directory: {directory}")

    safe_dumper = yaml.SafeDumper
    safe_dumper.add_representer(v1.DataType, lambda self, data: self.represent_str(str(data.value)))
    safe_dumper.add_representer(OrderedDict, lambda self, data: self.represent_mapping('tag:yaml.org,2002:map',
                                                                                       data.items()))
    safe_dumper.ignore_aliases = lambda self, data: True

    with open(f"{directory}/{file_name}", "w") as _yaml:
        # TODO: Not truly specifying an order yet.
        yaml.dump(data=OrderedDict(feature_set.dict(exclude_unset=True)), Dumper=safe_dumper, stream=_yaml)


def generate_feature_set_files(source_table: str, name: str = None, *,
                               feature_set: v1.FeatureSet, function: FunctionType = None,
                               directory: str = None, overwrite: bool = False) -> tuple:
    """
    return: yml file
    """
    if directory is None:
        directory = os.getcwd()
    working_directory = f"{directory}/featureSets/{name or source_table}"
    os.makedirs(working_directory, exist_ok=True)

    feature_set_yaml = f"{source_table}.yaml"
    requirements_txt = "requirements.txt"
    function_py = f"{function.__name__}.py" if function else ""
    files_to_create = [feature_set_yaml] if function_py == "" else [feature_set_yaml, requirements_txt, function_py]

    for existing_file in os.listdir(working_directory):
        if existing_file == requirements_txt and not overwrite:
            raise ValueError(f"There is {requirements_txt} existing in the directory {working_directory}")

        if existing_file in files_to_create:
            logging.warning(f"The directory {working_directory} contains the file "
                            f"({existing_file}) it will be overwritten.")

    if function:
        with open(f"{working_directory}/{function_py}", 'w') as _py:
            _py.write(get_function_code(function=function))

        with open(f"{working_directory}/{requirements_txt}", 'w') as _txt:
            _txt.writelines([f"{requirement.project_name}=={requirement.parsed_version}\n"
                             for requirement in identify_requirements(function=function)])

    save_feature_set_to_yaml(feature_set, file_name=feature_set_yaml, directory=working_directory)

    return feature_set_yaml, function_py, requirements_txt if function else feature_set_yaml, None, None


def get_function_code(*, function: FunctionType):
    """
    return: feature.py file
    """
    import_statements = []
    number_of_arguments = function.__code__.co_argcount
    arguments_clause = ",".join(function.__code__.co_varnames[0:number_of_arguments]) if number_of_arguments > 0 else ''
    indented = [""]
    def_signature = ["", f"def {function.__name__}({arguments_clause}):"]
    for line in pysource.code_deparse(function.__code__).text.split("\n"):
        if line.startswith("import"):
            import_statements.append(line)
        else:
            indented.append(f"{4 * ' '}{line}")
    return "\n".join(import_statements + def_signature + indented)


def identify_requirements(*, function: FunctionType):
    """
    return: content of requirements.txt to execute a function
    """
    imported_libraries = function.__code__.co_names
    try:
        from pip._internal.utils.misc import get_installed_distributions
    except ImportError:
        from pip import get_installed_distributions

    return [dist for dist in get_installed_distributions() if dist.project_name in imported_libraries]
