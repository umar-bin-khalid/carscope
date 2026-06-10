# CarScope 🚗

A **production-ready AI-powered car search MVP** with live Marketcheck integration and an intelligent 5-tool agent harness.

## Features

### 🔍 **Smart Car Search**
- Live Marketcheck API integration with 20+ filters (make, model, price, mileage, location)
- Fallback to realistic mock data when API is unavailable
- Real-time filtering with instant results

### 🤖 **AI Agent Harness** (5 Tools)
- **list_current_cars** – Show all cars on search page
- **get_vehicle_details** – Deep-dive on specific cars with specs & $/mile ratio
- **compare_cars** – Side-by-side comparison with value metrics
- **get_saved_cars** – Manage bookmarked listings
- **web_search** – DuckDuckGo integration for reviews & reliability info

### 💬 **Intelligent Chat Interface**
- Function-calling with GPT-4o-mini (or regex fallback)
- Beautiful response formatting (vehicle cards, comparison tables, search results)
- Tool activity transparency rail
- Suggested questions for discovery

### ✅ **Production Features**
- Rate limiting (20 req/min on chat endpoint)
- Comprehensive E2E test suite (50+ tests)
- HAR-mocked tests for fast CI/CD
- GitHub Actions automation
- Mock data fallback with visual indicator

## Tech Stack

**Frontend:**
- React 18 + TypeScript
- Vite (dev server)
- Axios (HTTP client)
- Playwright E2E tests

**Backend:**
- FastAPI (Python 3.10+)
- OpenAI SDK (gpt-4o-mini)
- httpx (async HTTP)
- slowapi (rate limiting)

**APIs:**
- Marketcheck v2/search/car/active (live inventory)
- DuckDuckGo Instant Answers (web search, no key needed)
- OpenAI (agent reasoning, optional)

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.10+
- Marketcheck API key (free tier available)

### 1. Clone & Setup

```bash
git clone https://github.com/YOUR_USERNAME/carscope.git
cd carscope

# Backend setup
cd backend
cp .env.example .env
# Edit .env and add MARKETCHECK_API_KEY
pip install -r requirements.txt
python -m uvicorn app.main:app --reload

# Frontend setup (new terminal)
cd frontend
npm install
npm run dev
```

### 2. Access the App
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/docs (Swagger UI)

### 3. Try It Out
1. Search for cars by make/model/price
2. Select a car to view details
3. Ask the AI agent: "What cars are on this page?"
4. Try: "Compare the first two cars" or "Is this reliable?"

## Configuration

### Environment Variables

**Backend (`backend/.env`):**
```env
MARKETCHECK_API_KEY=your_key_here
OPENAI_API_KEY=sk-... # Optional for better reasoning
```

**Frontend:**
API endpoints are hardcoded to `localhost:8000` (dev) or set via environment.

## Testing

### Run Tests
```bash
cd frontend

# Main E2E tests (real API)
npm run test:e2e

# HAR-mocked tests (10x faster, recommended for CI/CD)
npm run test:e2e:har

# Interactive UI mode
npm run test:e2e:ui

# Debug mode
npm run test:e2e:debug
```

### Test Coverage
- ✅ 50+ E2E test cases
- ✅ All 5 AI tools validated
- ✅ Filter interactions, car selection, chat flows
- ✅ Error handling & performance benchmarks
- ✅ UI rendering (cards, tables, badges)

See [TESTING.md](./frontend/TESTING.md) for complete guide.

## API Reference

### Search Endpoint
```bash
GET /api/marketcheck/search
  ?make=BMW
  &price_min=30000
  &price_max=50000
  &year=2022
  &zip=90210
  &radius=100
```

### Chat Endpoint (Rate Limited: 20/min)
```bash
POST /api/chat/ask
Content-Type: application/json

{
  "question": "What cars are on this page?",
  "current_cars_snapshot": [...],
  "saved_cars_snapshot": [...]
}
```

See [backend README](./backend/README.md) for full API docs.

## Project Structure

