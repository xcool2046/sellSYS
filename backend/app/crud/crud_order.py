from sqlalchemy.orm import Session
from fastapi import HTTPException
from .. import models
from ..schemas import order as order_schema
import uuid
from decimal import Decimal

def get_order(db: Session, order_id: int):
    """获取单个订单"""
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def get_orders(
   db: Session,
   customer_name: str = None,
   product_name: str = None,
   start_date: order_schema.datetime = None,
   end_date: order_schema.datetime = None,
   status: order_schema.OrderStatus = None,
   sales_id: int = None,
   skip: int = 0,
   limit: int = 100
):
   """获取订单列表（带筛选）"""
   query = db.query(models.Order).join(models.Customer)

   if customer_name:
       query = query.filter(models.Customer.company.ilike(f"%{customer_name}%"))
   
   if product_name:
       # This requires joining through OrderItem to Product
       query = query.join(models.OrderItem).join(models.Product).filter(models.Product.name.ilike(f"%{product_name}%"))

   if start_date:
       query = query.filter(models.Order.start_date >= start_date)
   
   if end_date:
       query = query.filter(models.Order.end_date <= end_date)

   if status:
       query = query.filter(models.Order.status == status)

   if sales_id:
       query = query.filter(models.Order.sales_id == sales_id)

   return query.offset(skip).limit(limit).all()

def update_order_financials(db: Session, order_id: int, financials: order_schema.OrderFinancialUpdate):
    """更新订单的财务信息"""
    db_order = get_order(db, order_id)
    if db_order:
        db_order.status = financials.status
        db_order.paid_amount = financials.paid_amount
        db_order.payment_date = financials.payment_date
        db.commit()
        db.refresh(db_order)
    return db_order

def create_order(db: Session, order: order_schema.OrderCreate):
    """创建新订单，并从数据库中获取真实价格"""
    
    total_amount = Decimal('0.0')
    order_items_to_create = []

    # 1. 验证产品存在并获取真实价格
    for item_data in order.order_items:
        product = db.query(models.Product).filter(models.Product.id == item_data.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with id {item_data.product_id} not found")
        
        # 使用数据库中的价格，忽略客户端提交的价格
        unit_price = product.price
        total_amount += item_data.quantity * unit_price
        
        # 准备要创建的订单项，使用真实价格
        item_dict = item_data.model_dump()
        item_dict['unit_price'] = unit_price
        order_items_to_create.append(item_dict)

    # 2. 创建订单主体
    db_order = models.Order(
        order_number=str(uuid.uuid4()),
        customer_id=order.customer_id,
        sales_id=order.sales_id,
        total_amount=total_amount,
        status=order.status
    )
    db.add(db_order)
    db.flush() # 获取订单ID

    # 3. 创建订单项
    for item_dict in order_items_to_create:
        db_item = models.OrderItem(
            **item_dict,
            order_id=db_order.id
        )
        db.add(db_item)
        
    db.commit()
    db.refresh(db_order)
    return db_order