from functools import singledispatchmethod
from typing import Dict


class QueryFilterExpr:
    def __init__(self, model, query):
        self.model = model
        self.query = query

    @classmethod
    async def apply_filter(cls, model, query, attributes):
        return await cls(model, query).filter(attributes)

    async def filter(self, attributes: Dict):
        for field, value in attributes.items():
            self.query = self._expr(field, value)

        return self.query

    @singledispatchmethod
    def _expr(self, field, value):
        if isinstance(value, str) and "__like" in field:
            field = field.replace('__like', '')
            return self.query.where(getattr(self.model, field).like(f"%{value}%"))

        return self.query.where(getattr(self.model, field) == value)

    @_expr.register
    def _(self, field, value: list):
        return self.query.where(getattr(self.model, field).in_(value))
