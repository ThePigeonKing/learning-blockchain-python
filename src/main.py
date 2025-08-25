from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse

from src.blockchain import Blockchain
from src.deps import get_blockchain_instance
from src.routers.chain import router as chain_router
from src.routers.mine import router as mine_router
from src.routers.transactions import router as transactions_router


# create Blockchain instance for the whole application's life
@asynccontextmanager
async def lifespan(app: FastAPI):
    new_bc = Blockchain()
    app.state.bc = new_bc
    print(new_bc)
    yield


app = FastAPI(lifespan=lifespan)

# include subrouters
app.include_router(chain_router, tags=["chain"])
app.include_router(mine_router, tags=["mine"])
app.include_router(transactions_router, prefix="/transactions", tags=["transactions"])


@app.get("/info")
async def bc_info(bc: Blockchain = Depends(get_blockchain_instance)):

    return JSONResponse(bc.json_dict())
