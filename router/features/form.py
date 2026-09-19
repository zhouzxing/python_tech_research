from typing import Annotated
from fastapi import Depends, FastAPI,APIRouter,Form,Request,Response
from fastapi.security import OAuth2PasswordRequestForm

route = APIRouter(prefix="/form",tags=["form"])

@route.post("/token")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # form_data 是解析后的表单对象
    # form_data.username  → OAuth2 规范要求字段名必须是 "username"
    # form_data.password  → OAuth2 规范要求字段名必须是 "password"
    # form_data.grant_type → 密码流程中必须是 "password"
    # form_data.scopes    → 空格分隔的权限列表
    # form_data.client_id / client_secret → 如果客户端选择 client_secret_post
    return {
        "username": form_data.username,
        "password":form_data.password,
        "client_id": form_data.client_id,
        "client_secret":form_data.client_secret,
        "grant_type":form_data.grant_type,
        "scopes":form_data.scopes,
    }


@route.post("/form")
def login(username:str=Form(),password:str=Form()):
    # form_data 是解nt_id / client_secret → 如果客户端选择 client_secret_post
    return {
        "username": username,
        "password":password,
    }

@route.post("/query")
def login(username:str,password:str):
    # form_data 是解nt_id / client_secret → 如果客户端选择 client_secret_post
    return {
        "username": username,
        "password":password,
    }


@route.post("/raw")
async def upload(request: Request):
    raw = await request.body()          # bytes
    text = raw.decode("utf-8")          # 明确解码
    return text
