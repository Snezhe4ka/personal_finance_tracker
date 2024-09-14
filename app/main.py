from fastapi import FastAPI
from app.routes import auth, transactions, categories, budgets, reports
from app.db.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

# Create the database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Personal Finance Tracker API")

# Allow requests from the Flask frontend (e.g., http://127.0.0.1:5000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5000"],  # Update with the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root route
@app.get("/")
def read_root():
    return {"message": "Your Personal Finance Tracker API"}

# Include routers
app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(categories.router)
app.include_router(budgets.router)
app.include_router(reports.router)
