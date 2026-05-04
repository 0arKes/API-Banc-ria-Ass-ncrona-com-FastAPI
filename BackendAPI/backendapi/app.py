from fastapi import FastAPI

from backendapi.routers import bank, token, transactions, user

app = FastAPI(title='API Sitema Bancário')


app.include_router(user.router)
app.include_router(token.router)
app.include_router(bank.router)
app.include_router(transactions.router)


@app.get('/')
def read_root():
    return {'msg': 'teste'}
