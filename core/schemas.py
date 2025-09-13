from pydantic import BaseModel


class BasePersonSchema(BaseModel):
    name: str

class PersonCreateSchema(BasePersonSchema):
    pass

class PersonResponseSchema(BaseModel):
    id: int

class PersonUpdateSchema(BasePersonSchema):
    pass
