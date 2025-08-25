from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.blockchain import Blockchain
from src.deps import get_blockchain_instance

router = APIRouter()


@router.post("/chain")
def full_chain(bc: Blockchain = Depends(get_blockchain_instance)):
    response = {
        "chain": bc.chain,
        "length": len(bc.chain),
    }

    json_response = jsonable_encoder(response)

    return JSONResponse(status_code=200, content=json_response)
