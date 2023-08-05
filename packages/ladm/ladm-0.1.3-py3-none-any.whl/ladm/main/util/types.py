from typing import List, Union, Hashable, Any, Dict

YamlContent = Union[Dict[Hashable, Any], List, None]

LanguageDependenciesInput = List[List[str]]
SystemDependenciesInput = List[List[str]]
DataDependenciesInput = List[str]
DependenciesInput = Union[LanguageDependenciesInput, SystemDependenciesInput, DataDependenciesInput]

LanguageDependenciesOutput = List[str]
SystemDependenciesOutput = List[str]
DataDependenciesOutput = List[str]
DependenciesOutput = Union[LanguageDependenciesOutput, SystemDependenciesOutput, DataDependenciesOutput]
