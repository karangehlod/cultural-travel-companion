# AI Cultural Travel Companion 🌍🌸

**Google for Developers - PromptWars Hackathon**  
**Challenge: Destination Discovery & Cultural Experiences**  
**Category: Build with AI (In-person)**

An AI-powered cultural travel companion that helps travelers discover destinations beyond traditional tourist attractions through personalized recommendations, local cultural experiences, historical storytelling, hidden gems, regional cuisine, festivals, and authentic activities.

---

## 🎯 Challenge Overview

**Challenge**: Destination Discovery & Cultural Experiences  
**Category**: Build with AI / Build with AI (In-person)  
**Hackathon**: Google for Developers - PromptWars (In-person)

### Problem Statement

Modern travel applications primarily focus on hotels, flights, and popular attractions, often overlooking the rich cultural identity, local traditions, community experiences, and hidden gems that make a destination truly unique. Travelers seek meaningful connections with local culture, heritage, and authentic experiences but lack tools to discover and engage with them meaningfully.

### Solution: AI Cultural Travel Companion

An AI-powered travel companion that transforms generic trip planning into personalized cultural journeys by combining:
- **Personalized Recommendations** - AI-powered destination matching based on interests, budget, travel style
- **Cultural Storytelling** - AI-generated immersive historical narratives and cultural context
- **Hidden Gem Discovery** - AI-powered discovery of hidden gems, local secrets, off-the-beaten-path locations
- **Cultural Events & Festivals** - Real-time local festival, ceremony, and community event discovery
- **Authentic Cuisine Discovery** - Regional cuisine recommendations with cultural context and family recipes
- **Authentic Experience Matching** - Workshops, homestays, craft workshops, community events
- **Personalized Itinerary Generation** - AI-generated day-by-day cultural itineraries tailored to interests, budget, travel style
- **Cultural Context & Storytelling** - Historical narratives, legends, traditions, and cultural context for every location

---

## 🛠 Tech Stack

### Backend (Python/FastAPI)
| Technology | Purpose |
|------------|---------|
| **FastAPI** | High-performance async API framework |
| **Google Gemini API** | Primary LLM for cultural storytelling, recommendations, itinerary generation |
| **Google Places API (New)** | Real place data, places, photos, reviews, opening hours |
| **Google Maps API** | Geocoding, directions, place details, place photos |
| **Google Maps Geocoding API** | Geocoding, reverse geocoding |
| **Google Maps Directions API** | Directions, transit, walking, driving routes |
| **Firebase/Firestore** | User data, preferences, saved trips, chat history |
| **Redis** | Caching, rate limiting, session management |
| **Celery + Redis** | Background tasks for AI generation, caching |
| **PostgreSQL** | User data, trips, preferences, saved places (production) |
| **Pydantic** | Data validation |
| **Pydantic AI** | Structured AI outputs with Pydantic validation |
| **LangChain/LangGraph** | Agent orchestration for multi-step workflows |
| **Pydantic AI Agents** | Structured agent workflows |

### Frontend (React/TypeScript/Next.js)
| Technology | Purpose |
|------------|---------|
| **Next.js 14+** | App Router, Server Components, Server Actions |
| **React 18+** | Client components, hooks |
| **TypeScript** | Type safety |
| **Tailwind CSS** | Styling |
| **shadcn/ui** | UI components |
| **React Query / TanStack Query** | Server state management |
| **Zustand** | Client state management |
| **React Hook Form + Zod** | Form validation |
| **MapLibre GL JS** | Interactive maps |
| **React Hot Toast** | Toasts |
| **Lucide React** | Icons |
| **date-fns** | Date handling |

### AI/ML Services
| Service | Purpose |
|---------|---------|
| **Google Gemini 1.5 Pro/Flash** | Primary LLM for cultural storytelling, recommendations, itineraries |
| **Google Gemini Embeddings** | Embeddings for semantic search, similarity |
| **Google Places API (New)** | Real place data, photos, reviews, opening hours |
| **Google Maps Platform** | Maps, Places, Geocoding, Directions, Places API (New) |
| **Google Events API** | Events, festivals, community events |
| **Firebase Genkit** | AI orchestration (optional) |
| **LangGraph** | Multi-agent workflows for complex itinerary planning |
| **Pydantic AI** | Structured outputs with validation |

