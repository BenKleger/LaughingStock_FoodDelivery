from fastapi import APIRouter
from typing import List
from FastAPI_DB.schemas.payment_processor import PaymentProcessor, PaymentProcessorCreate
from FastAPI_DB.services.payment_processor_service import process_payment, validatePaymentMethod

router = APIRouter(prefix="/payment", tags=["payment"])

@router.post("")
def process_payment_endpoint(payload: PaymentProcessorCreate):
    return process_payment(payload)

@router.post("validate_order")
def validate_payment_endpoint(payload: PaymentProcessorCreate):
    return validatePaymentMethod(payload)