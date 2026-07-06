# 🌍 AI Cultural Travel Companion

> **Google for Developers — PromptWars Hackathon**  
> **Challenge:** Destination Discovery & Cultural Experiences  
> **Category:** Build with AI (In-person)

An AI-powered cultural travel companion that helps travelers discover destinations beyond traditional tourist attractions through personalized recommendations, local cultural experiences, historical storytelling, hidden gems, regional cuisine, festivals, and authentic activities.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎯 **Personalized Discovery** | AI-powered destination matching based on interests, budget, travel style |
| 📖 **Immersive Storytelling** | Rich cultural narratives, historical context, and local legends |
| 💎 **Hidden Gems** | Off-the-beaten-path locations, secret local spots, community treasures |
| 🍽️ **Culinary Heritage** | Traditional dishes, family recipes, food markets, dining customs |
| 🎪 **Cultural Events** | Authentic festivals, ceremonies, workshops, performances |
| 🗺️ **Smart Itineraries** | Day-by-day cultural journeys with storytelling & practical logistics |
| 💬 **AI Travel Companion** | Conversational AI that understands cultural nuance & remembers preferences |

---

## 🏗️ Architecture

Request Response and Architeture Diagram

```mermaid

graph TD
    Client[Web Client (Next.js, React)]
    
    subgraph Frontend
        Client --> Pages[Next.js Pages & Routes]
        Pages --> Components[React Components]
        Components --> Tailwind[Tailwind CSS]
        Components --> MapLibre[MapLibre GL JS]
    end

    subgraph Backend [Backend API (FastAPI)]
        Pages -- REST API --> Router[API Router]
        Router --> Auth[Firebase Auth]
        Router --> Controllers[Service Controllers]
        
        Controllers --> DB[(PostgreSQL/SQLite)]
        Controllers --> Redis[(Redis Cache)]
        
        Controllers -- AI Requests --> Gemini[Google Gemini API]
        Controllers -- Location Data --> GPlaces[Google Places API]
        Controllers -- Map Data --> GMaps[Google Maps API]
    end
```

## 🔄 Request / Response Flow

```mermaid

sequenceDiagram
    participant U as User
    participant F as Frontend (Next.js)
    participant B as Backend (FastAPI)
    participant G as Google Places API
    participant AI as Gemini 1.5 Pro
    participant DB as Database

    U->>F: Request AI Destination Recommendations
    F->>B: POST /api/v1/recommendations/destinations (Preferences)
    B->>DB: Fetch User History & Constraints
    B->>AI: Generate Destination Ideas with Cultural Context
    AI-->>B: Return AI generated destinations
    B->>G: Fetch Real-world Place Details & Photos
    G-->>B: Return Place Metadata
    B-->>F: Aggregate & Return Formatted Recommendations
    F-->>U: Render Beautiful Interactive Map & Cards
```

---

## 🚀 Quick Start

### Prerequisites

- **Docker & Docker Compose** (recommended)
- **Python 3.11+** (for local backend development)
- **Node.js 20+** (for local frontend development)
- **Google Cloud Account** with APIs enabled
- **Firebase Project** for authentication

### 1. Clone & Configure

```bash
git clone https://github.com/your-username/cultural-travel-companion.git
cd cultural-travel-companion
cp .env.example .env
```

### 2. Configure Environment Variables

Edit `.env` with your API keys:

```bash
# Required API Keys (Get from Google Cloud Console)
GOOGLE_API_KEY=your_google_api_key
GOOGLE_MAPS_API_KEY=your_maps_api_key
GOOGLE_PLACES_API_KEY=your_places_api_key
GEMINI_API_KEY=your_gemini_api_key

# Firebase (Get from Firebase Console > Project Settings > Service Accounts)
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_PRIVATE_KEY_ID=your-private-key-id
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYOUR_KEY\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-xxxxx@your-project.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=your-client-id

# Security
SECRET_KEY=your-super-secret-key-min-32-chars
```

### 3. Enable Required Google Cloud APIs

