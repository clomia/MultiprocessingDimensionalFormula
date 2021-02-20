import os
from typing import *
from concurrent.futures import ThreadPoolExecutor
from itertools import zip_longest, repeat
from functools import reduce
from .sequential import DimensionalFormula


class DecompositionError(Exception):
    def __init__(self):
        super().__init__("수식객체를 분해할 수 없습니다. 객체가 0차원이기 때문일 수 있습니다")


class MultiprocessingDimensionalFormula(DimensionalFormula):
    """
    병렬 연산을 지원하는 N차원 수식 객체입니다
    컴퓨터의 CPU갯수와 인스턴스의 모양에 따라 CPU코어를 최대한 사용하는 병렬 연산을 수행할 수 있습니다.
    ! multiprocessing_convert메서드를 사용해야 합니다
    """

    def __init__(self, equation, coupler="+", unit_length=1, dimension=1):
        super().__init__(equation, coupler, unit_length, dimension)
        self.cpu_count = os.cpu_count()
        self.multiple_serialized: Iterator = self._serialization_decomposition()

    def _serialization_decomposition(self) -> Iterator:
        """
        직렬화 함수의 문서 _serialization.__doc__ 를 참고하세요.
        사용자 컴퓨터 CPU코어의 갯수를 참조하여 병렬 연산을 최적화 하기 위한 제너레이터입니다.
        반환되는 이터레이터는 각 CPU 코어에 고르게 할당하기 위해서 수식을 분해한 것입니다.
        """
        if self.dimension != 0:
            if self.dimension >= 1:
                unit = f"({self.equation}){self.coupler}"
                serial_count: int = self.unit_length ** self.dimension
            else:
                unit = f"(1/({self.equation})){self.coupler}"
                serial_count: int = self.unit_length ** -self.dimension
        else:
            raise DecompositionError
        default_quantum_count, remainder_quantum_count = divmod(serial_count, self.cpu_count)
        if default_quantum_count:
            yield from (
                (unit * default_quantum_count + unit * is_remainder)[:-1]
                for _, is_remainder in zip_longest(
                    range(self.cpu_count), repeat(1, remainder_quantum_count), fillvalue=0
                )
            )
        else:
            yield from (unit[:-1] for _ in range(remainder_quantum_count))

    def multiprocessing_convert(self, n: Union[int, float]) -> Union[int, float]:
        """
        미지수 n을 입력받아서 방정식 연산을 합니다. CPU를 병렬로 사용해서 진행합니다.
        """
        func = DimensionalFormula.convertor
        pool = ThreadPoolExecutor(max_workers=self.cpu_count)
        fanout = pool.map(func, self.multiple_serialized, repeat(n, self.cpu_count))
        fanin: str = reduce(lambda acc, cur: acc + (self.coupler + cur), map(str, fanout))
        return eval(fanin)
