# This is where we bootstrap and run our server
import asyncio

from alembic.config import Config
from alembic.command import upgrade
from fastapi import FastAPI

from rest.users import user_route


app = FastAPI(debug=True)

app.include_router(user_route)


@app.get('/')
def hello():
    return 'hello world'


@app.on_event('startup')
async def application_start():
    loop = asyncio.get_running_loop()
    config = Config('alembic.ini')
    loop.run_in_executor(None, upgrade, config, 'head')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True, log_level='debug')
