from fastapi import Cookie, Header, HTTPException

from app.auth import decode_token
from app.database import get_db
from app.models import User


def current_user(
    access_token: str | None = Cookie(None),
    authorization: str | None = Header(None),
):
    token = access_token or (
        authorization.split(" ", 1)[1].strip()
        if authorization and authorization.lower().startswith("bearer ")
        else None
    )

    if not token:
        raise HTTPException(401, "Authentication required")

    user_id = decode_token(token)

    if not user_id:
        raise HTTPException(401, "Invalid or expired token")

    with get_db() as db:
        row = db.execute(
            "SELECT id, email FROM users WHERE id=?",
            (user_id,),
        ).fetchone()

    if not row:
        raise HTTPException(401, "User not found")

    return User(row["id"], row["email"])