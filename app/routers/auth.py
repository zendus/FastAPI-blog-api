from fastapi import Response, status, HTTPException
from fastapi.routing import APIRouter
from starlette.responses import HTMLResponse
from .. import schemas, utils


router = APIRouter(tags=["Authentication"])


