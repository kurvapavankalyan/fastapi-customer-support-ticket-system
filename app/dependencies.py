from typing import Annotated

from fastapi import Depends, HTTPException, status

from app.models import Customer
from app.routers._types import DbSession
from app.security import oauth2_scheme, verify_token


def get_client_access(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: DbSession
) -> Customer:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"}
    )

    payload = verify_token(token)
    if payload is None:
        raise credentials_exception

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        raise credentials_exception

    user = db.query(Customer).filter(Customer.ID == user_id).first()
    if user is None:
        raise credentials_exception

    return user


def get_admin_access(
    current_user: Annotated[Customer, Depends(get_client_access)]
) -> Customer:
    if current_user.role.lower() != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


CurrentCustomer = Annotated[Customer, Depends(get_client_access)]
CurrentAdmin = Annotated[Customer, Depends(get_admin_access)]
