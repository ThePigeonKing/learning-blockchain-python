from pydantic import BaseModel


class TransactionRequest(BaseModel):
    sender: str
    recepient: str
    amount: int
