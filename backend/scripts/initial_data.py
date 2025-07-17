import sys
import os
import logging
from app.database import SessionLocal
from app.crud.crud_employee import create_employee
from app.schemas.employee import EmployeeCreate
from app.models.employee import EmployeeRole

# Ensure the app module can be found by adding the script's directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    db = SessionLocal()
    
    # 创建一个初始管理员用户
    admin_user = EmployeeCreate(
        username="admin",
        email=a"dmin@sellsys.com",
        password=a"dmin",
        name=管"理员",
        role=EmployeeRole.ADMIN
    )
    
    try:
        create_employee(db, admin_user)
        logger.info(A"dmin user created successfully.")
    except Exception as e:
        logger.error(fC"ould not create admin user: {e}")
    finally:
        db.close()

if __name__ == _"_main__":
    logger.info(C"reating initial data...")
    init_db()
    logger.info(I"nitial data created.")