Go to [Google Cloud Console](https://console.cloud.google.com/) and enable:
- ✅ Places API (New)
- ✅ Maps JavaScript API
- ✅ Geocoding API
- ✅ Directions API
- ✅ Generative Language API (Gemini)

### 4. Run with Docker Compose (Recommended)

```bash
docker-compose up -d --build
```

This starts:
- **PostgreSQL** on port 5432
- **Redis** on port 6379
- **Backend API** on port 8000 → http://localhost:8000
- **Frontend** on port 3000 → http://localhost:3000

### 5. Access the Application

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/api/v1/docs |
| API Docs (ReDoc) | http://localhost:8000/api/v1/redoc |
| Health Check | http://localhost:8000/health |

---

## 🛠️ Local Development (Without Docker)

### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your keys

# Run database migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Set environment variables
cp .env.example .env.local
# Edit .env.local

# Start development server
npm run dev
```

---

## 📡 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/verify-token` | Verify Firebase ID token |
| POST | `/api/v1/auth/refresh` | Refresh access token |
| GET | `/api/v1/auth/me` | Get current user |

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/users/me/preferences` | Get user preferences |
| PATCH | `/api/v1/users/me/preferences` | Update user preferences |
| GET | `/api/v1/users/me/saved-destinations` | Get saved destinations |
| GET | `/api/v1/users/me/saved-experiences` | Get saved experiences |

### Destinations
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/destinations/search` | Search destinations (Google Places) |
| GET | `/api/v1/destinations/nearby` | Find nearby cultural places |
| GET | `/api/v1/destinations/{place_id}/details` | Get place details |
| GET | `/api/v1/destinations/{place_id}/photos` | Get place photos |
| POST | `/api/v1/destinations/{place_id}/generate-narrative` | Generate AI cultural narrative |
| GET | `/api/v1/destinations` | List saved destinations |
| POST | `/api/v1/destinations/save` | Save a destination |

### AI-Powered Features
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/recommendations/destinations` | Get AI destination recommendations |
| POST | `/api/v1/storytelling/narrative` | Generate cultural narrative |
| POST | `/api/v1/hidden-gems/discover` | Discover hidden gems with AI |
| POST | `/api/v1/cultural-events/insight` | Generate event cultural insight |
| POST | `/api/v1/cuisine/insight` | Generate cuisine insight |
| POST | `/api/v1/experiences/insight` | Generate experience insight |
| POST | `/api/v1/itineraries/generate` | Generate AI itinerary |
| POST | `/api/v1/chat/message` | Chat with AI travel companion |

---

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest -v --cov=app --cov-report=html
```

### Frontend Tests

```bash
cd frontend
npm test -- --watchAll=false --coverage
```

### Integration Tests

```bash
# Start services
docker-compose up -d

# Wait for services
sleep 30

# Run smoke tests
curl -f http://localhost:8000/health
curl -f http://localhost:3000
curl -f http://localhost:8000/api/v1/docs
```

---

## 🐳 Docker

### Build Images

```bash
# Backend
docker build -t cultural-travel-backend ./backend

# Frontend
docker build -t cultural-travel-frontend ./frontend
```

### Run Containers

```bash
# Backend
docker run -p 8000:8000 \
  -e GOOGLE_API_KEY=$GOOGLE_API_KEY \
  -e GEMINI_API_KEY=$GEMINI_API_KEY \
  \
  \
  cultural-travel-backend

# Frontend
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1 \
  cultural-travel-frontend
```

---

## ☁️ Deployment

### Firebase Hosting (Frontend)

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# Initialize
firebase init hosting

# Deploy
firebase deploy
```

### Google Cloud Run (Backend)

```bash
# Build and push
gcloud builds submit --tag gcr.io/PROJECT_ID/travel-companion-backend

# Deploy
gcloud run deploy travel-companion-backend \
  --image gcr.io/PROJECT_ID/travel-companion-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Database (Production)

```bash
# Cloud SQL PostgreSQL
gcloud sql instances create travel-companion-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=us-central1

# Run migrations
alembic upgrade head
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Google Cloud API key | ✅ |
| `GOOGLE_MAPS_API_KEY` | Google Maps API key | ✅ |
| `GOOGLE_PLACES_API_KEY` | Google Places API key | ✅ |
| `GEMINI_API_KEY` | Google Gemini API key | ✅ |
| `FIREBASE_PROJECT_ID` | Firebase project ID | ✅ |
| `FIREBASE_PRIVATE_KEY` | Firebase service account private key | ✅ |
| `FIREBASE_CLIENT_EMAIL` | Firebase service account email | ✅ |
| `SECRET_KEY` | JWT secret key (min 32 chars) | ✅ |
| `DATABASE_URL` | PostgreSQL connection string | ✅ |
| `REDIS_URL` | Redis connection string | ⭕ |
| `NEXT_PUBLIC_API_URL` | Frontend API URL | ✅ |
| `NEXT_PUBLIC_GOOGLE_MAPS_API_KEY` | Maps API key for frontend | ✅ |

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Code Style

- **Backend**: Ruff + MyPy for linting/type checking
- **Frontend**: ESLint + Prettier + TypeScript strict mode
- **Commits**: Conventional Commits format

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Google for Developers** — PromptWars Hackathon
- **Google Gemini** — Cultural intelligence & storytelling
- **Google Places API (New)** — Real-world cultural place data
- **Google Maps Platform** — Navigation & location services
- **Firebase** — Authentication & real-time data
- **Unsplash** — Destination photography
- **Open Source Community** — FastAPI, Next.js, Tailwind, and all dependencies

---

**Built with ❤️ for meaningful cultural connections worldwide** 🌍🌸
