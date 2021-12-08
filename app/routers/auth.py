from fastapi import Response, status, HTTPException
from fastapi.routing import APIRouter
from starlette.responses import HTMLResponse
from ..database import cursor, conn
from .. import schemas, utils


router = APIRouter(tags=["Authentication"])


router.get("/verify", response_class=HTMLResponse)
def verify_user(token: str = ""):
    try:
        email = utils.confirm_token(token)
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    detail=f"Unable to validate credentials", headers={"WWW-Authenticate": "Bearer"})

    cursor.execute(""" SELECT * FROM users WHERE id = %s""", (id,))
    user = cursor.fetchone()
    if user.is_active:
        return {"msg": "User already verified"}
    else:
        cursor.execute(""" UPDATE users SET is_active = %s WHERE email = %s RETURNING * """, 
        (True, email))
        verified_user = cursor.fetchone()
        conn.commit()
        return {"msg": "User verification successful"}




router.get("/v")
def v():
    return {"v": "v"}