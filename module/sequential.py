import re
from typing import *


class DimensionalFormula:
    """
    N차원 수식 객체입니다.
    """

    def __init__(self, equation: str, coupler: str = "+", unit_length: int = 1, dimension: int = 1):
        """
        unit_length는 1차원(직선)에서 수식이 몇개가 연결되야 하는지를 지정하는 숫자입니다
        1차원을 이상의 객체에서 unit_length를 단위 길이로 사용합니다
        (단위 길이가 없으면 하나의 객체가 아닌 무한한 공간이 되기 때문에 연산이 불가능합니다)
        """
        self.equation = equation
        self.coupler = coupler
        self.dimension = 1
        self.unit_length = unit_length
        self.dimension = dimension
        self.serialized = self._serialization()

    def _serialization(self) -> str:
        """
        기본적으로 N차원 수식 객체의 직렬화는 아레와 같이 진행됩니다
        (equation + coupler) * (unit_length ** dimension)
        (수식 + 연결자) * (단위길이 ** N차원)

        N차원 인자로 음수값이 올 수 있습니다.
        음수 차원에서는 양자(입력된 수식)들이 모두 역수를 취합니다 (양자=최소단위)

        0차원의 경우 입력된 수식을 그대로 반환합니다
        1차원의 경우 입력된 수식을 연결자를 사용해서 unit_length만큼 일직선으로 연결합니다
        """
        if self.dimension != 0:
            return (
                f"({self.equation}){self.coupler}" * (self.unit_length ** self.dimension)
                if self.dimension >= 1
                else f"(1/({self.equation})){self.coupler}" * (self.unit_length ** -self.dimension)
            )[:-1]
        else:
            return self.equation

    @staticmethod
    def convertor(equation: str, n: int) -> Union[int, float]:
        """
        n을 미지수로 하는 방정식 문자열와 n값을 입력받아서 방정식을 풀고 정답을 반환합니다.

        로직: 정규 표현식을 사용해서 명시적으로 생략된 곱셈 기호를 추가하고 미지수 n을 삽입 한 뒤에 eval을 실행합니다
        """
        equation: MutableSequence = list(equation)
        while "n" in equation:
            ndex = equation.index("n")
            if re.match("[0-9]", equation[ndex - 1]) and ndex != 0:
                equation[ndex] = f"*{n}"
        return eval("".join(equation))

    def convert(self, n):
        """인스턴스를 직렬화하여 방정식 연산을 진행합니다"""
        return DimensionalFormula.convertor(self.serialized, n)