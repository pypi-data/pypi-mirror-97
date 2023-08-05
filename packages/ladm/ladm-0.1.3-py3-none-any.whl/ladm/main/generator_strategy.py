import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Union

from ladm.main.util.custom_exceptions import LADMError
from ladm.main.util.types import DependenciesOutput, DependenciesInput, SystemDependenciesOutput, \
    LanguageDependenciesOutput, DataDependenciesOutput, SystemDependenciesInput, LanguageDependenciesInput, \
    DataDependenciesInput


class GeneratorStrategy(ABC):
    @abstractmethod
    def generate(self, dependencies: DependenciesInput) -> DependenciesOutput:
        pass

    @staticmethod
    def convert_yaml_deps_to_dict(deps: Union[LanguageDependenciesInput,
                                              SystemDependenciesInput]) -> Dict[str, Optional[str]]:
        """
        Goes through the list of dependencies where each entry is a list containing a dependency name and a possible
        version as a second entry, converts it to a dict where the keys are the dependency names and possible
        values are the version

        :param deps: Parsed YAML input of either the system or language dependencies part of dependencies in skill.yml
        :return: dict where keys are names of packages or libraries, and optional values are versions
        """
        return {dep[0]: dep[1] if (len(dep) > 1) else None for dep in deps}

    @staticmethod
    def check_if_dependencies_empty(dependencies: DependenciesInput) -> bool:
        return dependencies == [] or dependencies is None


class SystemGeneratorStrategy(GeneratorStrategy):
    def generate(self, dependencies: SystemDependenciesInput) -> SystemDependenciesOutput:
        if self.check_if_dependencies_empty(dependencies):
            return []

        # Parse dependencies and add them to list
        deps_and_versions: dict[str, Optional[str]] = self.convert_yaml_deps_to_dict(dependencies)
        return [f"{k}={v}" if v else k for k, v in deps_and_versions.items()]


class LanguageGeneratorStrategy(GeneratorStrategy):
    def __init__(self, language: str = None) -> None:
        self._language: str = language

    def generate(self, dependencies: LanguageDependenciesInput) -> LanguageDependenciesOutput:
        """
        :return: list of language libraries as strings possibly including version numbers
        """
        if self.check_if_dependencies_empty(dependencies):
            return []

        language_libraries_generators = {
            "python": PythonGeneratorStrategy(),
            "java": JavaGeneratorStrategy()
        }

        if self._language in language_libraries_generators:
            return language_libraries_generators[self._language].generate(dependencies)
        else:
            raise LADMError(f"Language {self._language} is not supported.")


class PythonGeneratorStrategy(LanguageGeneratorStrategy):
    def generate(self, dependencies: LanguageDependenciesInput) -> LanguageDependenciesOutput:
        """
        :return: list of Python libraries as strings possibly including version numbers
        """
        # Parse libraries and add them to list
        libs_and_versions: Dict[str, Optional[str]] = self.convert_yaml_deps_to_dict(dependencies)

        # Python requirements txt needs == instead of single =.
        # (Others too, but that's not implemented) https://www.python.org/dev/peps/pep-0440/#version-specifiers
        return [f"{k}=={v}" if v else k for k, v in libs_and_versions.items()]


class JavaGeneratorStrategy(LanguageGeneratorStrategy):
    logger = logging.getLogger('JavaGeneratorStrategy')

    def generate(self, dependencies: LanguageDependenciesInput) -> LanguageDependenciesOutput:
        """
        :return: list of Java libraries as strings possibly including version numbers
        """
        self.logger.warning("LADM for Java/Gradle libraries is not yet implemented.")
        self.logger.warning(f"Language libraries {dependencies} are discarded from the process.")
        return []


class DataGeneratorStrategy(GeneratorStrategy):
    def generate(self, dependencies: DataDependenciesInput) -> DataDependenciesOutput:
        """
        :return: list of data as strings in GAIA URI format
        """
        if self.check_if_dependencies_empty(dependencies):
            return []

        return dependencies
