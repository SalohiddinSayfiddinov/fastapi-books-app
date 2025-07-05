from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from auth.routes import router as auth_router
from categories.routes import router as categories_router
from books.routes import router as books_router
from authors.routes import router as authors_router
from vendors.routes import router as vendors_router

# Optional lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Do startup logic here if needed (e.g., connect to services)
    yield
    # Do shutdown logic here if needed (e.g., disconnect cleanly)

app = FastAPI(lifespan=lifespan)

# CORS middleware config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route includes
app.include_router(auth_router)
app.include_router(categories_router)
app.include_router(books_router)
app.include_router(authors_router)
app.include_router(vendors_router)
