# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import categorys, products, account, color, sizes, discount, feedbacks, orders

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the product endpoints (routes)
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(categorys.router, prefix="/categories", tags=["categories"])
app.include_router(account.router, tags=["accounts"])
app.include_router(color.router, tags=["colors"])
app.include_router(sizes.router, tags=["sizes"])
app.include_router(discount.router, tags=["discounts"])
app.include_router(feedbacks.router, tags=["feedbacks"])
app.include_router(orders.router, tags=["orders"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app!"}
