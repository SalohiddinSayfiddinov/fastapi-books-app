from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth.routes import router as auth_router
from categories.routes import router as categories_router
from books.routes import router as books_router
from authors.routes import router as authors_router
from vendors.routes import router as vendors_router

app = FastAPI()

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

