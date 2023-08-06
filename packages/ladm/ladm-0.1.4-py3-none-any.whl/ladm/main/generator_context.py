from ladm.main.generator_strategy import GeneratorStrategy
from ladm.main.util.types import DependenciesOutput, DependenciesInput


class GeneratorContext:
    def __init__(self, strategy: GeneratorStrategy = None):
        self._strategy: GeneratorStrategy = strategy

    @property
    def strategy(self) -> GeneratorStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: GeneratorStrategy) -> None:
        self._strategy = strategy

    def execute_strategy(self, dependencies: DependenciesInput) -> DependenciesOutput:
        return self._strategy.generate(dependencies)
