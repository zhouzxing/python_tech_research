from typing import Annotated
from fastapi import Depends, FastAPI,APIRouter,Form,File,UploadFile
from fastapi.security import OAuth2PasswordRequestForm

route = APIRouter(prefix="/json",tags=["json"])


@route.get("/")
def json():
    return [1,"str",[1,2,3],{1,2,3},{"a":1,"b":2}]