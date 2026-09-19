from fastapi import APIRouter,Query,Request,Path,Query,Body,Form,File,UploadFile
from pydantic import constr,Field,field_validator,BaseModel, EmailStr, HttpUrl, IPvAnyAddress, conint
from typing import Annotated,Literal

from datetime import date, timedelta
import datetime
from decimal import Decimal
from time import time
from uuid import UUID
import json,os,logging

route = APIRouter(prefix="/wk0915",tags=["wk0915"])

class Login(BaseModel):
    username: str = Field(min_length=3, max_length=20,pattern="^[a-zA-Z]")
    passwd: str = Field(min_length=6, max_length=20)
    is_ok: bool

@route.post("/login/{session_id}")
def login(session_id:str = Path(min_length=10, pattern="^[a-zA-Z0-9]+$"),
          usertype:int| None = None,
          login:Login =Form()):
    d = {
        "username":login.username,
        "usertype":usertype,
        "is_ok":login.is_ok
    }
    # lg = Login.model_validate(json.loads())
    # return {
    #     "login": d
    # }
    return d


@route.get("/user/{user_id}")
def user(user_id: int = Path(gt=1)):
    return user_id

class Product(BaseModel):
    pname: str = Field(min_length=2,max_length=50)
    price: int = Field(gt=0)
    stock: int = Field(gt=0)
    type: str = Field(min_length=1) # todo not blank?

@route.post("/product")
def product(product:Product):
    return product

stu = teac = []

class Student(BaseModel):
    sid: int | None = None
    sname: str
    age: int | None = Field(default=None, ge=0)
    sex: Literal['男','女']
    hobby: set[str]
    create_date: datetime.datetime = Field(default_factory=datetime.datetime.now)


@route.post("/student")
def student(student: Student):
    stu.append(student)
    return student


@route.get('/student')
def student(sname:str|None = Query(default=None),
            sex:str|None = Query(default=None), # todo Literal validate
            age:int|None = Query(default=None, ge=0, le=120)
            ):

    # res = [s for s in stu if s['sname'] == sname]
    if sname == None and sex == None and age == None : return stu
    if sname != None and sex != None and age != None: return [s for s in stu if (sname != None and s.sname == sname)
            and (sex != None and s.sex == sex)
            and (age != None and s.age == age)]
    if sname != None and sex != None : return [s for s in stu if (sname != None and s.sname == sname)
            and (sex != None and s.sex == sex)]
    if sname != None and age != None : return [s for s in stu if (sname != None and s.sname == sname)
            and (age != None and s.age == age)]
    if sex != None and age != None : return [s for s in stu if (sex != None and s.sex == sex)
            and (age != None and s.age == age)]
    if sex != None : return [s for s in stu if s.sex == sex]
    if sname != None : return [s for s in stu if s.sname == sname]
    if age != None : return [s for s in stu if s.age == age]


class Teacher(BaseModel):
    name: str|None
    salary: float
    hiredate: date
    stu: list[Student]


@route.post("/teacher")
def teacher(teacher:Teacher):
    teac.append(teacher)
    return teac

import random
@route.post("/upload")
def upload(files:list[bytes]= File()):
    # names = random.choices(['001','002','geeker'],len(files)) # todo duplacate names
    # names = random.choices(range(len(files)),len(files)) # set fix!
    i = 0 # order name
    saved = []
    for file in files:
        try:
            # filepath = os.path.join(os.getcwd(), i)
            filepath = os.getcwd() + "/router/workhome/" +  str(i)
            with open(filepath,'wb') as f:
                f.write(file)
            i += 1
            saved.append(filepath)
        except Exception: # exception too large!
            pass

    return saved


@route.post("/upload_file")
async def upload(files:list[UploadFile] = File()):
    saved = []
    for file in files:
        path = os.getcwd() + "/router/workhome/" + file.filename
        data = await file.read()

        try:
            with open(path,'w',encoding='utf-8') as f:
                f.write(data)
            saved.append(path)
        except Exception:
            pass

    return saved
