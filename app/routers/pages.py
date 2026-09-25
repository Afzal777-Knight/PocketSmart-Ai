from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
router=APIRouter(); templates=Jinja2Templates(directory="app/templates")
def page(name):
    def handler(request:Request): return templates.TemplateResponse(name,{"request":request})
    return handler
router.add_api_route("/",page("index.html"),methods=["GET"],response_class=HTMLResponse)
router.add_api_route("/login",page("login.html"),methods=["GET"],response_class=HTMLResponse)
router.add_api_route("/register",page("register.html"),methods=["GET"],response_class=HTMLResponse)
router.add_api_route("/dashboard",page("dashboard.html"),methods=["GET"],response_class=HTMLResponse)
router.add_api_route("/planner/home",page("home.html"),methods=["GET"],response_class=HTMLResponse)
router.add_api_route("/planner/party",page("party.html"),methods=["GET"],response_class=HTMLResponse)
router.add_api_route("/planner/jewelry",page("jewelry.html"),methods=["GET"],response_class=HTMLResponse)
router.add_api_route("/history-page",page("history.html"),methods=["GET"],response_class=HTMLResponse)