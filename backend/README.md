# CarScope - Car Search & AI Assistant MVP

A full-stack car search and AI assistant experience built with React and FastAPI.

## Features

- 🚗 Browse and search cars with advanced filters
- 🔍 Filter by make, model, year, price, mileage, and location
- 💾 Save favorite cars
- 🤖 AI assistant to answer questions about cars, search results, and saved cars
- ⚡ Fast API backend with in-memory database
- ⚛️ Modern React frontend with TypeScript

## Project Structure

```
carscope/
├── frontend/          # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API client
│   │   ├── App.tsx        # Main app component
│   │   └── main.tsx       # Entry point
│   ├── package.json
│   └── vite.config.ts
└── backend/           # FastAPI backend
    ├── app/
    │   ├── models/        # Data models
    │   ├── routes/        # API routes
    │   ├── services/      # Business logic
    │   ├── database/      # In-memory DB
    │   └── main.py        # App entry point
    └── requirements.txt
```

## Getting Started

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
python -m uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. In a new terminal, navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## API Endpoints

### Cars
- `GET /api/cars` - Get all cars with optional filters
- `GET /api/cars/{id}` - Get a specific car

Query parameters for filtering:
- `make` - Filter by make
- `model` - Filter by model
- `year_min`, `year_max` - Filter by year range
- `price_min`, `price_max` - Filter by price range
- `mileage_max` - Filter by max mileage
- `location` - Filter by location

### Chat
- `POST /api/chat/ask` - Ask the AI assistant a question

## Development Notes

- Backend uses FastAPI with CORS enabled for localhost frontend
- Frontend uses Vite for fast development and React 18
- In-memory database is pre-populated with sample cars
- Chat service currently uses mock responses (can be integrated with OpenAI API)

## Next Steps for Production

1. Replace in-memory DB with a real database (PostgreSQL, MongoDB)
2. Integrate actual OpenAI API for chat
3. Add authentication and user management
4. Implement saved cars persistence
5. Add image storage and CDN
6. Deploy backend (Heroku, AWS, etc.)
7. Deploy frontend (Vercel, Netlify, etc.)
