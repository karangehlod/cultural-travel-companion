"""
Google Gemini AI Service
"""
import json
import structlog
from typing import Optional, List, Dict, Any, AsyncGenerator
from pydantic import BaseModel, Field

import google.generativeai as genai
from google.generativeai.types import GenerationConfig

from app.core.config import settings


logger = structlog.get_logger()


class CulturalNarrative(BaseModel):
    """AI-generated cultural narrative"""
    title: str
    summary: str
    full_narrative: str
    key_themes: List[str]
    historical_period: Optional[str] = None
    cultural_significance: Optional[str] = None
    local_perspective: Optional[str] = None


class DestinationRecommendation(BaseModel):
    """AI-generated destination recommendation"""
    destination_name: str
    country: str
    region: Optional[str] = None
    city: Optional[str] = None
    match_score: float  # 0-1
    reasons: List[str]
    best_for: List[str]  # cultural_immersion, food, history, nature, etc.
    budget_level: str  # budget, mid-range, luxury
    best_time_to_visit: str
    cultural_highlights: List[str]
    hidden_gems_suggested: List[str]
    estimated_daily_cost: Optional[Dict[str, float]] = None


class ItineraryDay(BaseModel):
    """Single day in AI-generated itinerary"""
    day_number: int
    date: Optional[str] = None
    title: str
    theme: str
    narrative: str
    activities: List[Dict[str, Any]]
    cultural_insights: List[str]
    estimated_cost: Optional[float] = None
    transport_notes: Optional[str] = None


class FullItinerary(BaseModel):
    """Complete AI-generated itinerary"""
    trip_title: str
    destination: str
    duration_days: int
    travel_style: str
    budget_range: str
    group_size: int
    overview: str
    cultural_context: str
    days: List[ItineraryDay]
    practical_tips: List[str]
    packing_suggestions: List[str]
    cultural_etiquette: List[str]
    emergency_info: Dict[str, str]


class HiddenGemRecommendation(BaseModel):
    """AI-generated hidden gem recommendation"""
    name: str
    description: str
    location_hint: str  # General area, not exact coordinates
    cultural_significance: str
    local_story: str
    best_time_to_visit: str
    access_difficulty: str  # easy, moderate, hard
    visit_duration_hours: float
    what_makes_it_special: str
    local_tips: List[str]


class CulturalEventInsight(BaseModel):
    """AI-generated cultural event insight"""
    event_name: str
    cultural_significance: str
    history_and_origins: str
    traditions_and_rituals: List[str]
    what_to_expect: str
    visitor_etiquette: List[str]
    dress_code: Optional[str] = None
    best_way_to_participate: str
    local_perspective: str
    practical_info: Dict[str, str]


class CuisineInsight(BaseModel):
    """AI-generated cuisine insight"""
    dish_name: str
    description: str
    cultural_significance: str
    history: str
    region_of_origin: str
    traditional_occasion: str
    key_ingredients: List[str]
    preparation_highlights: str
    flavor_profile: str
    pairing_suggestions: List[str]
    where_to_find_authentic_version: str
    local_eating_customs: List[str]


class ExperienceInsight(BaseModel):
    """AI-generated experience insight"""
    experience_name: str
    experience_type: str
    description: str
    cultural_significance: str
    tradition_preserved: str
    community_impact: str
    what_to_expect: str
    preparation_tips: List[str]
    local_insights: str
    why_it_matters: str


class ChatResponse(BaseModel):
    """AI chat response"""
    content: str
    function_calls: Optional[List[Dict[str, Any]]] = None
    referenced_content: Optional[Dict[str, List[str]]] = None


