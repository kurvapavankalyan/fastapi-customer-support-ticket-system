from fastapi import APIRouter, HTTPException

from app.dependencies import CurrentAdmin
from app.models import Customer, Ticket
from app.routers._types import DbSession
from app.schemas import AdminTicketUpdate, TicketResponse

router = APIRouter()


@router.get("/app/admin/customers")
def get_all_customers(
    current_admin: CurrentAdmin,
    db: DbSession
):
    customers = db.query(Customer).all()
    return [
        {
            "ID": customer.ID,
            "name": customer.name,
            "email": customer.email,
            "role": customer.role
        }
        for customer in customers
    ]


@router.get("/app/admin/tickets", response_model=list[TicketResponse])
def get_all_tickets(
    current_admin: CurrentAdmin,
    db: DbSession
):
    return db.query(Ticket).all()


@router.patch(
    "/app/admin/tickets/{ticket_id}",
    response_model=TicketResponse
)
def admin_update_ticket(
    ticket_id: int,
    info: AdminTicketUpdate,
    current_admin: CurrentAdmin,
    db: DbSession
):
    ticket = db.query(Ticket).filter(Ticket.ID == ticket_id).first()

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    update_data = info.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(ticket, key, value)

    db.commit()
    db.refresh(ticket)
    return ticket


@router.delete("/app/admin/tickets/{ticket_id}")
def delete_ticket(
    ticket_id: int,
    current_admin: CurrentAdmin,
    db: DbSession
):
    ticket = db.query(Ticket).filter(Ticket.ID == ticket_id).first()

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    db.delete(ticket)
    db.commit()

    return {"message": "Ticket deleted successfully"}
