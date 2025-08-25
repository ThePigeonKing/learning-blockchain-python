from fastapi import HTTPException, Request

from src.blockchain import Blockchain


def get_blockchain_instance(request: Request) -> Blockchain:
    bc = getattr(request.app.state, "bc", None)
    if bc is None:
        raise HTTPException(status_code=503, detail="Blockchain not initialized")
    return bc
