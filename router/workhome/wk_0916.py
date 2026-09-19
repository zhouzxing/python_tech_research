from fastapi import APIRouter,Query,Request,Path,Query,Body,Form,File,UploadFile,HTTPException
from pydantic import constr,Field,field_validator,BaseModel, EmailStr, HttpUrl, IPvAnyAddress, conint
from typing import Annotated,Literal

from datetime import date, timedelta
import datetime
from decimal import Decimal
from time import time
from uuid import UUID
import json,os,logging
from hashlib import md5  # ①导入md5加密
from libplus.logpluslplus import Log

route = APIRouter(prefix="/wk0916",tags=["wk0916"])

users = []

@route.post("/registe")
def registe(username:str, passwd:str):
    users.append({"username":username,"passwd":passwd})
    return users


@route.post("upload")
async def upload(file:UploadFile,res:Request):
    data = await file.read()
    if "洗脚" in data:
        md = md5()
        md.update(("sensitive_word" + str(range(10))).encode())
        file_name = md.hexdigest()
        with open(file_name,'w',encoding='utf-8') as f:
            f.write(data)
            log = Log('local_log','warning')
            log.set_file_logger("logfile.log")
            log.warning("洗脚"+res.client.host)
    else:
        log = Log('local_log', 'info')
        log.get_file_logger("logfile.log")
        log.warning("no洗脚" + res.client.host)
        return "该文件没有敏感词汇"


stu =  [{"sname":"gk","classid":"java"},
        {"sname":"yb","classid":"python"}]


@route.get("/student")
def student(name:str):
    for s in stu:
        if s["sname"] == name:
            return s
        raise HTTPException(status_code=404,detail="学生不存在")

# app.mount(path="/staticfile",app=StaticFiles(directory="d://tmp"),name="sn")

class Response(BaseModel):
    code: int = 200
    detail: str = "添加成功"
    total: int = 1
    sname: str
    classid: int


class Request(BaseModel):
    sname: str
    classid: int

@route.get("/student_model",response_model=Response)
def student_model(s:Request):
    for s0 in stu:
        if s0["sname"] == s.sname:
            raise HTTPException(status_code=404,detail="学生不存在")
    return s


@route.post("/student_model_post",response_model=Response)
def student_model_post(s:Request):
    stu.append({"sname":s.sname,"classid":s.classid})
    # suc / fail
    flag = True
    if flag : return Response(code = '200',sname=s.sname,classid = s.classid)
    else :return Response(code = '500',sname=s.sname,classid = s.classid)




