from fastapi import APIRouter, Request,Header,Cookie

from pydantic import constr,Field, field_validator
from typing import Annotated
from fastapi import Path,Query, Form,File,UploadFile

from router.features import method

route = APIRouter(prefix="/mimetypes",tags=["mimetypes"])

from uuid import UUID
from pydantic import BaseModel, EmailStr, HttpUrl, IPvAnyAddress, conint

@route.get("/any_types")
def any_types(email: EmailStr
        , url: HttpUrl = Query()
        , ipv4: IPvAnyAddress | None=None
        , ipv6: IPvAnyAddress | None=None
        , uuid: UUID | None=None
        # , date: date
        # , datetime: datetime
        # , time: time
        # , timedelta: timedelta
        # , decimal: Decimal
        # , json: Json
        # , secret: SecretStr
        # , secret_bytes: SecretBytes
        # , conint: conint(gt=0, lt=100)
        ):
    return {
        "email": email,
        "url": url,
        "ipv4": ipv4,
        "ipv6": ipv6,
        "uuid": uuid
    }
    pass


'''
    form/ file
'''

@route.post('/login')
def login(name:str = Form()):
    return name


@route.post('/upload')
def upload(file_name:bytes = File()):
    return file_name

@route.post("/upload_raw")
async def upload(request: Request):
    return await request.body()

@route.post('/upload_files')
def upload(file_name:list[bytes] = File()):
    return file_name


@route.post('/upload_files_annotated')
def upload(file_name:Annotated[list[bytes],File()]):
    return file_name


@route.post('/upload_uploadfiles')
def upload(files:list[UploadFile] = File()):
    return [f.filename for f in files]

@route.post('/upload_file')
def upload(file:UploadFile):
    return file


@route.post('/upload_str')
def upload(file_name:str = File()):
    return file_name


'''
    validator app
'''
@route.get("/validate_con")
def web(
    age: conint(ge=0, lt=150),
    name: constr(min_length=1, max_length=50),
):
    return {
        "age":age,
        "name":name
    }

@route.get("/validate_field")
def web(
    num:int = Query(Field(10,le=100,ge=8))
):
    return num


@route.get("/validate_annotated")
def web(
    age: Annotated[int, Field(ge=0, lt=150)],
    name: Annotated[str, Field(min_length=1, max_length=50)],
):
    return {
        "age": age,
        "name": name
    }


@route.get("/validated_annotated_query")
async def get(option: Annotated[str|None, Query(max_length=10)] = None):
    return option

@route.get("/validated_annotated_path/{option}")
async def get(option: Annotated[str|None, Path(max_length=10)]):
    return option

'''
    
'''
class ValidatorSelf(BaseModel):
    email: EmailStr
    age: int

    @field_validator("age")
    def age_must_be_realistic(cls, v):
        if v > 150:
            raise ValueError("age too large")
        return v


@route.post("/validated_self")
async def post(vs: ValidatorSelf):
    return vs


@route.get("/request")
def request(res: Request):
    return res.headers.raw


from fastapi import Request
# from method import Item
# @route.api_route("/anything/{item}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def anything(request: Request):
    return {
        "method": request.method,
        "path_params": request.path_params,
        "query": dict(request.query_params),
        "headers": dict(request.headers),
        "cookies": request.cookies,
        "body": (await request.body()).decode("utf-8", "ignore"),
    }

@route.post("/anything_params/{item_id}")
async def anything_params(
    item_id: Annotated[int, Path()],
    dry_run: Annotated[bool, Query()] = False,
    x_token: Annotated[str, Header()] = None,
    session: Annotated[str | None, Cookie()] = None,
    # item: Item | None = None,                      # JSON body & multi-part cannot occured same time!
    item: str = Form(),
    avatar: UploadFile | None = File(None)):

    import json
    item_obj = method.Item.model_validate(json.loads(item))
    return {
        "item_id": item_id,
        "dry_run": dry_run,
        "x_token": x_token,
        "session": session,
        "item": json.dumps(item_obj),
        "avatar": avatar
    }


@route.get("/proxy")
def get(request: Request):
    path = request.url_for('sn',path = 'head.png')
    return path


# 定义请求体模型
class UserRequest(BaseModel):
    username:str
    passwd:str

class UserResponse(BaseModel):
    code:int = 200
    detail:str = 'ok'
    totals:int = 0
    username:str

@route.post('/user',response_model=UserResponse)
def user(u:UserRequest):
    # return UserResponse(username=u.username)
    return u  # 等价于 return UserResponse(username=u.username)

@route.post('/users')
def users(u:list[UserRequest]):
    x = [_.username for _ in u]
    return UserResponse(code='200',totals = len(x),username=x[0])


@route.post('/users_list')
def users(u:list[str]):
    return UserResponse(code='200',totals = len(u),username=u[0])

@route.get('/url_for/{id}',name='url_for')
def url_for(id:int):
    return id

@route.get('/test_url_for')
def url_for(res:Request):
    url = res.url_for('url_for',id = 123)
    return {"url":str(url)}


from fastapi import status,Response


@route.post("/status_code", status_code=status.HTTP_201_CREATED)
async def status_code(name:str):
    return name

# 或者动态设置
@route.post("/response")
async def response(name: str, response: Response):
    response.status_code = 201
    response.headers["X-Custom"] = "value"
    return name


