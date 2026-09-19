from typing import Annotated
from fastapi import Depends, FastAPI,APIRouter,Form,File,UploadFile
from fastapi.security import OAuth2PasswordRequestForm

route = APIRouter(prefix="/file",tags=["file"])

@route.post("/bytes")
def bytes(file:bytes = File()):
    print("bytes:\t" + str(file))
    print("str:\t" + file.decode("utf-8"))
    return file.decode("utf-8")


@route.post("/uploadfile")
async def uploadfile(file:UploadFile):
    data = await file.read()
    print("bytes:\t" + str(data))
    print("str:\t" + data.decode("utf-8"))
    return data.decode("utf-8")

# text read/write


