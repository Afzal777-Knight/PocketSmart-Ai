from fastapi import APIRouter, Depends, File, Form, UploadFile
from app.dependencies import current_user
from app.database import get_db
from app.models import User
from app.schemas import HomeRequest, PartyRequest, JewelryRequest
from app.services.recommendations import home, party, jewelry
router=APIRouter()

def save(user:User, planner:str, request_obj, result):
    with get_db() as db:
        db.execute("INSERT INTO recommendations(user_id,planner,request_json,response_json) VALUES (?,?,?,?)", (user.id,planner,request_obj.model_dump_json(),result.model_dump_json()))
        db.commit()

@router.post("/generate-home")
def generate_home(data:HomeRequest,user:User=Depends(current_user)):
    result=home(data); save(user,"home",data,result); return result

@router.post("/generate-party")
def generate_party(data:PartyRequest,user:User=Depends(current_user)):
    result=party(data); save(user,"party",data,result); return result

@router.post("/generate-jewelry")
async def generate_jewelry(budget:float=Form(...),occasion:str=Form(...),style:str=Form("elegant"),outfit_description:str=Form(""),outfit_image:UploadFile|None=File(None),user:User=Depends(current_user)):
    req=JewelryRequest(budget=budget,occasion=occasion,style=style,outfit_description=outfit_description)
    image=await outfit_image.read() if outfit_image else None
    mime=outfit_image.content_type if outfit_image else None
    result=jewelry(req,image,mime); save(user,"jewelry",req,result); return result
