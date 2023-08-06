from typing import Any

from faunadb import query as q
from pydantic import BaseModel

class FaunaEasyBaseModel:
    collection: str
    pydantic_basemodel: Any

    def __init__(self, collection: str, pydantic_basemodel: Any) -> None:
        self.collection = collection
        if not issubclass(pydantic_basemodel, BaseModel):
            raise Exception(
                f'pydantic_basemodel must be a subclass of pydantic.BaseModel'
            )

        self.pydantic_basemodel = pydantic_basemodel

    def create(self, doc: dict, id: str = None) -> q._Expr:
        self.pydantic_basemodel(**doc)
        return q.create(
            q.ref(
                q.collection(
                    self.collection,
                ),
                id=id
            ) if id != None else q.collection(
                self.collection,
            ),
            { 'data': doc },
        ),
    
    def delete(self, id: str) -> q._Expr:
        return q.delete(
            q.ref(
                q.collection(
                    self.collection,
                ),
                id=id
            )
        ),

    
    def update(self, doc: dict, id: str) -> q._Expr:
        self.pydantic_basemodel(**doc)
        return q.update(
            q.ref(
                q.collection(
                        self.collection,
                ),
                id=id
            ),
            { 'data': doc },
        ),

    

    def find_by_id(self, id: str) -> q._Expr:
        return q.get(
            q.ref(
                q.collection(self.collection),
                id,
            )
        )
