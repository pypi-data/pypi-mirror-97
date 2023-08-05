import shutil
import unittest
from pathlib import Path
from ladm.main.main import LADM
from ladm.main.util.custom_exceptions import LADMError


class LADMTestCase(unittest.TestCase):
    default_output_path = "test-output/LADM"
    default_output_file_name = "LADM-requirements.txt"

    def tearDown(self) -> None:
        if Path(self.default_output_path).exists():
            shutil.rmtree(self.default_output_path.split('/')[0])

    def test_correct_generation(self) -> None:
        dependencies_yml_path = "resources/correct-skill-ladm/skill_with_dependencies.yml"
        ladm = LADM(dependencies_yml_path)
        results = ladm.generate_dependencies_from_file()

        self.assertEqual((["zupline==1.0.0", "tensorblow"],
                          ["libffi-dev", "default-jre=2:1.11-71"],
                          []), results)
        self.assertEqual(ladm.language, "python")
        self.assertEqual(ladm.version, "3.8.8")

    def test_no_dependencies(self) -> None:
        ladm = LADM("resources/correct-skill-ladm/skill_without_dependencies.yml")
        results = ladm.generate_dependencies_from_file()
        self.assertEqual(([], [], []), results)

    def test_empty_dependencies(self) -> None:
        ladm = LADM("resources/correct-skill-ladm/skill_with_dependencies_empty.yml")
        results = ladm.generate_dependencies_from_file()
        self.assertEqual(([], [], []), results)

    def test_system_dependencies_only(self) -> None:
        ladm = LADM("resources/correct-skill-ladm/skill_with_dependencies_system_only.yml")
        results = ladm.generate_dependencies_from_file()
        self.assertEqual(([],
                          ["libffi-dev", "default-jre=2:1.11-71"],
                          []), results)

    def test_libraries_only(self) -> None:
        ladm = LADM("resources/correct-skill-ladm/skill_with_dependencies_libraries_only.yml")
        results = ladm.generate_dependencies_from_file()
        self.assertEqual((["zupline==1.0.0", "tensorblow"],
                          [],
                          []), results)

    def test_correct_data(self) -> None:
        dependencies_yml_path = "resources/correct-skill-ladm/skill_with_dependencies_with_data.yml"
        ladm = LADM(dependencies_yml_path)
        results = ladm.generate_dependencies_from_file()
        self.assertEqual((["zupline==1.0.0", "tensorblow"],
                          ["libffi-dev", "default-jre=2:1.11-71"],
                          ["gaia://tenant/a.txt", "gaia://tenant/test/b.txt"]), results)

    def test_data_only(self) -> None:
        dependencies_yml_path = "resources/correct-skill-ladm/skill_with_dependencies_with_data.yml"
        ladm = LADM(dependencies_yml_path)
        results = ladm.generate_dependencies_from_file(do_language=False, do_system=False, do_data=True)
        self.assertEqual(([],
                          [],
                          ["gaia://tenant/a.txt", "gaia://tenant/test/b.txt"]), results)

    def test_correct_generation_with_specified_language(self) -> None:
        dependencies_yml_path = \
            "resources/correct-skill-ladm/skill_with_dependencies_with_specified_language_python.yml"
        ladm = LADM(dependencies_yml_path)
        results = ladm.generate_dependencies_from_file()

        self.assertEqual((["zupline==1.0.0", "tensorblow"],
                          ["libffi-dev", "default-jre=2:1.11-71"],
                          []), results)
        self.assertEqual(ladm.language, "python")
        self.assertEqual(ladm.version, "3.7")

    def test_planned_but_unsupported_language(self) -> None:
        dependencies_yml_path = \
            "resources/correct-skill-ladm/skill_with_dependencies_with_specified_language_java.yml"
        ladm = LADM(dependencies_yml_path)
        results = ladm.generate_dependencies_from_file()

        self.assertEqual(([],
                          ["libffi-dev", "default-jre=2:1.11-71"],
                          []), results)
        self.assertEqual(ladm.language, "java")
        self.assertEqual(ladm.version, "1.8")

    def test_unsupported_language(self) -> None:
        dependencies_yml_path = \
            "resources/incorrect-skill-ladm/skill_with_dependencies_with_specified_language_unsupported.yml"
        ladm = LADM(dependencies_yml_path)
        self.assertRaises(LADMError, ladm.generate_dependencies_from_file)

    def test_single_dash(self) -> None:
        result = LADM._get_language_and_version("java-1.8")
        self.assertEqual(('java', '1.8'), result)

    def test_multiple_dashes(self) -> None:
        result = LADM._get_language_and_version("java-1.8-jre")
        self.assertEqual(('java', '1.8-jre'), result)
