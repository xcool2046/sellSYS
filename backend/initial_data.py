import logging
from app.database import SessionLocal
from app.crud.crud_employee import create_employee
from app.schemas.employee import EmployeeCreate
from app.models.employee import EmployeeRole

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    db = SessionLocal()
    
    # 创建一个初始管理员用户
    admin_user = EmployeeCreate(
        username="admin",
        email="admin@sellsys.com",
        password="admin",
        full_name="Administrator",
        role=EmployeeRole.ADMIN
    )
    
    try:
        create_employee(db, admin_user)
        logger.info("Admin user created successfully.")
    except Exception as e:
        logger.error(f"Could not create admin user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    logger.info("Creating initial data...")
    init_db()
    logger.info("Initial data created.")