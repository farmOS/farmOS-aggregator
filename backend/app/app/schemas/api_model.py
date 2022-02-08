from pydantic import BaseConfig, BaseModel


# Shared properties
class APIModel(BaseModel):
    class Config(BaseConfig):
        orm_mode = True
        allow_population_by_field_name = True
