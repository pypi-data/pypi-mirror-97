import os
import pytest
from .. import jenkins

DATADIR = os.path.join(os.path.dirname(__file__), "data")
INPUT_FILE = os.path.join(DATADIR, "jenkins.log")


@pytest.fixture(scope="module")
def records():
    return jenkins.parse_log(INPUT_FILE)


@pytest.fixture(scope="module")
def master_log(records):
    return log_combine(records, "type", "masterLog")


@pytest.fixture(scope="module")
def hello_stage(records):
    return log_search(records, "name", "hello")


def log_search(data, key, by_value=""):
    result = list()
    for record in data:
        for k, v in record.items():
            if not by_value:
                v = ""
            if key == k and v == by_value:
                result.append(record)
    return result


def log_combine(data, key, key_value):
    result = ""
    for record in data:
        for k, v in record.items():
            if not key_value:
                v = ""
            if key == k and v == key_value:
                result += record["data"]
    return result


def test_pipeline_specification():
    assert jenkins.PIPELINE_MARKER == "[Pipeline]"
    assert jenkins.PIPELINE_BLOCK_START == '{'
    assert jenkins.PIPELINE_BLOCK_END == '}'
    assert jenkins.PIPELINE_BLOCK_START_NOTE == '('
    assert jenkins.PIPELINE_BLOCK_START_NOTE_END == ')'
    assert jenkins.PIPELINE_BLOCK_END_NOTE == "//"


@pytest.mark.parametrize("test_input,token,expected,test_args", [
    # consume_token(s, token, l_trunc=0, r_trunc=0, strip_leading=True)
    ("^See you later alligator^", "^", "See you later alligator", [0, 1, True]),
    ("###     In a while crocodile", "###", "In a while crocodile", [0, 0, True]),
    ("Bye bye butterfly", "Bye bye ", "utter", [1, 3, False]),
    ("[Pipeline] value", "[Pipeline]", "value", [0, 0, True]),
    ("[Pipeline] { (name)", "{", "(name)", [0, 0, True]),
    ("[Pipeline] { (name)", "(", "name", [0, 1, True]),
])
def test_consume_token(test_input, token, expected, test_args):
    assert jenkins.consume_token(test_input, token, *test_args) == expected


def test_parse_log_empty_file():
    assert jenkins.parse_log(os.devnull) == list()


def test_parse_log_path_failure():
    with pytest.raises(FileNotFoundError):
        assert jenkins.parse_log("1234unlikely_to_exist4321.log")


def test_parse_log_master_log_keys(records):
    log = log_search(records, "type", "masterLog")
    assert len(log[0].keys()) == len(["name", "type", "depth", "line", "data"])


def test_parse_log_master_log_genesis(records):
    log = log_search(records, "type", "masterLog")
    assert log
    assert log[0]["name"] == "master"
    assert log[0]["type"] == "masterLog"
    assert log[0]["depth"] == 0  # First record, lowest depth
    assert log[0]["line"] == 0
    assert log[0]["data"]


def test_parse_log_master_log_complete(master_log):
    """Verify the entire master log is present
    """
    assert master_log.startswith("Started by")
    assert master_log.endswith("SUCCESS\n")


def test_parse_log_hello_stage_length(hello_stage):
    assert len(hello_stage) == 2


def test_parse_log_hello_stage_types(hello_stage):
    assert hello_stage[0]["type"] == "stage"
    assert hello_stage[1]["type"] == "sh"


def test_parse_log_hello_stage_depths(hello_stage):
    assert len(hello_stage) == 2
    assert hello_stage[0]["depth"] == 2
    assert hello_stage[1]["depth"] == 2


def test_parse_log_hello_contents(hello_stage):
    assert len(hello_stage[1]["data"].splitlines()) == 30

