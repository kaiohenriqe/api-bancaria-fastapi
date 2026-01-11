from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
import auth
from routers import transacoes  # importa o router da pasta routers

app = FastAPI(title="API Bancária Assíncrona")

# incluir router de transações
app.include_router(transacoes.router, prefix="/api", tags=["transacoes"])

# endpoint de login
@app.post("/login", response_model=auth.TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return await auth.login(form_data)