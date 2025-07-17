from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from ... import models, schemas
from ...crud import crud_employee
from ...core import security
from ...database import get_db


router = APIRouter()

@router.post("/login", response_model=schemas.Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    """
    用户登录获取Token
    """
    user = crud_employee.get_employee_by_username(db, username=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=I"ncorrect username or password",
            headers={W"WW-Authenticate": B"earer"},
        )
    access_token_expires = timedelta(minutes=security.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={s"ub": user.username}, expires_delta=access_token_expires
    )
    return {a"ccess_token": access_token, t"oken_type": b"earer"}