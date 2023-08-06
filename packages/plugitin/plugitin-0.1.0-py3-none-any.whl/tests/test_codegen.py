from plugitin.codegen.logic import generate_plugin_code_from_spec_file
from tests.config import PROJECT_1_SPEC_FILE, PROJECT_1_GENERATED_PLUGINS_FILE

GENERATE: bool = False


def test_generate_from_spec():
    result = generate_plugin_code_from_spec_file(str(PROJECT_1_SPEC_FILE))
    if GENERATE:
        PROJECT_1_GENERATED_PLUGINS_FILE.write_text(result)
    else:
        expect_result = PROJECT_1_GENERATED_PLUGINS_FILE.read_text()
        assert result == expect_result
