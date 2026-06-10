from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from dotenv import load_dotenv
from app.routes import cars, chat, marketcheck

load_dotenv()

app = FastAPI(
    title="CarScope API",
    description="Car search and AI assistant API",
    version="0.1.0"
)

# Add rate limiter
app.state.limiter = chat.limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(cars.router)
app.include_router(chat.router)
app.include_router(marketcheck.router)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "CarScope API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
