import os

from src.main import CallMapper


class TestCallMapper():
    fixtures_folder = "test/fixtures"

    def test_find_function_call(self):
        file_fixture = os.path.join(self.fixtures_folder, "class_definition")
        mapper = CallMapper()
        mapper.process(file_fixture)

        assert mapper.calls["TestClass"] is not None
