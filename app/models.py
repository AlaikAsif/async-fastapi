# Pydantic models for request/response
from pydantic import BaseModel, Field
from typing import Literal, Optional, Union, Any
from datetime import datetime


class Document(BaseModel):
    type: Literal["invoice", "contract"]
    content: dict
    metaData: Optional[dict] = None


class uploadResponse(BaseModel):
    job_id: str
    message: str
    timestamp: str


class processRequest(BaseModel):
    job_id: str
    document: str


class InvoiceResult(BaseModel):
    invoice_number: str
    amount: float
    status: str


class ContractResult(BaseModel):
    contract_number: str
    parties: list
    effective_date: str
    status: str
    signed_by: list


class ErrorResult(BaseModel):
    error: str


class processResponse(BaseModel):
    job_id: str
    status: Literal["pending", "processing", "completed", "failed"]
    result: Optional[Union[InvoiceResult, ContractResult, ErrorResult, dict]] = None
    progress: int
    created_at: str
    updated_at: str


class statusResponse(BaseModel):
    job_id: str
    status: Literal["pending", "processing", "completed", "failed"]
    progress: int
    created_at: str
    updated_at: str
    result: Optional[Union[InvoiceResult, ContractResult, ErrorResult, dict]] = None

