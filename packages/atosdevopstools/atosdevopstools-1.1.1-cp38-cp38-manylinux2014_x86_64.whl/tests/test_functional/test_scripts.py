from pathlib import Path
import pytest

from atosdevopstools.pylint_wrapper import PylintWrapper


def test_pylint_report_validation_not_ok():
    file = Path(__file__).parent / Path('resources', 'pylint_report_with_errors.txt')
    pylint_wrapper = PylintWrapper(file)
    with pytest.raises(ValueError):
        pylint_wrapper.validate_pylint_report()


def test_pylint_report_validation_ok():
    file = Path(__file__).parent / Path('resources', 'pylint_report_no_errors.txt')
    expected_qa_value = '6.33'
    pylint_wrapper = PylintWrapper(file)
    qa_value = pylint_wrapper.validate_pylint_report()

    assert qa_value == expected_qa_value