```
carscope/
├── frontend/                    # React + Vite app
│   ├── src/
│   │   ├── App.tsx             # Main component
│   │   ├── components/         # UI components
│   │   ├── services/           # API client
│   │   └── index.css           # Styling
│   ├── tests/                  # Playwright E2E tests
│   │   ├── e2e.spec.ts         # Main test suite
│   │   ├── e2e.har.spec.ts     # HAR-mocked tests
│   │   └── fixtures/
│   ├── TESTING.md              # Testing guide
│   └── package.json
│
├── backend/                     # FastAPI application
│   ├── app/
│   │   ├── main.py             # FastAPI app + rate limiter
│   │   ├── routes/             # Endpoint handlers
│   │   │   ├── chat.py         # AI agent endpoint
│   │   │   ├── marketcheck.py  # Car search proxy
│   │   │   └── cars.py         # Legacy endpoints
│   │   ├── services/           # Business logic
│   │   │   ├── agent_service.py   # 5-tool AI agent
│   │   │   ├── web_search.py      # DuckDuckGo integration
│   │   │   ├── mock_data.py       # Fallback inventory
│   │   │   └── ...
│   │   ├── models/             # Data models
│   │   └── database/           # Optional DB
│   ├── requirements.txt         # Python dependencies
│   ├── .env.example            # Environment template
│   └── README.md
│
├── .github/
│   └── workflows/
│       └── test.yml            # GitHub Actions CI/CD
│
├── README.md                   # You are here
├── IMPLEMENTATION_SUMMARY.md   # Detailed implementation guide
└── .gitignore
```

## Key Features Deep Dive

### 🎯 Mock Data Fallback
When Marketcheck API is unavailable (timeout, rate-limit, network error):
1. Backend automatically falls back to `mock_data.py` (25 realistic cars)
2. Frontend shows orange banner: "⚠️ Using demo data — Marketcheck API unavailable"
3. App continues working seamlessly

### 🛡️ Rate Limiting
- `/api/chat/ask` endpoint: **20 requests per minute per IP**
- Prevents spam, abuse, DDoS
- Returns 429 status when exceeded
- Implemented with `slowapi`

### 🔧 AI Agent Tools
Each tool returns structured data that the frontend renders beautifully:
- **Vehicle cards** – Price, mileage, $/mile ratio, VIN
- **Comparison tables** – Side-by-side specs with best value highlight
- **Search results** – Clickable cards linking to external sources

### 📊 Performance
- Page load: ~2 seconds
- Filter response: < 1 second
- Agent response: 1-3 seconds (depending on tools used)
- With HAR mocking: < 1.5 seconds

## Security Notes

- ✅ Rate limiting on chat endpoint
- ✅ CORS enabled for localhost only
- ✅ No user authentication (local MVP)
- ✅ API keys stored in `.env` (not committed)
- ⚠️ **Not production-ready** – Add auth/logging before deploying

For production deployment, consider:
- User authentication (OAuth, JWT)
- API request logging & monitoring
- HTTPS enforcement
- Database persistence
- Caching layer (Redis)

## CI/CD Pipeline

GitHub Actions automatically:
- Installs dependencies
- Runs 50+ E2E tests (HAR-mocked)
- Runs linter
- Uploads test report

See `.github/workflows/test.yml` for configuration.

## Development Tips

### Backend
```bash
cd backend
python -m uvicorn app.main:app --reload
# Auto-reloads on file changes
# Swagger UI: http://localhost:8000/docs
```

### Frontend
```bash
cd frontend
npm run dev
# Hot module reload on save
# Dev server: http://localhost:5173
```

### Debugging
```bash
# E2E test debugging
npm run test:e2e:debug

# See network requests
# In browser DevTools: Network tab

# Backend logs
# Check terminal where uvicorn is running
```

## Troubleshooting

### "Cannot find name 'filteredCars'"
This was fixed – use `listings` instead (backend filters).

### "Unterminated JSX contents"
Check closing tags in FilterPanel.tsx (was fixed).

### Marketcheck API returns 503
App automatically falls back to mock data. Check `.env` for API key.

### Tests timeout
Use HAR-mocked tests: `npm run test:e2e:har` (much faster).

## Contributing

This is an MVP/portfolio project. Feel free to fork and extend:
- Add more agent tools (pricing analysis, safety reports, etc.)
- Implement user authentication
- Add database persistence
- Deploy to production (Vercel + Railway/Heroku)

## License

MIT License – See LICENSE file.

## Author

Built by [Your Name] as an AI agent + car search MVP demo.

---

## Next Steps

1. ✅ **Immediate:** Review [IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md) for technical details
2. 📖 **Testing:** See [frontend/TESTING.md](./frontend/TESTING.md) for test suite guide
3. 🚀 **Deploy:** Backend → Railway/Heroku, Frontend → Vercel
4. 🔐 **Secure:** Add user auth, API key protection
5. 📊 **Monitor:** Set up logging & analytics

---

**Questions?** Open an issue or check the detailed docs linked above.

Happy coding! 🚀
