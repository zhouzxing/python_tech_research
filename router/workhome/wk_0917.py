from fastapi import APIRouter,Query,Request,Path,Query,Body,Form,File,UploadFile,HTTPException,Response
from pydantic import constr,Field,field_validator,BaseModel, EmailStr, HttpUrl, IPvAnyAddress, conint,model_validator
from typing import Annotated,Literal

from datetime import date, timedelta
import datetime
from decimal import Decimal
from time import time
from uuid import UUID
import json,os,logging
from hashlib import md5  # ①导入md5加密
from libplus.logpluslplus import Log

route = APIRouter(prefix="/wk0917",tags=["wk0917"])

products = [{"name":"a","price":123.9,"stock":2},{"name":"a","price":123.9,"stock":2},{"name":"a","price":123.9,"stock":2},]
class Product(BaseModel):
    name:str
    price:float
    stock: int

    @model_validator(mode='after') #
    def check(self):
        pnames = [p['name'] for p in products]
        if self.name in pnames: raise HTTPException(status_code="409",detail="name duplicate")
        return self

@route.get("/product")
def product(name:str):
    for p in products:
        if name == p["name"]: return p
    else: return Response(status_code="409",content="not find!")

@route.post("/product")
def product(p: Product):
    products.append(p.model_dump())
    return p


orders = []
@route.get("/order")
def order(name:str):
    return name

@route.post("/order")
def order(name:str):
    orders.append(name)
    return name


