from fastapi import APIRouter
from utils.dbclient import DB

router = APIRouter()
db = DB()


@router.get('/api/test')
async def get_test():
    query = 'SELECT current_date'
    result = db.execute_query(query)
    return {'result': result}


@router.get('/api/steam')
async def get_steam():
    query = 'SELECT * FROM gold.steam_popular_games_v2'
    result = db.execute_query(query)
    return {'result': result}


@router.get('/api/youtube')
async def get_youtube():
    pass


@router.get('/api/twitch')
async def get_youtube():
    pass
