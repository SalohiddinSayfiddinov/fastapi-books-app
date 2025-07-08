from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from auth.routes import router as auth_router
from categories.routes import router as categories_router
from books.routes import router as books_router
from authors.routes import router as authors_router
from vendors.routes import router as vendors_router
from cart.routes import router as cart_router
from wishlist.routes import router as wishlist_router
from orders.routes import router as orders_router
from database import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create database tables
    from auth.models import User
    from orders.models import Order, OrderItem  # adjust path based on your project structure
    from books.models import Book
    from authors.models import Author
    from categories.models import Category
    from vendors.models import Vendor
    from wishlist.models import WishlistItem
    from cart.models import CartItem
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown: Add any cleanup logic here if needed

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(categories_router)
app.include_router(books_router)
app.include_router(authors_router)
app.include_router(vendors_router)
app.include_router(cart_router)
app.include_router(wishlist_router)
app.include_router(orders_router)


import subprocess
from fastapi.responses import JSONResponse

@app.get("/run-migrations")
def run_migrations():
    try:
        result = subprocess.run(["alembic", "upgrade", "head"], capture_output=True, text=True)
        return JSONResponse(
            content={
                "status": "success",
                "stdout": result.stdout
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "detail": str(e)
            }
        )
