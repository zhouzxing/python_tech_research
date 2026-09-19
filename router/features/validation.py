import fastapi
from fastapi import APIRouter,Query,Path,HTTPException
from pydantic import Field,BaseModel,field_validator,model_validator
from typing import Annotated,Union,Optional


route = APIRouter(prefix="/validations",tags=["validations"])

@route.get("/annotated_query")
async def get(option: Annotated[str|None, Query(max_length=10)] = None):
    return option

@route.get("/annotated_query_lst")
async def get(option: Annotated[list[str], Query()] = None):
    return option


@route.get("/annotated_query_re")
async def get(option: Annotated[str|None, Query(min_length=2,max_length=10,pattern="^g.*k$")] = None):
    return option


@route.get("/annotated_path/{option}")
async def get(option: Annotated[str|None, Path(max_length=10)]):
    return option


@route.get("/query")
async def get(option: str = Query(min_length=2, max_length=10)):
    return option

@route.get("/params_validate")
async def params_validate(name:Union[str,None], # default
                 id: Optional[int]):
    pass


# @route.get("/field")
# async def get(option: str = Field(min_length=2, max_length=10)):
#     return option

class Clazz(BaseModel):
    name: str = Field(min_length=2,max_length=12)

@route.get("/field")
async def get(clazz: Clazz):
    return clazz

@route.get("/field_body")
async def get(clazz: Clazz = fastapi.Body()):
    return clazz


@route.get("/path_path/{option}")
async def get(option: str = Path(min_length=2, max_length=10)):
    return option
#
# @route.get("/path_query/{option}")
# async def get(option: str = Query(min_length=2, max_length=10)):
#     return option

# param not got!
@route.get("/path_bad")
async def get(option: str = Path(min_length=2, max_length=10)):
    return option


@route.get("/items/")
async def read_items(q: str|None = Query(default=None, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@route.get("/items_default_bad/")
async def read_items(q: str = Query(default=None, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# field/model_validator

class User(BaseModel):
    name: str
    passwd: str

    # @field_validator("passwd")
    # def check_passwd(cls,passwd,values): #
    #     # print(f'{values=}') # values=ValidationInfo(config={'title': 'User'}, context=None, data={'name': 'string'}, field_name='passwd')
    #     # 无法cannot access passwd/ name ?!
    #     # print(f'{values["passwd"]=}')
    #     # print(f'{values["name"]=}')
    #     if passwd == '001':
    #         raise HTTPException(status_code=408,detail="001 only root can set!")
    #     return passwd

    @model_validator(mode="before")
    def check_model_before(cls, data): #
        print('model_validator before............')
        return data

    @field_validator("passwd","name")
    def check_field(cls,value,values): #
        # print(f'{values=}') # values=ValidationInfo(config={'title': 'User'}, context=None, data={'name': 'string'}, field_name='passwd')
        # cannot access passwd/ name ?!
        # print(f'{values["passwd"]=}')
        # print(f'{values["name"]=}')
        print('field_validator............')
        if value == '001':
            raise HTTPException(status_code=408,detail="001 only root can set!")
        if value == 'root':
            raise HTTPException(status_code=408,detail="only root can set name!")
        return value

    @model_validator(mode="after")
    def check_model_after(self): #
        print('model_validator............')
        if self.passwd == '001':
            raise HTTPException(status_code=408,detail="model : 001 only root can set!")
        if self.name == 'root':
            raise HTTPException(status_code=408,detail="model : only root can set name!")
        return self


# u = User(age="20", name="geeker")


@route.post("/registe")
def registe(user: User):
    return user

