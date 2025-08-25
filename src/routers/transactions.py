from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.blockchain import Blockchain
from src.deps import get_blockchain_instance
from src.models import TransactionRequest

router = APIRouter()


@router.post("/new")
def new_transaction(
    item: TransactionRequest, bc: Blockchain = Depends(get_blockchain_instance)
):
    new_index = bc.new_transaction(
        sender=item.sender, recipient=item.recepient, amount=item.amount
    )
    response = {"message": f"Transaction will be added to Block #{new_index}"}

    return JSONResponse(status_code=201, content=response)
