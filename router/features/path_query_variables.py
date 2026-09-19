# from idlelib.query import Query
from typing import Optional
from fastapi import APIRouter,Query
from pydantic import BaseModel
import re

from enum import Enum

route = APIRouter(prefix="/path_query_variables",tags=["path_query_variables"])

stu = [{"sid":'001','name':'gk','age':18,'address':'dd_abc_lg_', 'sex':'male'},
       {"sid":'002','name':'gk2','age':19},
       {"sid":'003','name':'gk3','age':20}]

class Sex(str,Enum):
    MALE = 1
    FEMAIL = 2,
    TRANS = 3

    maile = '男'
    femail = '女',
    trans = '跨性别'



@route.get("/{sid}")
def get(sid: str):
    for s in stu:
        if s['sid'] == sid: return s
    return None


@route.get("/")
def get(age_min: int | None = None, age_max: int| None=None):
    lst = []
    for s in stu:
        if age_min <= s['age'] <= age_max: lst.append(s)
    return lst

# todo: not support int|None? <0.141.1
'''
BP:
    - Optional[str,None]
    - str | None
    - str | None = None
     
'''
@route.get("/validate")
def get(age_min: int=Query(default=0, ge=0,le=100),
        age_max: int=Query(default=0, ge=0,le=100),
        sname:str=Query(default='',min_length=2,max_length=10),
        address:str=Query(pattern=".*lg.*"),
        sex:Sex=Query()
        ):

    return [x for x in stu if age_min <= x['age'] <= age_max and x['name']==sname and re.search(address,x['address'])]



# path
@route.get("/good/{path:path}")
def get_path(path: str):
    return path

@route.get("/bad/{path}")
def get_path(path: str):
    return path

class Object(BaseModel):
    id:int|None = None
    name: str|None = None
    price: float|None = None


@route.post("/model_dump_extraset")
def model_dump_extraset(obj: Object):
    return obj.model_dump(exclude_unset=True)


@route.get("/model_dump_extraset")
def model_dump_extraset(obj: Object):
    return obj.model_dump(exclude_unset=True)


