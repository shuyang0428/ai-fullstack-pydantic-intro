from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator, model_validator

app = FastAPI()


# Nested Models 嵌套模型
class Supplier(BaseModel):
    name: str
    contact_email: Optional[str] = None

class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0)
    supplier: Supplier
    tags: list[str] = Field(default_factory=list)

# The corresponding JSON is as follows:
# {
#     "name": "Product A",
#     "price": 10.99,
#     "supplier": {
#         "name": "Supplier X",
#         "contact_email": "supplier@example.com"
#     },
#     "tags": ["tag1", "tag2"]
# }


# Field Validation and Model Validation 字段验证和模型校验
class Discount(BaseModel):
    original_price: float = Field(gt=0)
    sale_price: float = Field(gt=0)
    code: str

    @field_validator("code")
    @classmethod
    def normalize_code(cls, value: str) -> str:
        value = value.strip().upper()
        if not value:
            raise ValueError("Discount code cannot be empty")
        return value

    @model_validator(mode='after')
    def check_price(self) -> 'Discount':
        if self.sale_price >= self.original_price:
            raise ValueError("Sale price must be less than original price")
        return self
# 校验函数适合保证数据本身成立，不适合查询数据库或调用外部接口。
# 名称是否重复、用户是否存在这类判断依赖于外部状态，应放在业务服务中处理。
