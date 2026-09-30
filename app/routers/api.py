from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import current_user
from app.models import User
from app.database import get_db
router=APIRouter()
@router.get("/token")
def token(user:User=Depends(current_user)): return {"authenticated":True,"user_id":user.id}
@router.get("/session-info")
def session_info(user:User=Depends(current_user)): return {"authenticated":True,"user_id":user.id,"email":user.email}
@router.get("/session-data")
def session_data(user:User=Depends(current_user)):
    with get_db() as db: count=db.execute("SELECT COUNT(*) AS c FROM recommendations WHERE user_id=?",(user.id,)).fetchone()["c"]
    return {"user_id":user.id,"recommendation_count":count}
@router.get("/api/history")
def history(user:User=Depends(current_user)):
    with get_db() as db: rows=db.execute("SELECT id,planner,request_json,response_json,created_at FROM recommendations WHERE user_id=? ORDER BY id DESC",(user.id,)).fetchall()
    return [dict(r) for r in rows]
@router.get("/recommendations-details/{recommendation_id}")
def details(recommendation_id:int,user:User=Depends(current_user)):
    with get_db() as db: row=db.execute("SELECT * FROM recommendations WHERE id=? AND user_id=?",(recommendation_id,user.id)).fetchone()
    if not row: raise HTTPException(404,"Recommendation not found")
    return dict(row)