class GeminiService:
    """Service for interacting with Google Gemini API"""
    
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY or settings.GOOGLE_API_KEY
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
        self.flash_model = genai.GenerativeModel(settings.GEMINI_FLASH_MODEL)
    
    async def generate_cultural_narrative(
        self,
        destination_name: str,
        country: str,
        region: Optional[str] = None,
        city: Optional[str] = None,
        focus_topics: Optional[List[str]] = None,
        length: str = "detailed",  # brief, detailed, immersive
        language: str = "en",
    ) -> CulturalNarrative:
        """Generate immersive cultural narrative for a destination"""
        
        focus = focus_topics or ["history", "traditions", "arts", "cuisine", "festivals", "daily_life", "architecture", "nature"]
        
        prompt = f"""
You are a cultural anthropologist and master storyteller specializing in {destination_name}, {country}.
Create an immersive, authentic cultural narrative that helps travelers truly understand the soul of this place.

DESTINATION: {destination_name}
COUNTRY: {country}
{f"REGION: {region}" if region else ""}
{f"CITY: {city}" if city else ""}
FOCUS AREAS: {', '.join(focus)}
NARRATIVE LENGTH: {length}
LANGUAGE: {language}

REQUIREMENTS:
1. Write in an engaging, respectful, and culturally sensitive voice
2. Include specific historical details, not generic descriptions
3. Weave in local perspectives, legends, and oral traditions
4. Explain cultural significance of traditions, not just what they are
5. Include sensory details (sounds, smells, textures, colors)
6. Address the "why" behind cultural practices
7. Highlight what makes this place unique compared to similar destinations
8. Include practical cultural insights for respectful engagement
9. Avoid stereotypes and tourism clichés
10. If generating in a language other than English, ensure cultural nuance is preserved

STRUCTURE YOUR RESPONSE AS JSON with these fields:
- title: Engaging title for the narrative
- summary: 2-3 sentence hook
- full_narrative: The complete narrative (2-5 paragraphs for brief, 5-15 for detailed, 15+ for immersive)
- key_themes: List of 5-10 central cultural themes
- historical_period: Primary historical period(s) covered
- cultural_significance: Why this culture matters globally
- local_perspective: A voice from the community (fictional but authentic-sounding)
"""
        
        generation_config = GenerationConfig(
            temperature=0.8,
            top_p=0.9,
            top_k=40,
            max_output_tokens=8192,
            response_mime_type="application/json",
        )
        
        try:
            response = await self.model.generate_content_async(
                prompt,
                generation_config=generation_config,
            )
            return CulturalNarrative.model_validate_json(response.text)
        except Exception as e:
            logger.error("Failed to generate cultural narrative", error=str(e))
            raise
    
    async def recommend_destinations(
        self,
        user_interests: List[str],
        travel_style: str,
        budget_range: str,
        group_size: int,
        preferred_regions: Optional[List[str]] = None,
        trip_duration_days: Optional[int] = None,
        pace: str = "moderate",
        accessibility_needs: Optional[List[str]] = None,
        dietary_restrictions: Optional[List[str]] = None,
        language: str = "en",
        num_recommendations: int = 5,
    ) -> List[DestinationRecommendation]:
        """Generate personalized destination recommendations"""
        
        prompt = f"""
You are an expert cultural travel advisor with deep knowledge of global destinations.
Recommend {num_recommendations} destinations that perfectly match this traveler's profile.

TRAVELER PROFILE:
- Interests: {', '.join(user_interests)}
- Travel Style: {travel_style}
- Budget Range: {budget_range}
- Group Size: {group_size}
- Trip Duration: {f"{trip_duration_days} days" if trip_duration_days else "Flexible"}
- Pace: {pace}
- Accessibility Needs: {', '.join(accessibility_needs) if accessibility_needs else "None"}
- Dietary Restrictions: {', '.join(dietary_restrictions) if dietary_restrictions else "None"}
{f"- Preferred Regions: {', '.join(preferred_regions)}" if preferred_regions else ""}
- Language: {language}

REQUIREMENTS:
1. Recommend REAL destinations with genuine cultural depth
2. Prioritize places where travelers can have authentic cultural experiences
3. Include off-the-beaten-path gems alongside known destinations
4. Consider budget REALISTICALLY (local costs, not just tourist prices)
5. Match travel style to destination character
6. Consider group dynamics (solo, couple, family, friends)
7. Include cultural events/festivals timing if relevant
8. Provide specific, actionable reasons for each match
9. Estimate daily costs in USD for budget planning

RETURN JSON array of destinations with these fields:
- destination_name: Name of the destination
- country: Country
- region: Region/state/province (if applicable)
- city: Main city/base (if applicable)
- match_score: 0.0-1.0 how well it matches
- reasons: List of specific reasons (3-5)
- best_for: List of categories (cultural_immersion, food, history, nature, arts, spirituality, adventure, relaxation, community_connection)
- budget_level: budget, mid-range, luxury
- best_time_to_visit: Specific months/seasons with reasoning
- cultural_highlights: Top 5-7 cultural experiences not to miss
- hidden_gems_suggested: 3-5 specific hidden gems with brief descriptions
- estimated_daily_cost: {{"budget": X, "mid_range": Y, "luxury": Z}} in USD
"""
        
        generation_config = GenerationConfig(
            temperature=0.7,
            top_p=0.9,
            top_k=40,
            max_output_tokens=8192,
            response_mime_type="application/json",
        )
        
        try:
            response = await self.model.generate_content_async(
                prompt,
                generation_config=generation_config,
            )
            return [DestinationRecommendation.model_validate_json(r) for r in json.loads(response.text)]
        except Exception as e:
            logger.error("Failed to generate destination recommendations", error=str(e))
            raise
    
    async def generate_itinerary(
        self,
        destination: str,
        country: str,
        duration_days: int,
        travel_style: str,
        budget_range: str,
        group_size: int,
        interests: List[str],
        pace: str = "moderate",
        start_date: Optional[str] = None,
        special_requirements: Optional[str] = None,
        language: str = "en",
    ) -> FullItinerary:
        """Generate detailed cultural itinerary"""
        
        prompt = f"""
You are a master cultural itinerary designer. Create a deeply meaningful, day-by-day itinerary 
that transforms a trip into a cultural journey.

TRIP PARAMETERS:
- Destination: {destination}, {country}
- Duration: {duration_days} days
- Travel Style: {travel_style}
- Budget: {budget_range}
- Group Size: {group_size}
- Interests: {', '.join(interests)}
- Pace: {pace}
{f"- Start Date: {start_date}" if start_date else ""}
{f"- Special Requirements: {special_requirements}" if special_requirements else ""}
- Language: {language}

REQUIREMENTS:
1. Each day must have a coherent cultural theme
2. Balance famous sites with hidden gems and local experiences
3. Include cultural storytelling at each stop - WHY it matters
4. Schedule realistic timing with buffer for serendipity
5. Mix activity types: observation, participation, learning, reflection
6. Include meals at culturally significant places (not just "good restaurants")
7. Suggest authentic local interactions (workshops, home visits, ceremonies)
8. Provide cultural context for every recommendation
9. Include practical logistics (transport, timing, reservations needed)
9. Add cultural etiquette for each activity
10. Estimate costs per day
11. Include evening cultural options
12. Build in reflection/journaling prompts
13. Consider group dynamics in scheduling

RETURN JSON with these fields:
- trip_title: Inspiring title for the journey
- destination: {destination}, {country}
- duration_days: {duration_days}
- travel_style: {travel_style}
- budget_range: {budget_range}
- group_size: {group_size}
- overview: 2-3 paragraph trip overview
- cultural_context: Essential cultural background for the traveler
- days: Array of day objects with:
  - day_number: 1-{duration_days}
  - date: ISO date if start_date provided
  - title: Day theme title
  - theme: Cultural theme (e.g., "Living History", "Sacred Spaces", "Flavors of Tradition")
  - narrative: Immersive day narrative (2-3 paragraphs)
  - activities: Array of activity objects with:
    - time: "HH:MM" or "morning/afternoon/evening"
    - type: destination/experience/hidden_gem/event/cuisine/transit/free_time/meal/accommodation
    - title: Activity name
    - description: What happens
    - location: Specific place/area
    - cultural_context: Why this matters culturally
    - duration_minutes: Estimated duration
    - cost_estimate_usd: Estimated cost
    - transport_from_previous: How to get there
    - cultural_etiquette: Specific dos/don'ts
    - reflection_prompt: Question for journaling
  - cultural_insights: Key cultural learnings for the day
  - estimated_cost: Total day estimate in USD
  - transport_notes: Getting around that day
- practical_tips: 10-15 essential practical tips
- packing_suggestions: Culturally appropriate packing list
- cultural_etiquette: Top 10 cultural etiquette rules
- emergency_info: {{"embassy": "...", "emergency_number": "...", "health": "..."}}
"""
        
        generation_config = GenerationConfig(
            temperature=0.75,
            top_p=0.9,
            top_k=40,
            max_output_tokens=8192,
            response_mime_type="application/json",
        )
        
        try:
            response = await self.model.generate_content_async(
                prompt,
                generation_config=generation_config,
            )
            return FullItinerary.model_validate_json(response.text)
        except Exception as e:
            logger.error("Failed to generate itinerary", error=str(e))
            raise
    
    async def discover_hidden_gems(
        self,
        destination: str,
        country: str,
        known_places: Optional[List[str]] = None,
        interest_areas: Optional[List[str]] = None,
        num_gems: int = 5,
        language: str = "en",
    ) -> List[HiddenGemRecommendation]:
        """Discover hidden cultural gems"""
        
        prompt = f"""
You are a local cultural insider revealing secret treasures of {destination}, {country}.
Share {num_gems} genuine hidden gems that tourists rarely discover but locals cherish.

DESTINATION: {destination}, {country}
{f"ALREADY KNOWN: {', '.join(known_places)}" if known_places else ""}
{f"INTEREST AREAS: {', '.join(interest_areas)}" if interest_areas else ""}
LANGUAGE: {language}

REQUIREMENTS:
1. These MUST be real places, not fictional
2. Include specific location hints (neighborhood, landmark proximity) but NOT exact coordinates
3. Explain WHY each is culturally significant
4. Share authentic local stories/legends associated
5. Describe the experience of visiting (sensory, emotional)
6. Include practical access information
7. Reveal what makes each place special to locals
8. Provide insider tips only locals would know
9. Respect sacred/private spaces - only include publicly accessible gems
10. Vary types: natural, architectural, culinary, social, spiritual, artistic

RETURN JSON array with these fields:
- name: Local name (with English translation)
- description: Vivid description of the place
- location_hint: General area description for finding it
- cultural_significance: Why it matters to the culture
- local_story: Legend, history, or personal story
- best_time_to_visit: Specific time (season, time of day, festival)
- access_difficulty: easy/moderate/hard with explanation
- visit_duration_hours: Realistic time needed
- what_makes_it_special: The unique essence
- local_tips: 3-5 insider tips
"""
        
        generation_config = GenerationConfig(
            temperature=0.8,
            top_p=0.9,
            top_k=40,
            max_output_tokens=8192,
            response_mime_type="application/json",
        )
        
        try:
            response = await self.model.generate_content_async(
                prompt,
                generation_config=generation_config,
            )
            return [HiddenGemRecommendation.model_validate_json(r) for r in json.loads(response.text)]
        except Exception as e:
            logger.error("Failed to discover hidden gems", error=str(e))
            raise
    
    async def generate_cultural_event_insight(
        self,
        event_name: str,
        destination: str,
        country: str,
        event_type: str,
        date_context: str,
        language: str = "en",
    ) -> CulturalEventInsight:
        """Generate deep cultural insight for an event/festival"""
        
        prompt = f"""
You are a cultural historian and local festival expert. Provide deep cultural insight for this event.

EVENT: {event_name}
LOCATION: {destination}, {country}
EVENT TYPE: {event_type}
DATE CONTEXT: {date_context}
LANGUAGE: {language}

REQUIREMENTS:
1. Explain the DEEP cultural significance, not just surface description
2. Share historical origins and evolution
3. Detail specific traditions, rituals, and their meanings
4. Describe what a visitor will experience (all senses)
5. Provide SPECIFIC visitor etiquette (not generic "be respectful")
6. Include dress code with cultural reasoning
7. Explain HOW to participate meaningfully (not just observe)
8. Share a local's perspective on what the event means to them
9. Include practical info: timing, tickets, transport, facilities
10. Address photography rules, gender considerations, sacred elements

RETURN JSON with these fields:
- event_name: {event_name}
- cultural_significance: Deep cultural meaning
- history_and_origins: Historical background
- traditions_and_rituals: List of specific traditions with explanations
- what_to_expect: Sensory, emotional experience description
- visitor_etiquette: Specific dos and don'ts with cultural reasons
- dress_code: Specific requirements with cultural context
- best_way_to_participate: How to engage meaningfully
- local_perspective: First-person local voice
- practical_info: {{"dates": "...", "tickets": "...", "transport": "...", "facilities": "...", "photography": "..."}}
"""
        
        generation_config = GenerationConfig(
            temperature=0.75,
            top_p=0.9,
            top_k=40,
            max_output_tokens=8192,
            response_mime_type="application/json",
        )
        
        try:
            response = await self.model.generate_content_async(
                prompt,
                generation_config=generation_config,
            )
            return CulturalEventInsight.model_validate_json(response.text)
        except Exception as e:
            logger.error("Failed to generate cultural event insight", error=str(e))
            raise
    
    async def generate_cuisine_insight(
        self,
        dish_name: str,
        destination: str,
        country: str,
        cuisine_type: str,
        language: str = "en",
    ) -> CuisineInsight:
        """Generate deep cultural insight for a dish/cuisine"""
        
        prompt = f"""
You are a culinary anthropologist and local food expert. Reveal the cultural soul of this dish.

DISH: {dish_name}
LOCATION: {destination}, {country}
CUISINE TYPE: {cuisine_type}
LANGUAGE: {language}

REQUIREMENTS:
1. Explain cultural significance beyond "it's delicious"
2. Share history - origins, evolution, historical context
3. Identify specific region/community of origin
4. Explain traditional occasions (festivals, daily life, ceremonies)
5. List KEY ingredients with cultural context (not just ingredients)
6. Describe preparation highlights - techniques, tools, rituals
7. Articulate flavor profile in cultural terms
8. Suggest traditional pairings (drinks, sides, sequence)
9. Guide to finding AUTHENTIC versions (not tourist versions)
10. Share local eating customs for this dish

RETURN JSON with these fields:
- dish_name: {dish_name}
- description: Vivid, sensory description
- cultural_significance: Why this dish matters to the culture
- history: Historical origins and evolution
- region_of_origin: Specific region/community
- traditional_occation: When traditionally eaten
- key_ingredients: List with cultural context for each
- preparation_highlights: Techniques, tools, rituals
- flavor_profile: Cultural flavor description
- pairing_suggestions: Traditional pairings
- where_to_find_authentic_version: Specific guidance
- local_eating_customs: How locals eat this dish
"""
        
        generation_config = GenerationConfig(
            temperature=0.75,
            top_p=0.9,
            top_k=40,
            max_output_tokens=8192,
            response_mime_type="application/json",
        )
        
        try:
            response = await self.model.generate_content_async(
                prompt,
                generation_config=generation_config,
            )
            return CuisineInsight.model_validate_json(response.text)
        except Exception as e:
            logger.error("Failed to generate cuisine insight", error=str(e))
            raise
    
    async def generate_experience_insight(
        self,
        experience_name: str,
        experience_type: str,
        destination: str,
        country: str,
        host_info: Optional[str] = None,
        language: str = "en",
    ) -> ExperienceInsight:
        """Generate deep cultural insight for an experience"""
        
        prompt = f"""
You are a cultural experience curator and community liaison. Reveal the depth of this experience.

EXPERIENCE: {experience_name}
TYPE: {experience_type}
LOCATION: {destination}, {country}
{f"HOST INFO: {host_info}" if host_info else ""}
LANGUAGE: {language}

REQUIREMENTS:
1. Explain what tradition/skill/culture is being preserved
2. Describe the community impact (economic, cultural, social)
3. Detail what participants actually DO (not just watch)
4. Share preparation tips for meaningful engagement
5. Provide local insights only insiders know
6. Explain WHY this experience matters - to the culture, to the visitor
7. Address cultural sensitivity - what NOT to do
8. Include the host/community perspective
9. Describe the emotional/transformative potential
10. Practical guidance for respectful participation

RETURN JSON with these fields:
- experience_name: {experience_name}
- experience_type: {experience_type}
- description: What the experience entails
- cultural_significance: What culture/tradition this preserves
- tradition_preserved: Specific tradition/skill/knowledge
- community_impact: How this supports the community
- what_to_expect: Step-by-step participant journey
- preparation_tips: 5-7 specific preparation tips
- local_insights: Insider knowledge
- why_it_matters: The deeper significance
"""
        
        generation_config = GenerationConfig(
            temperature=0.75,
            top_p=0.9,
            top_k=40,
            max_output_tokens=8192,
            response_mime_type="application/json",
        )
        
        try:
            response = await self.model.generate_content_async(
                prompt,
                generation_config=generation_config,
            )
            return ExperienceInsight.model_validate_json(response.text)
        except Exception as e:
            logger.error("Failed to generate experience insight", error=str(e))
            raise
    
    async def chat_with_travel_companion(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]],
        trip_context: Optional[Dict[str, Any]] = None,
        user_profile: Optional[Dict[str, Any]] = None,
        language: str = "en",
    ) -> ChatResponse:
        """Chat with the AI cultural travel companion"""
        
        system_prompt = """You are an AI Cultural Travel Companion - a knowledgeable, warm, and culturally sensitive guide who helps travelers discover the soul of places through authentic cultural experiences.

YOUR PERSONA:
- Deep cultural knowledge across global destinations
- Respectful, nuanced, never stereotypical
- Practical yet poetic - you inspire AND inform
- You ask clarifying questions when needed
- You remember conversation context
- You connect recommendations to the traveler's unique profile
- You prioritize authentic experiences over tourist traps
- You explain cultural WHY, not just WHAT
- You're honest about challenges and considerations

CAPABILITIES:
- Destination recommendations with cultural depth
- Itinerary planning with cultural narratives
- Hidden gem discovery
- Cultural event/festival insights
- Cuisine and food culture guidance
- Authentic experience matching
- Cultural etiquette and preparation
- Real-time travel assistance
- Storytelling and cultural context

GUIDELINES:
- Always be culturally respectful and accurate
- Distinguish between tourist experiences and authentic cultural engagement
- Acknowledge when you don't know something specific
- Encourage respectful, reciprocal cultural exchange
- Consider accessibility, budget, and practical constraints
- Connect suggestions to the traveler's stated interests"""

        if trip_context:
            system_prompt += f"\n\nCURRENT TRIP CONTEXT:\n{json.dumps(trip_context, indent=2)}"
        
        if user_profile:
            system_prompt += f"\n\nTRAVELER PROFILE:\n{json.dumps(user_profile, indent=2)}"
        
        # Build conversation
        messages = [{"role": "user", "parts": [system_prompt]}]
        
        for msg in conversation_history[-10:]:  # Last 10 messages
            role = "model" if msg["role"] == "assistant" else "user"
            messages.append({"role": role, "parts": [msg["content"]]})
        
        messages.append({"role": "user", "parts": [user_message]})
        
        generation_config = GenerationConfig(
            temperature=0.8,
            top_p=0.9,
            top_k=40,
            max_output_tokens=4096,
        )
        
        try:
            response = await self.model.generate_content_async(
                messages,
                generation_config=generation_config,
            )
            
            return ChatResponse(
                content=response.text,
                function_calls=None,
                referenced_content=None,
            )
        except Exception as e:
            logger.error("Failed to generate chat response", error=str(e))
            raise


# Singleton instance
gemini_service = GeminiService()