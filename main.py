from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware

from starlette.staticfiles import StaticFiles
from router.features import form, method, file, validation, mimetype, path_query_variables, json

from router.dbopt import mysql,order_route

from router.workhome import wk_0915,wk_0916,wk_0917

app = FastAPI(
    swagger_ui_parameters={
        "docExpansion": "none",  # 完全折叠，所有 Tags 默认收起
        "defaultModelsExpandDepth": -1  # 顺便把底部的 Schemas 模型也收起来
    },
    title="fastapi tutor - gk"
)

# request response model
app.include_router(mimetype.route)
app.include_router(method.route)
app.include_router(path_query_variables.route)
app.include_router(validation.route)
app.include_router(form.route)
app.include_router(file.route)
app.include_router(json.route)


app.include_router(mysql.route)
app.include_router(order_route.route)

# homeworks...
app.include_router(wk_0915.route)
app.include_router(wk_0916.route)
app.include_router(wk_0917.route)
# for r in app.routes:
#     print(r.path, r.methods, r.name)

app.mount(path="/static",app=StaticFiles(directory="/home/geeker/Pictures"),name="sn")

@app.get("/proxy")
def get(request: Request):
    path = request.url_for('sn',path = 'head.png')
    return path

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # 允许所有来源，开发阶段用
    # allow_origins=["null","http://localhost:8000"],          # 允许所有来源，开发阶段用
    allow_credentials=True,       # 允许携带 Cookie
    allow_methods=["*"],          # 允许所有 HTTP 方法
    allow_headers=["*"],          # 允许所有请求头
)

from middle import middles
app.middleware("http")(middles.black)
app.middleware("http")(middles.time_)
# black_list = ['192.168.1.40','192.168.1.94'] # '127.0.0.1'，'192.168.1.26‘
# @app.middleware("http",)
# async def middleware(req:Request, next):
#     if req.client.host in black_list:
#         return Response("you are limited to access!")
#     res = await next(req)
#     # print('exite http',req.client.host)
#     return res
#
# @app.middleware("https")
# async def middleware(req:Request, next):
#     print('enter https',time.time())
#     res = await next(req)
#     print('exite https',time.time())
#     return res
#
# @app.middleware("websocket")
# async def middleware(req:Request, next):
#     print('enter websocket',req.client.host)
#     res = await next(req)
#     print('exite websocket',req.client.host)
#     return res



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",port=9090)