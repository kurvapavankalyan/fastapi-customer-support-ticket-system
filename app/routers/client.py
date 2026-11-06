from fastapi import APIRouter, HTTPException

from app.dependencies import CurrentCustomer
from app.models import Ticket
from app.routers._types import DbSession
from app.schemas import (
    Response,
    TicketInput,
    TicketResponse,
    TicketUpdate
)

router = APIRouter()


@router.get("/app/client/profile", response_model=Response)
def get_my_profile(
    current_user: CurrentCustomer
):
    return current_user


@router.post(
    "/app/client/tickets",
    response_model=TicketResponse,
    status_code=201
)
def create_ticket(
    info: TicketInput,
    current_user: CurrentCustomer,
    db: DbSession
):
    new_ticket = Ticket(
        user_id=current_user.ID,
        message=info.message
    )

    try:
        db.add(new_ticket)
        db.commit()
        db.refresh(new_ticket)
        return new_ticket
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Ticket creation failed"
        ) from exc


@router.get("/app/client/tickets", response_model=list[TicketResponse])
def get_my_tickets(
    current_user: CurrentCustomer,
    db: DbSession
):
    return db.query(Ticket).filter(
        Ticket.user_id == current_user.ID
    ).all()


@router.get(
    "/app/client/tickets/{ticket_id}",
    response_model=TicketResponse
)
def get_my_ticket(
    ticket_id: int,
    current_user: CurrentCustomer,
    db: DbSession
):
    ticket = db.query(Ticket).filter(
        Ticket.ID == ticket_id,
        Ticket.user_id == current_user.ID
    ).first()

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket


@router.patch(
    "/app/client/tickets/{ticket_id}",
    response_model=TicketResponse
)
def update_my_ticket(
    ticket_id: int,
    info: TicketUpdate,
    current_user: CurrentCustomer,
    db: DbSession
):
    ticket = db.query(Ticket).filter(
        Ticket.ID == ticket_id,
        Ticket.user_id == current_user.ID
    ).first()

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    if info.message is not None:
        ticket.message = info.message

    db.commit()
    db.refresh(ticket)
    return ticket
