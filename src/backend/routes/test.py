from fastapi import APIRouter
from models.datamodels import TestOutput
from utils.test import TestFunction

router = APIRouter()


@router.get('/api/test', response_model=TestOutput)
async def GetAPITest():
    test_str = TestFunction()
    return {'output': test_str}