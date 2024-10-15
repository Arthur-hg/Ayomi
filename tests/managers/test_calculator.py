from decimal import Decimal

from pytest import mark, raises

from src.api.calculator.db import OperationRecord
from src.api.calculator.managers import CalcultorStack


class TestCalcultorStack:
    @staticmethod
    def _assert_equals_with_quantize(first_value: Decimal, second_value: Decimal) -> None:
        decimal_cases = Decimal(".000000000000000")
        assert Decimal(first_value).quantize(decimal_cases) == Decimal(second_value).quantize(decimal_cases)

    @mark.parametrize(
        "operation, expected_result, exception_raised",
        [
            ("3 5 4 7 + - * cos sin", ["3", "5", "4", "7", "+", "-", "*", "cos", "sin"], None),
            ("3 5 4 7 + - * fhfzefez cos sin", None, ValueError),
            ("fezf zefze ezf zf ze", None, ValueError),
        ],
    )
    def test_validate_operation(self, session, operation, expected_result, exception_raised):
        if exception_raised:
            with raises(exception_raised):
                CalcultorStack(session).validate_operation(operation)
            return

        assert CalcultorStack(session).validate_operation(operation) == expected_result

    @mark.parametrize(
        "operation, expected_result, exception_raised",
        [
            ("3 5 4 7 + - *", Decimal("-18"), None),
            ("3 5 4 7 + - * sin", Decimal("0.750987246771676"), None),
            # Not enough number
            ("3 5 4 + - * sin", None, ValueError),
            # Not enough operation
            ("3 5 4 + sin", None, ValueError),
        ],
    )
    def test_calc(self, session, operation, expected_result, exception_raised):
        if exception_raised:
            with raises(exception_raised):
                CalcultorStack(session).calc(operation)
            return

        self._assert_equals_with_quantize(CalcultorStack(session).calc(operation), expected_result)
        recorded_operation = OperationRecord.get_all(session)

        assert len(recorded_operation) == 1
        assert recorded_operation[0].operation == operation
        self._assert_equals_with_quantize(recorded_operation[0].result, expected_result)


# Missing FastAPI request test, which could have been done with the client fixture.
