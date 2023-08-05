import logging
import yaml
from typing import Tuple

from ladm.main.generator_context import GeneratorContext
from ladm.main.generator_strategy import LanguageGeneratorStrategy, SystemGeneratorStrategy, DataGeneratorStrategy
from ladm.main.util.custom_exceptions import LADMError
from ladm.main.util.types import LanguageDependenciesOutput, SystemDependenciesOutput, DataDependenciesOutput, \
    YamlContent


class LADM:
    logger = logging.getLogger('LADM')

    def __init__(self, input_filepath: str) -> None:
        """
        :param input_filepath: File path and name of the skill.yml file containing the dependencies
                               (Or any other file containing dependencies in the correct format)
        """
        self._input_filepath: str = input_filepath
        self._fallback_language: str = "python-3.8.8"
        self._language: str = ""
        self._version: str = ""

    @property
    def language(self):
        if not self._language:
            self.logger.warning("Language not set, generation must be run first")
        return self._language

    @property
    def version(self):
        if not self._version:
            self.logger.warning("Version not set, generation must be run first")
        return self._version

    def generate_dependencies_from_file(self,
                                        do_language: bool = True,
                                        do_system: bool = True,
                                        do_data: bool = True) -> Tuple[LanguageDependenciesOutput,
                                                                       SystemDependenciesOutput,
                                                                       DataDependenciesOutput]:
        """
        Main method to call from this class. Generates three lists.
        :param do_language: generate language libraries dependencies
        :param do_system: generate system dependencies
        :param do_data: generate data dependencies
        :return: Language library dependencies, system-level dependencies, data dependencies
        """
        self.logger.info(f"Generating with args{list(vars().items())[1:]}")

        dependencies_yaml = self._read_yaml()

        self._set_language_and_version(dependencies_yaml)

        if 'dependencies' not in dependencies_yaml:
            self.logger.warning("'dependencies' is not specified in skill.yml.")
            self.logger.warning("No additional dependencies will be installed.")
            return [], [], []

        language_libraries = dependencies_yaml['dependencies'].get('libraries')
        system_dependencies = dependencies_yaml['dependencies'].get('system')
        data = dependencies_yaml['dependencies'].get('data')

        language_libraries_results: LanguageDependenciesOutput = []
        system_dependencies_results: SystemDependenciesOutput = []
        data_results: DataDependenciesOutput = []

        context = GeneratorContext()
        if do_language:
            context.strategy = LanguageGeneratorStrategy(self._language)
            language_libraries_results = context.execute_strategy(language_libraries)
        if do_system:
            context.strategy = SystemGeneratorStrategy()
            system_dependencies_results = context.execute_strategy(system_dependencies)
        if do_data:
            context.strategy = DataGeneratorStrategy()
            data_results = context.execute_strategy(data)

        return language_libraries_results, system_dependencies_results, data_results

    def _read_yaml(self) -> YamlContent:
        with open(self._input_filepath, 'r') as stream:
            try:
                dependencies_yaml = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                self.logger.error(exc)
                raise LADMError(f"The supplied YAML in {self._input_filepath} cannot be parsed.")
            return dependencies_yaml

    def _set_language_and_version(self, dependencies_yaml: YamlContent) -> None:
        language_and_version = dependencies_yaml.get('language')
        if not language_and_version:
            # TODO: Error and abort or is fallback fine?
            self.logger.warning(
                f"No language specified in skill.yml - using {self._fallback_language} as fallback skill language.")
            language_and_version = self._fallback_language
        self._language, self._version = self._get_language_and_version(language_and_version)

    @staticmethod
    def _get_language_and_version(language_and_version: str) -> Tuple[str, str]:
        lv = language_and_version.split('-')
        return lv[0].lower(), '-'.join(lv[1:])
