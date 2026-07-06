"""
Google Places API Service
"""
import httpx
import json
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

from app.core.config import settings


class PlaceSearchResult(BaseModel):
    place_id: str
    name: str
    formatted_address: str
    location: Dict[str, float]  # lat, lng
    types: List[str]
    rating: Optional[float] = None
    user_ratings_total: Optional[int] = None
    price_level: Optional[int] = None
    photos: Optional[List[Dict[str, Any]]] = None
    opening_hours: Optional[Dict[str, Any]] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    editorial_summary: Optional[str] = None


class PlaceDetailsResult(BaseModel):
    place_id: str
    name: str
    formatted_address: str
    location: Dict[str, float]
    types: List[str]
    rating: Optional[float] = None
    user_ratings_total: Optional[int] = None
    price_level: Optional[int] = None
    photos: Optional[List[Dict[str, Any]]] = None
    opening_hours: Optional[Dict[str, Any]] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    editorial_summary: Optional[str] = None
    reviews: Optional[List[Dict[str, Any]]] = None
    wheelchair_accessible_entrance: Optional[bool] = None
    takes_reservations: Optional[bool] = None
    delivery: Optional[bool] = None
    dine_in: Optional[bool] = None
    outdoor_seating: Optional[bool] = None
    live_music: Optional[bool] = None
    good_for_children: Optional[bool] = None
    good_for_groups: Optional[bool] = None
    restroom: Optional[bool] = None


