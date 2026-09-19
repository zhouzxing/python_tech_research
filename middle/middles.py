from fastapi import Request,Response
import time


black_list = ['192.168.1.40','192.168.1.94'] # '127.0.0.1'，'192.168.1.26‘
# @app.middleware("http",)
async def black(req:Request, next):
    if req.client.host in black_list:
        return Response("you are limited to access!")
    res = await next(req)
    # print('exite http',req.client.host)
    return res

# @app.middleware("https")
async def time_(req:Request, next):
    print('enter https',time.time())
    res = await next(req)
    print('exite https',time.time())
    return res
