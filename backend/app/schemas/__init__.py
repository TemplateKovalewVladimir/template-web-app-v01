from pydantic import BaseModel as BaseModelPydantic
from pydantic import ConfigDict


class BaseModel(BaseModelPydantic):
    model_config = ConfigDict(str_strip_whitespace=True)