### Infrastructure & DevOps
| Tool | Purpose |
|------|---------|
| **Docker** | Containerization |
| **Docker Compose** | Local development |
| **Google Cloud Run** | Serverless deployment (backend) |
| **Vercel** | Frontend deployment |
| **Cloud SQL (PostgreSQL)** | Production database |
| **Cloud Memorystore (Redis)** | Caching |
| **Cloud Firestore** | User data, trips, preferences |
| **Cloud Storage** | Images, assets |
| **Cloud Build** | CI/CD |
| **GitHub Actions** | CI/CD |

### APIs & Services
| API | Purpose |
|-----|---------|
| **Google Maps Platform** | Places API New, Geocoding, Directions, Places Photos, Places Details |
| **Google Places API (New)** | Places, photos, reviews, opening hours, place details |
| **Google Maps Geocoding API** | Geocoding, reverse geocoding |
| **Google Maps Directions API** | Directions |
| **Google Places API (New)** | Places, photos, reviews, opening hours |
| **Google Events API** | Events, festivals, community events |
| **Google Gemini API** | LLM, embeddings |
| **Firebase Auth** | Authentication |
| **Firebase Firestore** | User data, trips, preferences |

---

## 📁 Project Structure

```
cultural-travel-companion/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── endpoints/
│   │   │   │   │   ├── auth.py
│   │   │   │   │   ├── destinations.py
│   │   │   │   │   ├── recommendations.py
│   │   │   │   │   ├── storytelling.py
│   │   │   │   │   ├── hidden_gems.py
│   │   │   │   │   ├── cultural_events.py
│   │   │   │   │   ├── cuisine.py
│   │   │   │   │   ├── experiences.py
│   │   │   │   │   ├── itineraries.py
│   │   │   │   │   ├── chat.py
│   │   │   │   │   ├── users.py
│   │   │   │   │   └── trips.py
│   │   │   │   └── router.py
│   │   │   └── deps.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   ├── database.py
│   │   │   ├── redis.py
│   │   │   ├── firebase.py
│   │   │   ├── exceptions.py
│   │   │   └── logging.py
│   │   ├── models/
│   │   │   ├── base.py
│   │   │   ├── user.py
│   │   │   ├── trip.py
│   │   │   ├── destination.py
│   │   │   ├── hidden_gem.py
│   │   │   ├── cultural_event.py
│   │   │   ├── cuisine.py
│   │   │   ├── experience.py
│   │   │   ├── story.py
│   │   │   ├── itinerary.py
│   │   │   ├── chat.py
│   │   │   └── __init__.py
│   │   ├── schemas/
│   │   ├── services/
│   │   │   ├── google_places.py
│   │   │   ├── google_maps.py
│   │   │   ├── gemini.py
│   │   │   └── __init__.py
│   │   ├── main.py
│   │   └── __init__.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── app/
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── auth/
│   │       ├── login/
│   │       │   └── page.tsx
│   │       └── signup/
│   │           └── page.tsx
│   ├── components/
│   ├── lib/
│   ├── public/
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
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
git clone <repository-url>
cd cultural-travel-companion
cp .env.example .env
```

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

### 2. Enable Required Google Cloud APIs

