from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ...schemas import sales_view
from ...crud import crud_sales_view
from ...database import get_db

router = APIRouter()

@router.get("/", response_model=List[sales_view.SalesView])
def read_sales_view(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    获取销售管理视图数据
    """
    sales_view_data = crud_sales_view.get_sales_view_data(db, skip=skip, limit=limit)
    return sales_view_data