import fastapi
from fastapi import APIRouter,Query,Path,Header,Cookie,File,UploadFile,Form,Request,Response,Depends
from pydantic import BaseModel,Field
from typing import Union,Optional,Literal,Annotated


route = APIRouter(prefix="/methods",tags=["methods"])

'''
    Filed & Query : 做param validate!
'''
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class StuUpdate(BaseModel):
    id : int|None = None
    name:str|None  = None
    age:int = None
    sex:Literal['男','女']|None = None
    address:str|None = None


@route.put('/model_dump/{sid}')
def model_dump(sid:int,s:StuUpdate):
    d = s.model_dump(exclude_unset=True)
    return d

@route.post("/model_dump/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

@route.put("/body_path/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump()}

@route.put("/body_path_query/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result


class Body(BaseModel):
    id: int = 1  # :
    name: str = Field(default="good", min_length=2, max_length=20,description="test in class defination name")
    age: int = Field(default=18,ge=1,le=100)
    isNone: bool | None = False
    lst: list[int|str|BaseModel]
    option: Literal['a','b']

bodies = [{"id":1,"name":"test"},]

@route.post("/body_default")
async def post(body:Body) ->list: # 500
    bodies.append(body)
    return bodies

@route.post("/body_fastapi.Body")
async def body_fastapi_Body(body: Body = fastapi.Body()) ->list: # 500
    return bodies

@route.post("/body_fastapi.query")
async def body_fastapi_query(body: Body = fastapi.Query()) ->list: # 500
    return bodies


@route.get("debug/{item_id}")
async def read_item(item_id: str = Path(min_length=2,max_length=100,description="test str in path variables")
                    , q: str | None  = Query(min_length=2)):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


@route.get("debugs/{item_id}")
async def read_item(item_id: Optional[str], q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

@route.get("debugs1/{item_id}")
async def read_item(item_id: Union[str,int], q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


@route.get("/users/{user_id}/items/{item_id}",tags=['users'])
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item



@route.api_route("/multi", methods=["GET", "POST", "PUT"],summary="summary",description="description",tags=['multi'])
def multi():
    return {"message": "支持多种方法"}


@route.api_route("/trace", methods=["TRACE"])
def trace_endpoint():
    return {"method": "TRACE"}


@route.api_route("/connect", methods=["CONNECT"])
def connect_endpoint():
    return {"method": "CONNECT"}


from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect
@route.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # await websocket.accept()
    # while True:
    #     data = await websocket.receive_text()
    #     await websocket.send_text(f"收到: {data}")
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message: {data}")
    except WebSocketDisconnect:
        print("客户端断开连接")
    finally:
        # 清理资源
        pass



def ori_func(e):
    return e

def ori_func1(a,b,c,d,z=Depends(ori_func)):
    return ori_func

@route.get("/depends")
def depends(req: Request, r=Depends(ori_func1)):
    # req
    return r

@route.get("/depends_nested")
def depends_nested(req: Request, r=Depends(depends)):
    # req
    return r