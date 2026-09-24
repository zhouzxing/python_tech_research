# 编写更订单相关的增删改查接口，结合数据库
from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy import *
from sqlalchemy.orm import declarative_base,sessionmaker
from datetime import datetime
from pydantic import BaseModel

from model.order import OrderRequest,Order,get_session,OrderResponse

from dao.order_dao import get_order

route = APIRouter(prefix="/order_select_query",tags=["order_select_query"])

# 模糊查询
@route.get('/query',response_model=OrderResponse)
def orders(id:int=None, user_id:int=None, title:str=None,session=Depends(get_session)):
    q = session.query(Order)
    if id: q = q.filter(Order.id == id)
    if user_id: q = q.filter(Order.userid == user_id)
    if title: q = q.where(Order.title.like('%' + title + '%'))
    res = q.all()
    return {"data": [{"order_id": r.id, 'order_title': r.title, "user_id": r.userid, "create_date": r.create_date,
                      "update_date": r.update_date} for r in res]}

@route.get('/select', response_model=OrderResponse)
def orders(id: int = None, user_id: int = None, title: str = None, session=Depends(get_session)):
    s = select(Order)
    if id: s = s.filter(Order.id == id)
    if user_id: s = s.filter(Order.userid == user_id)
    if title: s = s.where(Order.title.like('%' + title + '%'))

    res = session.execute(s)
    return {"data": [{"order_id": r.id, 'order_title': r.title, "user_id": r.userid, "create_date": r.create_date,
                      "update_date": r.update_date} for r in res]}


# todo 请求响应模型序列化Order类问题
@route.get('/no_response_model')
def orders(id:int=None, user_id:int=None, title:str=None,session=Depends(get_session)):
    q = session.query(Order)
    if id: q = q.filter(Order.id == id)
    if user_id: q = q.filter(Order.userid == user_id)
    if title: q = q.where(Order.title.like('%' + title + '%'))
    res = q.all()
    return res



@route.get('/{id}',response_model=OrderResponse)
def orders(id:int,session=Depends(get_session)):
    r = session.query(Order).filter( Order.id == id ).first()
    session.close()
    return {"data":
                {"order_id":r.id,'order_title':r.title,"user_id":r.userid,"create_date":r.create_date,"update_date":r.update_date}
            }

@route.delete('/',response_model=OrderResponse)
def orders(session=Depends(get_session)):
    return '删除订单'


@route.post('/',response_model=OrderResponse)
def orders(order:OrderRequest,session=Depends(get_session)):
    d = order.model_dump()  # d = {"title":xxx,"userid":xxx}
    o1 = Order( **d )
    session.add(o1)
    session.commit()
    session.close()
    return {'code':200,'detail':'添加成功！'}


@route.put('/{id}',response_model=OrderResponse)
def orders(order:OrderRequest,id:int,session=Depends(get_session)):
    r = session.query( Order ).filter( Order.id == id ).update( order.model_dump(exclude_unset=True) )
    session.commit()
    session.close()
    return OrderResponse(status_code='200',detail='ok',total=r)
