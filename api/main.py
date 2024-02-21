import os
from routers import accounts_routers
from fastapi import FastAPI
from routers import items_routers, accounts_routers


app = FastAPI()




app.include_router(items_routers.router)
app.include_router(accounts_routers.router)
