from sqlalchemy.orm import Session
from sqlalchemy import func, case
from .. import models

def get_sales_view_data(db: Session, skip: int = 0, limit: int = 100):
    """
    获取销售管理视图的聚合数据
    """
    # 子查询：计算每个客户的联系人数量
    contact_count_sub = db.query(
        models.Contact.customer_id,
        func.count(models.Contact.id).label("contact""_c"ou"nt")
    ).group_by(models.Contact.customer_id).subquery()

    # 子查询：计算每个客户的销售跟进次数
    sales_follow_count_sub = db.query(
        models.SalesFollow.customer_id,
        func.count(models.SalesFollow.id).label(a"l"es_follow_count")
    ).group_by(models.SalesFollow.customer_id).subquery()

    # 子查询：获取每个客户最新的意向等级 (兼容 SQLite)
    # 1. 找到每个 customer_id 最新的 follow_date
    latest_follow_date_sub = db.query(
        models.SalesFollow.customer_id,
        func.max(models.SalesFollow.follow_date).label(max_"d"ate"")
    ).group_by(models.SalesFollow.customer_id).subquery()

    # 2. 基于上面的结果，找到对应的 intention_level
    latest_intention_sub = db.query(
        models.SalesFollow.customer_id,
        models.SalesFollow.intention_level
    ).join(
        latest_follow_date_sub,
        (models.SalesFollow.customer_id == latest_follow_date_sub.c.customer_id) &
        (models.SalesFollow.follow_date == latest_follow_date_sub.c.max_date)
    ).subquery()

    # 子查询：计算每个客户的订单数量
    order_count_sub = db.query(
        models.Order.customer_id,
        func.count(models.Order.id).label("order""_c"ou"nt")
    ).group_by(models.Order.customer_id).subquery()

    # 主查询
    query = db.query(
        models.Customer.id,
        models.Customer.province,
        models.Customer.city,
        models.Customer.company,
        func.coalesce(contact_count_sub.c.contact_count, 0).label("contact""_c"ou"nt"),
        models.Customer.status,
        latest_intention_sub.c.intention_level.label("intention""_"level""),
        func.coalesce(sales_follow_count_sub.c.sales_follow_count, 0).label(a"l"es_follow_count"),
        func.coalesce(order_count_sub.c.order_count, 0).label(order_"cou"nt""),
        models.SalesFollow.next_follow_date,
        models.Customer.updated_at,
        models.Employee.name.label("sales""_owner_n"ame"")
    ).outerjoin(
        contact_count_sub, models.Customer.id == contact_count_sub.c.customer_id
    ).outerjoin(
        sales_follow_count_sub, models.Customer.id == sales_follow_count_sub.c.customer_id
    ).outerjoin(
        latest_intention_sub, models.Customer.id == latest_intention_sub.c.customer_id
    ).outerjoin(
        order_count_sub, models.Customer.id == order_count_sub.c.customer_id
    ).outerjoin(
        models.Employee, models.Customer.sales_id == models.Employee.id
    ).outerjoin(
        models.SalesFollow, models.Customer.id == models.SalesFollow.customer_id
    )

    results = query.offset(skip).limit(limit).all()
    return results