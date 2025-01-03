from fastapi import APIRouter
from models.datamodels import TestOutput

router = APIRouter()


@router.get('/api/stats', response_model=TestOutput)
async def GetGameStats():
    pass