Go to [Google Cloud Console](https://console.cloud.google.com/) and enable:
- ✅ **Places API (New)**
- ✅ **Maps JavaScript API**
- ✅ **Geocoding API**
- ✅ **Directions API**
- ✅ **Maps Embed API**
- ✅ **Generative Language API (Gemini)**

### 3. Run with Docker Compose (Recommended)

```bash
docker-compose up -d
```

This starts:
- **PostgreSQL** on port 5432
- **Redis** on port 6379
- **Backend API** on port 8000 (http://localhost:8000)
- **Frontend** on port 3000 (http://localhost:3000)

### 4. Access the Application

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:800/api/v1/docs |
| API Docs (ReDoc) | http://localhost:8000/api/v1/redoc |

---

## 🔧 Local Development (Without Docker)

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

### Recommendations
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/recommendations/destinations` | Get AI destination recommendations |
| POST | `/api/v1/recommendations/from-trip/{trip_id}` | Get recommendations from trip |

### Storytelling
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/storytelling/narrative` | Generate cultural narrative |
| POST | `/api/v1/storytelling/narrative/destination/{destination_id}` | Generate narrative for destination |
| GET | `/api/v1/storytelling/stories/destination/{destination_id}` | Get destination stories |
| POST | `/api/v1/storytelling/stories/generate` | Generate cultural story |

### Hidden Gems
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/hidden-gems/discover` | Discover hidden gems with AI |
| POST | `/api/v1/hidden-gems/discover/destination/{destination_id}` | Discover gems for destination |
| GET | `/api/v1/hidden-gems/destination/{destination_id}` | List hidden gems |

### Cultural Events
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/cultural-events/destination/{destination_id}` | List cultural events |
| POST | `/api/v1/cultural-events/search/nearby` | Search events nearby |
| POST | `/api/v1/cultural-events/insight` | Generate event cultural insight |
| POST | `/api/v1/cultural-events/insight/event/{event_id}` | Generate insight for event |

### Cuisine
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/cuisine/destination/{destination_id}` | List cuisines |
| GET | `/api/v1/cuisine/search/nearby` | Search food places nearby |
| POST | `/api/v1/cuisine/insight` | Generate cuisine insight |
| POST | `/api/v1/cuisine/insight/cuisine/{cuisine_id}` | Generate insight for cuisine |

### Experiences
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/experiences/destination/{destination_id}` | List experiences |
| GET | `/api/v1/experiences/search/nearby` | Search experiences nearby |
| POST | `/api/v1/experiences/insight` | Generate experience insight |
| POST | `/api/v1/experiences/insight/experience/{experience_id}` | Generate insight for experience |

### Itineraries
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/itineraries/generate` | Generate AI itinerary |
| POST | `/api/v1/itineraries/generate/trip/{trip_id}` | Generate itinerary for trip |
| GET | `/api/v1/itineraries/trip/{trip_id}` | Get trip itinerary |
| POST | `/api/v1/itineraries/trip/{trip_id}/day` | Add itinerary day |
| POST | `/api/v1/itineraries/trip/{trip_id}/day/{day_id}/item` | Add itinerary item |

### Chat
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/chat/message` | Send message to AI companion |
| GET | `/api/v1/chat/sessions` | List chat sessions |
| GET | `/api/v1/chat/sessions/{session_id}` | Get chat session with messages |
| DELETE | `/api/v1/chat/sessions/{session_id}` | Delete chat session |

---

## 🎨 Key Features Implementation

### 1. AI Cultural Storytelling
```python
# Backend: app/services/gemini.py
async def generate_cultural_narrative(
    destination_name: str,
    country: str,
    focus_topics: List[str] = ["history", "traditions", "arts", "cuisine"],
    length: str = "detailed"
) -> CulturalNarrative
```

Generates immersive cultural narratives with:
- Historical context and significance
- Local legends and oral traditions
- Cultural practices and their meanings
- Sensory details (sounds, smells, textures)
- Practical cultural etiquette

### 2. Personalized Destination Recommendations
```python
async def recommend_destinations(
    user_interests: List[str],
    travel_style: str,
    budget_range: str,
    group_size: int,
    num_recommendations: int = 5
) -> List[DestinationRecommendation]
```

Matches travelers to destinations based on:
- Cultural depth alignment
- Budget reality (local costs, not tourist prices)
- Travel style compatibility
- Group dynamics
- Accessibility needs

### 3. Hidden Gem Discovery
```python
async def discover_hidden_gems(
    destination: str,
    country: str,
    known_places: List[str],
    interest_areas: List[str],
    num_gems: int = 5
) -> List[HiddenGemRecommendation]
```

Finds authentic local spots:
- Neighborhood secrets locals cherish
- Family-run establishments
- Community gathering places
- Sacred/natural sites off tourist radar
- Artisan workshops and studios

### 4. Smart Itinerary Generation
```python
async def generate_itinerary(
    destination: str,
    duration_days: int,
    travel_style: str,
    budget: str,
    interests: List[str]
) -> FullItinerary
```

Creates day-by-day cultural journeys with:
- Thematic day narratives
- Balanced activity pacing
- Cultural context for each stop
- Practical logistics (transport, timing, costs)
- Reflection prompts
- Cultural etiquette guides

### 5. Real-time Google Places Integration
```python
# Backend: app/services/google_places.py
async def search_cultural_places(lat: float, lng: float, radius: int = 10000)
async def get_place_details(place_id: str)
async def get_place_photos(place_id: str, max_photos: int = 10)
```

Live data for:
- Cultural sites, museums, temples
- Local restaurants and markets
- Artisan workshops
- Community centers
- Heritage sites

### 6. Interactive AI Travel Companion
```python
async def chat_with_travel_companion(
    user_message: str,
    conversation_history: List[Dict],
    trip_context: Optional[Dict],
    user_profile: Optional[Dict]
) -> ChatResponse
```

Conversational AI that:
- Remembers trip context and preferences
- Suggests relevant destinations/experiences
- Explains cultural significance
- Helps modify itineraries in real-time
- Answers cultural etiquette questions

---

## 🔐 Authentication Flow

1. **Frontend** → Firebase Auth (Email/Password, Google, GitHub)
2. **Frontend** gets Firebase ID Token
3. **Frontend** → Backend `/api/v1/auth/verify-token` with ID Token
4. **Backend** verifies token with Firebase Admin SDK
5. **Backend** creates/updates user in PostgreSQL
6. **Backend** returns JWT Access + Refresh Tokens
7. **Frontend** stores tokens, uses Access Token for API calls
8. **Refresh Token** used to get new Access Token when expired

---

## 🌍 Deployment

### Backend to Google Cloud Run

```bash
# Build and push
gcloud builds submit --tag gcr.io/PROJECT_ID/travel-companion-backend

# Deploy
gcloud run deploy travel-companion-backend \
  --image gcr.io/PROJECT_ID/travel-companion-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars=GOOGLE_API_KEY=...,FIREBASE_PROJECT_ID=...,etc.
```

### Frontend to Vercel

```bash
# Connect GitHub repo to Vercel
# Add environment variables in Vercel dashboard
# Deploy automatically on push
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

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest -v --cov=app
```

### Frontend Tests
```bash
cd frontend
npm run test
npm run test:coverage
```

### Integration Tests
```bash
# Start services
docker-compose up -d

# Run API tests
pytest tests/integration/ -v
```

---

## 📊 Monitoring & Observability

- **Logging**: Structured JSON logging with structlog
- **Metrics**: Prometheus metrics endpoint
- **Tracing**: OpenTelemetry integration ready
- **Error Tracking**: Sentry integration ready
- **Health Checks**: `/health` endpoint for load balancers

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Google for Developers** - PromptWars Hackathon
- **Google Gemini** - Cultural intelligence & storytelling
- **Google Places API (New)** - Real-world cultural place data
- **Google Maps Platform** - Navigation & location services
- **Firebase** - Authentication & real-time data
- **Unsplash** - Destination photography
- **Open Source Community** - FastAPI, Next.js, Tailwind, and all dependencies

---

## 📞 Support & Contact

- **Hackathon**: Google for Developers - PromptWars
- **Challenge**: Destination Discovery & Cultural Experiences
- **Team**: AI Cultural Travel Companion

---

**Built with ❤️ for meaningful cultural connections worldwide**