from sqlalchemy.orm import Session
from .. import models
from ..schemas import product as product_schema

def get_product(db: Session, product_id: int):
    """通过ID获取产品"""
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session, name: str = None, skip: int = 0, limit: int = 100):
    """获取产品列表, 可选择按名称筛选"""
    query = db.query(models.Product)
    if name:
        query = query.filter(models.Product.name.contains(name))
    return query.offset(skip).limit(limit).all()

def create_product(db: Session, product: product_schema.ProductCreate):
    """创建新产品"""
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product: product_schema.ProductUpdate):
    """更新产品信息"""
    db_product = get_product(db, product_id)
    if db_product:
        update_data = product.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    """删除产品"""
    db_product = get_product(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product