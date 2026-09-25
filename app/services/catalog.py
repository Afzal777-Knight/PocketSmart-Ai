from dataclasses import dataclass
@dataclass(frozen=True)
class Item:
    title: str
    category: str
    platform: str
    price: float
    tags: tuple[str, ...]
    url: str

CATALOG = [
    Item("Minimalist LED Ceiling Light","lighting","Amazon",1499,("modern","minimal","lighting"),"https://www.amazon.in/"),
    Item("Nordic Floor Lamp","lighting","IKEA",2999,("modern","scandinavian","lamp"),"https://www.ikea.com/in/en/"),
    Item("Compact Study Table","furniture","IKEA",4999,("modern","wood","study"),"https://www.ikea.com/in/en/"),
    Item("6-Seater Dining Table","furniture","Amazon",12999,("dining","wood","family"),"https://www.amazon.in/"),
    Item("Decorative Wall Art Set","decor","Flipkart",1199,("art","minimal","decor"),"https://www.flipkart.com/"),
    Item("Artificial Indoor Plant","decor","IKEA",799,("green","minimal","decor"),"https://www.ikea.com/in/en/"),
    Item("Birthday Decoration Kit","decoration","Amazon",1499,("birthday","party","decor"),"https://www.amazon.in/"),
    Item("Vegetarian Catering Package","catering","Zomato",450,("vegetarian","food","catering"),"https://www.zomato.com/"),
    Item("Party Food Package","catering","Swiggy",500,("food","party","catering"),"https://www.swiggy.com/"),
    Item("Budget Event Venue","venue","OYO",8000,("venue","event","budget"),"https://www.oyorooms.com/"),
    Item("Elegant Stud Earrings","jewelry","Amazon",899,("elegant","stud","classic"),"https://www.amazon.in/"),
    Item("Gold-Tone Necklace Set","jewelry","Flipkart",1499,("elegant","gold","necklace"),"https://www.flipkart.com/"),
    Item("Minimal Pendant","jewelry","Amazon",699,("minimal","pendant","modern"),"https://www.amazon.in/"),
    Item("Statement Earrings","jewelry","Flipkart",1299,("party","statement","modern"),"https://www.flipkart.com/"),
]

def search(categories: list[str], budget: float, tags: list[str], limit: int = 8):
    candidates = [x for x in CATALOG if x.price <= budget]
    if categories:
        preferred = [x for x in candidates if x.category in categories]
        if preferred:
            candidates = preferred
    tags = [x.lower() for x in tags]
    return sorted(candidates, key=lambda x: (-sum(t in x.tags for t in tags), x.price))[:limit]
