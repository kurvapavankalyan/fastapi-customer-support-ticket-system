from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.models import Customer
from app.routers._types import DbSession
from app.schemas import Response, UserInput
from app.security import create_access_token, hash_password, verify_password

router = APIRouter()


@router.post("/app/register", response_model=Response, status_code=201)
def user_register(info: UserInput, db: DbSession):
    existing_user = db.query(Customer).filter(
        (Customer.name == info.name) |
        (Customer.email == str(info.email))
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Customer name or email already exists"
        )

    new_user = Customer(
        name=info.name,
        password=hash_password(info.password),
        email=str(info.email),
        role="Client"
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Registration failed"
        ) from exc


@router.post("/app/client/token")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: DbSession
):
    customer = db.query(Customer).filter(
        Customer.email == form_data.username
    ).first()

    if customer is None or not verify_password(
        form_data.password, customer.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return {
        "access_token": create_access_token({"sub": str(customer.ID)}),
        "token_type": "bearer"
    }
