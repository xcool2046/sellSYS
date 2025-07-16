from sqlalchemy.orm import Session
from ..models import sales_follow as models
from ..schemas import sales_follow as schemas

def get_sales_follow(db: Session, follow_id: int):
    return db.query(models.SalesFollow).filter(models.SalesFollow.id == follow_id).first()

def get_sales_follows_by_customer(db: Session, customer_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.SalesFollow).filter(models.SalesFollow.customer_id == customer_id).offset(skip).limit(limit).all()

def create_sales_follow(db: Session, follow: schemas.SalesFollowCreate):
    db_follow = models.SalesFollow(**follow.model_dump())
    db.add(db_follow)
    db.commit()
    db.refresh(db_follow)
    return db_follow

def update_sales_follow(db: Session, follow_id: int, follow_update: schemas.SalesFollowUpdate):
    db_follow = get_sales_follow(db, follow_id)
    if db_follow:
        update_data = follow_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_follow, key, value)
        db.commit()
        db.refresh(db_follow)
    return db_follow

def delete_sales_follow(db: Session, follow_id: int):
    db_follow = get_sales_follow(db, follow_id)
    if db_follow:
        db.delete(db_follow)
        db.commit()
    return db_follow