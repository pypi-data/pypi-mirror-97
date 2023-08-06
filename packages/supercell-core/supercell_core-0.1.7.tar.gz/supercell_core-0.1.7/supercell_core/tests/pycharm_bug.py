from typing import Sequence, Union, Tuple

AType = Union[int, float]
BType = Sequence[AType]
CType = Union[int, Tuple[str, BType]]
c : CType = ("a", ("b", [1]))
def f(c : CType) -> AType:
    try:
        return c[1][0]
    except Exception:
        return 0


