from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0)
    stock: int = Field(ge=0, default=0) # 不能写 = 0 因为Field(...)已经是给字段设置默认值和教养规则的地方不能再写第二个 = 0
    tags: list[str] = Field(default_factory=list) # default_factory=list是为了避免可变默认值的问题，确保每个实例都有自己的独立列表

@app.post("/products/")
async def create_product(data: ProductCreate) -> dict[str, object]:
    return {
        'name': data.name,
        'price': data.price,
        'stock': data.stock,
        'tags': data.tags
    }
# 客户缺少name或者把price传承无法转换的字符串或者提交负数库存时，FastAPI会返回422，并指出错误字段和原因