from __future__ import annotations
from enum import Enum
from pydantic import BaseModel


class LogicOp(Enum):
    AND = 1
    OR = 2


class Expr(BaseModel):
    operator: LogicOp
    operands: tuple[Expr | Literal | None, Expr | Literal | None]


class Literal(BaseModel):
    code: bool
    content: str


Expr.update_forward_refs()


def toDNF(expr: Expr | Literal) -> list[list[Literal]]:
    # print('in toDNF')
    if isinstance(expr, Literal):
        return [[expr]]
    elif expr.operator == LogicOp.OR:
        return toDNF(expr.operands[0]) + toDNF(expr.operands[1])
    else:
        res = []
        for a in toDNF(expr.operands[0]):
            for b in toDNF(expr.operands[1]):
                res.append(a + b)

        return res
