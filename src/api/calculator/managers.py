import re
from decimal import Decimal
from math import cos, sin, tan
from numbers import Number
from typing import List, Union

from sqlalchemy.orm import Session

from src.api.calculator.db import OperationRecord


class CalcultorStack:
    number_stack: List[Number]
    operation = {
        "+": {"formula": lambda x, y: CalculatorOperation.add(x, y), "pop_two": True},
        "-": {"formula": lambda x, y: CalculatorOperation.sub(x, y), "pop_two": True},
        "*": {"formula": lambda x, y: CalculatorOperation.mult(x, y), "pop_two": True},
        "/": {"formula": lambda x, y: CalculatorOperation.div(x, y), "pop_two": True},
        "cos": {"formula": lambda x, y: CalculatorOperation.cos(x, y), "pop_two": False},
        "sin": {"formula": lambda x, y: CalculatorOperation.sin(x, y), "pop_two": False},
        "tan": {"formula": lambda x, y: CalculatorOperation.tan(x, y), "pop_two": False},
        "%": {"formula": lambda x, y: CalculatorOperation.mod(x, y), "pop_two": True},
    }

    def __init__(self, session: Session):
        self.session = session
        self.number_stack = []

    def calc(self, operation: str) -> Decimal:
        stacks = self.validate_operation(operation)

        for element in stacks:
            try:
                n = Decimal(element)
                self.number_stack.append(n)
            except:
                try:
                    y = self.number_stack.pop()
                    x = self.number_stack.pop() if self.operation[element]["pop_two"] else None
                except IndexError:
                    raise ValueError("Not enough number in operation")

                self.number_stack.append(self.operation[element]["formula"](x, y))

        if len(self.number_stack) >= 2:
            raise ValueError("Not enough operation")

        self.session.add(OperationRecord(operation=operation, result=self.number_stack[0]))
        self.session.commit()

        return self.number_stack[0]

    def validate_operation(self, operation: str) -> List[Union[int, str]]:
        regex = re.compile(r"(\d+\.?\d?|\+|-|\*|\\|cos|sin|tan|%)+")
        result = regex.findall(operation)

        if len(result) != len(operation.split(" ")):
            raise ValueError("Not a valid operation")

        if not result:
            raise ValueError("No valid operation")

        return result


class CalculatorOperation:
    @classmethod
    def add(cls, x: Number, y: Number):
        return x + y

    @classmethod
    def sub(cls, x: Number, y: Number):
        return x - y

    @classmethod
    def mult(cls, x: Number, y: Number):
        return x * y

    @classmethod
    def div(cls, x: Number, y: Number):
        return x / y

    @classmethod
    def mod(cls, x: Number, y: Number):
        return x % y

    @classmethod
    def sin(cls, x: Number, y: Number):
        return Decimal(sin(y))

    @classmethod
    def cos(cls, x: Number, y: Number):
        return Decimal(cos(y))

    @classmethod
    def tan(cls, x: Number, y: Number):
        return Decimal(tan(y))
