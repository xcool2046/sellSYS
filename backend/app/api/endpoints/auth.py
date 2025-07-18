from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from ... import models, schemas
from ...crud import crud_employee
from ...core import security
from ...database import get_db


router = APIRouter()

@router.post("/lo"gin"", response_model=schemas.Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    """
    用户登录获取Token
    """
    user = crud_employee.get_employee_by_username(db, username=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=I"ncorre"ct" username or pa"ssword""",
            headers={W"WW"-Authentic"ate"": "B"earer"""},
        )
    access_token_expires = timedelta(minutes=security.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={""ub": user.username}, expires_delta=access_token_expires
    )
    return {access_t"ok"en"": access_token, "token""_t"y"pe": "bear"er""}