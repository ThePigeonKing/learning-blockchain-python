from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.blockchain import Blockchain
from src.deps import get_blockchain_instance

router = APIRouter()


@router.get("/mine")
async def mine(bc: Blockchain = Depends(get_blockchain_instance)):
    # run PoW to get the next proof
    last_block = bc.last_block
    last_proof = last_block["proof"]
    proof = bc.proof_of_work(last_proof=last_proof)

    # must receive a reward for finding the proof
    # sender is "0", that means a new coin
    bc.new_transaction(sender="0", recipient=bc.node_id, amount=1)

    # forge new block by adding it to the chain
    previous_hash = bc.hash(last_block)
    block = bc.new_block(proof=proof, previous_hash=previous_hash)

    response = {
        "message": "New Block Forged",
        "index": block["index"],
        "transactions": block["transactions"],
        "proof": block["proof"],
        "previous_hash": block["previous_hash"],
    }

    return JSONResponse(status_code=201, content=response)
