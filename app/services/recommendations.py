from app.schemas import *
from app.services.catalog import search
from app.services.gemini import gemini
from urllib.parse import quote_plus

def make_search_url(platform, title):
    query = quote_plus(title)

    if platform.lower() == "amazon":
        return f"https://www.amazon.in/s?k={query}"

    if platform.lower() == "flipkart":
        return f"https://www.flipkart.com/search?q={query}"
    if platform.lower() == "ikea":
        return f"https://www.ikea.com/in/en/search/?q={query}"
    if platform.lower() == "swiggy":
        return f"https://www.swiggy.com/search?query={query}"
    if platform.lower() == "zomato":
        return f"https://www.zomato.com/search?query={query}"
    if platform.lower() == "oyo":
        return f"https://www.oyorooms.com/search?location={query}"
    return ""
def normalize(planner, budget, data):
    recs=[]
    for x in (data.get("recommendations") or [])[:12]:
        try:
            recs.append(RecommendationItem(title=str(x.get("title","Recommendation")),category=str(x.get("category","general")),platform=str(x.get("platform","")),estimated_price=float(x.get("estimated_price",0)),reason=str(x.get("reason","")),url=make_search_url(str(x.get("platform","")), str(x.get("title","Recommendation"))) or str(x.get("url",""))))
        except (TypeError, ValueError):
            pass
    total=sum(x.estimated_price for x in recs)
    return RecommendationResponse(planner=planner,budget=budget,budget_used=min(total,budget),summary=str(data.get("summary","AI budget plan")),allocation={str(k):float(v) for k,v in (data.get("allocation") or {}).items()},recommendations=recs,ai_generated=True)

def home(req):
    candidates=search([x.category.lower() for x in req.items],req.budget,[req.style,req.room_type])
    prompt=f"""You are PocketSmart AI. Return JSON only with keys summary, allocation, recommendations. Budget INR {req.budget}. Room {req.room_type}. Style {req.style}. Requested items {[x.model_dump() for x in req.items]}. Use only these candidates: {[x.__dict__ for x in candidates]}. Keep recommendations within budget."""
    ai=gemini.generate(prompt)
    if ai: return normalize("home",req.budget,ai)
    return RecommendationResponse(planner="home",budget=req.budget,budget_used=min(sum(x.price for x in candidates),req.budget),summary=f"Budget-friendly {req.style} plan for your {req.room_type}.",allocation={"furniture":req.budget*.45,"lighting":req.budget*.20,"decor":req.budget*.15,"reserve":req.budget*.20},recommendations=[RecommendationItem(title=x.title,category=x.category,platform=x.platform,estimated_price=x.price,reason="Selected from the local demo catalog for your budget and style.",url=make_search_url(x.platform, x.title) or x.url) for x in candidates],warning="Gemini is not configured; deterministic fallback recommendations are being used.")

def party(req):
    candidates=search(["catering","venue","decoration"],req.budget,[req.event_type])
    prompt=f"""Return JSON only with keys summary, allocation, recommendations. Plan a {req.event_type} for {req.guests} guests. Budget INR {req.budget}. Venue {req.venue}. City {req.city}. Preferences {req.preferences}. Use only these candidates: {[x.__dict__ for x in candidates]}."""
    ai=gemini.generate(prompt)
    if ai: return normalize("party",req.budget,ai)
    return RecommendationResponse(planner="party",budget=req.budget,budget_used=min(req.budget*.9,req.budget),summary=f"Budget plan for {req.guests} guests and a {req.event_type} event.",allocation={"catering":req.budget*.5,"venue":req.budget*.25,"decoration":req.budget*.15,"reserve":req.budget*.1},recommendations=[RecommendationItem(title=x.title,category=x.category,platform=x.platform,estimated_price=x.price,reason="Budget-planning option from the local demo catalog.",url=make_search_url(x.platform, x.title) or x.url) for x in candidates],warning="Gemini is not configured; deterministic fallback recommendations are being used.")

def jewelry(req,image=None,mime=None):
    candidates=search(["jewelry"],req.budget,[req.style,req.occasion])
    prompt=f"""Return JSON only with keys summary, allocation, recommendations. Recommend jewelry for occasion {req.occasion}, style {req.style}, budget INR {req.budget}. Outfit description: {req.outfit_description}. An outfit image may be attached. Use only these candidates: {[x.__dict__ for x in candidates]}."""
    ai=gemini.generate(prompt,image,mime)
    if ai: return normalize("jewelry",req.budget,ai)
    return RecommendationResponse(planner="jewelry",budget=req.budget,budget_used=min(sum(x.price for x in candidates),req.budget),summary=f"{req.style.title()} jewelry suggestions for a {req.occasion} occasion.",allocation={"jewelry":req.budget*.85,"reserve":req.budget*.15},recommendations=[RecommendationItem(title=x.title,category=x.category,platform=x.platform,estimated_price=x.price,reason="Selected for the requested occasion and style.",url=make_search_url(x.platform, x.title) or x.url) for x in candidates],warning="Gemini is not configured; image analysis is unavailable.")