class GooglePlacesService:
    """Service for interacting with Google Places API (New)"""
    
    def __init__(self):
        self.api_key = settings.GOOGLE_PLACES_API_KEY or settings.GOOGLE_API_KEY
        self.base_url = "https://places.googleapis.com/v1"
        self.headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self.api_key,
            "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.location,places.types,places.rating,places.userRatingCount,places.priceLevel,places.photos,places.regularOpeningHours,places.websiteUri,places.nationalPhoneNumber,places.editorialSummary,places.reviews,places.accessibilityOptions",
        }
        self._client: Optional[httpx.AsyncClient] = None
    
    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=30.0)
        return self._client
    
    async def close(self):
        if self._client:
            await self._client.aclose()
            self._client = None
    
    async def search_nearby(
        self,
        lat: float,
        lng: float,
        radius: int = 5000,
        included_types: Optional[List[str]] = None,
        excluded_types: Optional[List[str]] = None,
        max_results: int = 20,
        rank_preference: str = "RELEVANCE",
    ) -> List[PlaceSearchResult]:
        """Search for places near a location"""
        client = await self._get_client()
        
        body = {
            "locationRestriction": {
                "circle": {
                    "center": {"latitude": lat, "longitude": lng},
                    "radius": radius,
                }
            },
            "maxResultCount": max_results,
            "rankPreference": rank_preference,
        }
        
        if included_types:
            body["includedTypes"] = included_types
        if excluded_types:
            body["excludedTypes"] = excluded_types
        
        response = await client.post(
            f"{self.base_url}/places:searchNearby",
            headers=self.headers,
            json=body,
        )
        
        if response.status_code != 200:
            raise Exception(f"Places API error: {response.status_code} - {response.text}")
        
        data = response.json()
        places = []
        for place in data.get("places", []):
            places.append(self._parse_place_search_result(place))
        
        return places
    
    async def search_text(
        self,
        text_query: str,
        lat: Optional[float] = None,
        lng: Optional[float] = None,
        radius: Optional[int] = None,
        included_types: Optional[List[str]] = None,
        max_results: int = 20,
    ) -> List[PlaceSearchResult]:
        """Search for places by text query"""
        client = await self._get_client()
        
        body = {
            "textQuery": text_query,
            "maxResultCount": max_results,
        }
        
        if lat is not None and lng is not None and radius:
            body["locationBias"] = {
                "circle": {
                    "center": {"latitude": lat, "longitude": lng},
                    "radius": radius,
                }
            }
        
        if included_types:
            body["includedTypes"] = included_types
        
        response = await client.post(
            f"{self.base_url}/places:searchText",
            headers=self.headers,
            json=body,
        )
        
        if response.status_code != 200:
            raise Exception(f"Places API error: {response.status_code} - {response.text}")
        
        data = response.json()
        places = []
        for place in data.get("places", []):
            places.append(self._parse_place_search_result(place))
        
        return places
    
    async def get_place_details(
        self,
        place_id: str,
        field_mask: Optional[str] = None,
    ) -> PlaceDetailsResult:
        """Get detailed information about a place"""
        client = await self._get_client()
        
        headers = self.headers.copy()
        if field_mask:
            headers["X-Goog-FieldMask"] = field_mask
        
        response = await client.get(
            f"{self.base_url}/places/{place_id}",
            headers=headers,
        )
        
        if response.status_code != 200:
            raise Exception(f"Places API error: {response.status_code} - {response.text}")
        
        data = response.json()
        return self._parse_place_details_result(data)
    
    async def get_place_photos(
        self,
        place_id: str,
        max_photos: int = 10,
    ) -> List[Dict[str, Any]]:
        """Get photos for a place"""
        client = await self._get_client()
        
        response = await client.get(
            f"{self.base_url}/places/{place_id}/photos",
            headers=self.headers,
            params={"maxResults": max_photos},
        )
        
        if response.status_code != 200:
            raise Exception(f"Places Photos API error: {response.status_code} - {response.text}")
        
        data = response.json()
        return data.get("photos", [])
    
    async def get_photo_url(
        self,
        photo_name: str,
        max_width: int = 800,
        max_height: int = 800,
    ) -> str:
        """Get a photo URL"""
        return f"{self.base_url}/{photo_name}/media?key={self.api_key}&maxWidthPx={max_width}&maxHeightPx={max_height}"
    
    async def search_cultural_places(
        self,
        lat: float,
        lng: float,
        radius: int = 10000,
    ) -> List[PlaceSearchResult]:
        """Search for culturally significant places"""
        cultural_types = [
            "museum", "art_gallery", "library", "university", "school",
            "church", "temple", "mosque", "synagogue", "hindu_temple",
            "tourist_attraction", "point_of_interest", "historical_landmark",
            "monument", "cultural_center", "performing_arts_theater",
            "amphitheatre", "stadium", "aquarium", "zoo", "botanical_garden",
            "park", "natural_feature", "campground", "rv_park",
        ]
        
        return await self.search_nearby(
            lat=lat,
            lng=lng,
            radius=radius,
            included_types=cultural_types,
            max_results=50,
            rank_preference="RELEVANCE",
        )
    
    async def search_food_places(
        self,
        lat: float,
        lng: float,
        radius: int = 5000,
    ) -> List[PlaceSearchResult]:
        """Search for food and dining places"""
        food_types = [
            "restaurant", "cafe", "bakery", "bar", "pub", "night_club",
            "meal_takeaway", "meal_delivery", "food_court", "market",
            "grocery_or_supermarket", "convenience_store", "liquor_store",
        ]
        
        return await self.search_nearby(
            lat=lat,
            lng=lng,
            radius=radius,
            included_types=food_types,
            max_results=30,
            rank_preference="RELEVANCE",
        )
    
    async def search_accommodation(
        self,
        lat: float,
        lng: float,
        radius: int = 10000,
    ) -> List[PlaceSearchResult]:
        """Search for accommodation places"""
        accommodation_types = [
            "lodging", "hotel", "motel", "hostel", "campground", "rv_park",
            "bed_and_breakfast", "guest_house", "inn", "resort_hotel",
        ]
        
        return await self.search_nearby(
            lat=lat,
            lng=lng,
            radius=radius,
            included_types=accommodation_types,
            max_results=30,
            rank_preference="RELEVANCE",
        )
    
    def _parse_place_search_result(self, place: Dict[str, Any]) -> PlaceSearchResult:
        location = place.get("location", {})
        return PlaceSearchResult(
            place_id=place.get("id", ""),
            name=place.get("displayName", {}).get("text", ""),
            formatted_address=place.get("formattedAddress", ""),
            location={"lat": location.get("latitude", 0), "lng": location.get("longitude", 0)},
            types=place.get("types", []),
            rating=place.get("rating"),
            user_ratings_total=place.get("userRatingCount"),
            price_level=place.get("priceLevel"),
            photos=place.get("photos"),
            opening_hours=place.get("regularOpeningHours"),
            website=place.get("websiteUri"),
            phone=place.get("nationalPhoneNumber"),
            editorial_summary=place.get("editorialSummary", {}).get("text") if place.get("editorialSummary") else None,
        )
    
    def _parse_place_details_result(self, place: Dict[str, Any]) -> PlaceDetailsResult:
        location = place.get("location", {})
        photos = place.get("photos", [])
        opening_hours = place.get("regularOpeningHours", {})
        reviews = place.get("reviews", [])
        accessibility = place.get("accessibilityOptions", {})
        
        return PlaceDetailsResult(
            place_id=place.get("id", ""),
            name=place.get("displayName", {}).get("text", ""),
            formatted_address=place.get("formattedAddress", ""),
            location={"lat": location.get("latitude", 0), "lng": location.get("longitude", 0)},
            types=place.get("types", []),
            rating=place.get("rating"),
            user_ratings_total=place.get("userRatingCount"),
            price_level=place.get("priceLevel"),
            photos=photos,
            opening_hours=opening_hours,
            website=place.get("websiteUri"),
            phone=place.get("nationalPhoneNumber"),
            editorial_summary=place.get("editorialSummary", {}).get("text") if place.get("editorialSummary") else None,
            reviews=reviews,
            wheelchair_accessible_entrance=accessibility.get("wheelchairAccessibleEntrance"),
            takes_reservations=place.get("takesReservations"),
            delivery=place.get("delivery"),
            dine_in=place.get("dineIn"),
            outdoor_seating=place.get("outdoorSeating"),
            live_music=place.get("liveMusic"),
            good_for_children=place.get("goodForChildren"),
            good_for_groups=place.get("goodForGroups"),
            restroom=place.get("restroom"),
        )


# Singleton instance
google_places_service = GooglePlacesService()