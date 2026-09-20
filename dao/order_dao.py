'''
todo: 只定义dao method ?
'''

from fastapi import Depends
from model.order import Order, get_session, OrderResponse, OrderSchema

def get_order(id:int=None, user_id:int=None, title:str=None,session=None) -> OrderResponse:
    q = session.query(Order)
    if id: q = q.filter( Order.id == id )
    if user_id: q = q.filter( Order.userid == user_id )
    if title: q = q.where(Order.title.like('%'+title+'%'))
    res = q.all()
    # return {"data":OrderSchema(many=True).dump(q,many=True)}
    # return {"data":[OrderSchema.model_validate(o) for o in r]}
    return {"data":[{"order_id":r.id,'order_title':r.title,"user_id":r.userid,"create_date":r.create_date,"update_date":r.update_date} for r in res]}

