from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, Request, Form
from models import Users
from database import SessionLocal
from starlette import status
from .auth import get_current_user,verify_password,get_password_hash
from passlib.context import CryptContext

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates



router = APIRouter(
    prefix='/user',
    tags=['user']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

templates = Jinja2Templates(directory="templates")



class UserVerification(BaseModel):
    username: str
    password: str
    new_password: str = Field(min_length=3)


# @router.get('/info', status_code=status.HTTP_200_OK)
# async def get_user(user: user_dependency, db: db_dependency):
#     if user is None:
#         raise HTTPException(status_code=401, detail="Authentication failed")

#     return db.query(Users).filter(Users.id == user.get('id')).first()

@router.get("/password", response_class=HTMLResponse)
async def change_password(request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    
    return templates.TemplateResponse("change_pass.html", {"request": request, "user": user})

@router.post("/password", response_class=HTMLResponse)
async def change_pass_commit(request: Request, db: db_dependency,username: str = Form(...),
                             password: str = Form(...), new_password: str = Form(...)):
    
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    
    if username != user.get("username"):
        msg = msg = "Invalid username or password"
        return templates.TemplateResponse("change_pass.html", {"request": request, "msg": msg,"user":user})
    
    user_model = db.query(Users).filter(Users.username == username).first()

    msg = "Invalid username or password"

    if user_model is not None:
        if user_model.username == username and verify_password(password,user_model.hashed_password):
            user_model.hashed_password = get_password_hash(new_password)

            db.add(user_model)
            db.commit()
            msg = "Password updated"

    return templates.TemplateResponse("change_pass.html", {"request": request, "msg": msg,"user":user})



# @router.put('/change_password', status_code=status.HTTP_204_NO_CONTENT)
# async def change_password(user: user_dependency, db: db_dependency, user_verification: UserVerification):
#     if user is None:
#         raise HTTPException(status_code=401, detail="Authentication failed")

#     user_model = db.query(Users).filter(Users.id == user.get('id')).first()

#     if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
#         raise HTTPException(
#             status_code=401, detail="Current Password is wrong")
#     user_model.hashed_password = bcrypt_context.hash(
#         user_verification.new_password)
#     db.add(user_model)
#     db.commit()
