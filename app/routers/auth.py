from fastapi import APIRouter, HTTPException, Response
from app.schemas import RegisterRequest, LoginRequest
from app.database import get_db
from app.auth import hash_password, verify_password, create_token
router=APIRouter()
@router.post("/register")
def register(data:RegisterRequest):
    email=data.email.strip().lower()
    with get_db() as db:
        if db.execute("SELECT id FROM users WHERE email=?",(email,)).fetchone(): raise HTTPException(409,"Email is already registered")
        cur=db.execute("INSERT INTO users(email,password_hash) VALUES (?,?)",(email,hash_password(data.password))); db.commit()
    return {"message":"Registration successful","user_id":cur.lastrowid}
@router.post("/login")
def login(data:LoginRequest,response:Response):
    with get_db() as db: row=db.execute("SELECT id,password_hash FROM users WHERE email=?",(data.email.strip().lower(),)).fetchone()
    if not row or not verify_password(data.password,row["password_hash"]): raise HTTPException(401,"Invalid email or password")
    response.set_cookie("access_token",create_token(row["id"]),httponly=True,samesite="lax",max_age=86400)
    return {"message":"Login successful"}
@router.post("/logout")
def logout(response:Response):
    response.delete_cookie("access_token"); return {"message":"Logged out"}
