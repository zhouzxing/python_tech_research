# 编写更订单相关的增删改查接口，结合数据库
from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy import *
from sqlalchemy.orm import declarative_base,sessionmaker
from datetime import datetime
from pydantic import BaseModel

from model.order import OrderRequest,Order,get_session,OrderResponse

route = APIRouter(prefix="/order",tags=["orders"])

# 模糊查询
@route.get('/',response_model=list[OrderResponse])
def orders(id:int=None, user_id:int=None, title:str=None,session=Depends(get_session)):
    q = session.query(Order)
    if id: q = q.filter( Order.id == id )
    if user_id: q = q.filter( Order.userid == userid )
    if title: q = q.where(Order.title.like('%'+title+'%'))
    r = q.all()
    session.close()
    return r

@route.get('/{id}',response_model=OrderResponse)
def orders(id:int):
    session = Session()
    r = session.query(Order).filter( Order.id == id ).all()
    session.close()
    return [ {"order_id":i.id,'order_title':i.title,"user_id":i.userid,"create_date":i.create_date,"update_date":i.update_date} for i in r]

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
    session.query( Order ).filter( Order.id == id ).update( order.model_dump(exclude_unset=True) )
    session.commit()
    res = session.query(Order).filter(Order.id == id).first()
    session.close()
    return res
