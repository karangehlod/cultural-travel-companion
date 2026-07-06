"""
Google Maps API Service
"""
import httpx
from typing import Optional, List, Dict, Any, Tuple
from pydantic import BaseModel

from app.core.config import settings


class GeocodeResult(BaseModel):
    place_id: str
    formatted_address: str
    location: Dict[str, float]  # lat, lng
    address_components: List[Dict[str, Any]]
    types: List[str]
    bounds: Optional[Dict[str, Any]] = None


class DirectionsResult(BaseModel):
    routes: List[Dict[str, Any]]
    waypoints: List[Dict[str, Any]]


class DistanceMatrixResult(BaseModel):
    origin: str
    destination: str
    distance: Dict[str, Any]  # text, value (meters)
    duration: Dict[str, Any]  # text, value (seconds)
    duration_in_traffic: Optional[Dict[str, Any]] = None


class GoogleMapsService:
    """Service for interacting with Google Maps API (Geocoding, Directions, etc.)"""
    
    def __init__(self):
        self.api_key = settings.GOOGLE_MAPS_API_KEY or settings.GOOGLE_API_KEY
        self.base_url = "https://maps.googleapis.com/maps/api"
        self._client: Optional[httpx.AsyncClient] = None
    
    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=30.0)
        return self._client
    
    async def close(self):
        if self._client:
            await self._client.aclose()
            self._client = None
    
    async def geocode(
        self,
        address: str,
        language: str = "en",
        region: Optional[str] = None,
        components: Optional[str] = None,
    ) -> List[GeocodeResult]:
        """Convert address to coordinates"""
        client = await self._get_client()
        
        params = {
            "address": address,
            "key": self.api_key,
            "language": language,
        }
        
        if region:
            params["region"] = region
        if components:
            params["components"] = components
        
        response = await client.get(
            f"{self.base_url}/geocode/json",
            params=params,
        )
        
        if response.status_code != 200:
            raise Exception(f"Geocoding API error: {response.status_code} - {response.text}")
        
        data = response.json()
        
        if data.get("status") != "OK":
            raise Exception(f"Geocoding API status: {data.get('status')} - {data.get('error_message', '')}")
        
        results = []
        for result in data.get("results", []):
            location = result.get("geometry", {}).get("location", {})
            results.append(GeocodeResult(
                place_id=result.get("place_id", ""),
                formatted_address=result.get("formatted_address", ""),
                location={"lat": location.get("lat", 0), "lng": location.get("lng", 0)},
                address_components=result.get("address_components", []),
                types=result.get("types", []),
                bounds=result.get("geometry", {}).get("bounds"),
            ))
        
        return results
    
    async def reverse_geocode(
        self,
        lat: float,
        lng: float,
        language: str = "en",
        result_type: Optional[str] = None,
        location_type: Optional[str] = None,
    ) -> List[GeocodeResult]:
        """Convert coordinates to address"""
        client = await self._get_client()
        
        params = {
            "latlng": f"{lat},{lng}",
            "key": self.api_key,
            "language": language,
        }
        
        if result_type:
            params["result_type"] = result_type
        if location_type:
            params["location_type"] = location_type
        
        response = await client.get(
            f"{self.base_url}/geocode/json",
            params=params,
        )
        
        if response.status_code != 200:
            raise Exception(f"Reverse Geocoding API error: {response.status_code} - {response.text}")
        
        data = response.json()
        
        if data.get("status") != "OK":
            raise Exception(f"Reverse Geocoding API status: {data.get('status')} - {data.get('error_message', '')}")
        
        results = []
        for result in data.get("results", []):
            location = result.get("geometry", {}).get("location", {})
            results.append(GeocodeResult(
                place_id=result.get("place_id", ""),
                formatted_address=result.get("formatted_address", ""),
                location={"lat": location.get("lat", 0), "lng": location.get("lng", 0)},
                address_components=result.get("address_components", []),
                types=result.get("types", []),
                bounds=result.get("geometry", {}).get("bounds"),
            ))
        
        return results
    
    async def get_directions(
        self,
        origin: str,  # "lat,lng" or address
        destination: str,
        mode: str = "driving",  # driving, walking, bicycling, transit
        waypoints: Optional[List[str]] = None,
        alternatives: bool = True,
        avoid: Optional[str] = None,  # tolls, highways, ferries, indoor
        language: str = "en",
        units: str = "metric",
        departure_time: Optional[str] = None,  # "now" or timestamp
        arrival_time: Optional[str] = None,
        transit_mode: Optional[str] = None,  # bus, subway, train, tram, rail
        transit_routing_preference: Optional[str] = None,  # less_walking, fewer_transfers
    ) -> DirectionsResult:
        """Get directions between locations"""
        client = await self._get_client()
        
        params = {
            "origin": origin,
            "destination": destination,
            "mode": mode,
            "alternatives": "true" if alternatives else "false",
            "key": self.api_key,
            "language": language,
            "units": units,
        }
        
        if waypoints:
            params["waypoints"] = "|".join(waypoints)
        if avoid:
            params["avoid"] = avoid
        if departure_time:
            params["departure_time"] = departure_time
        if arrival_time:
            params["arrival_time"] = arrival_time
        if transit_mode:
            params["transit_mode"] = transit_mode
        if transit_routing_preference:
            params["transit_routing_preference"] = transit_routing_preference
        
        response = await client.get(
            f"{self.base_url}/directions/json",
            params=params,
        )
        
        if response.status_code != 200:
            raise Exception(f"Directions API error: {response.status_code} - {response.text}")
        
        data = response.json()
        
        if data.get("status") not in ["OK", "ZERO_RESULTS"]:
            raise Exception(f"Directions API status: {data.get('status')} - {data.get('error_message', '')}")
        
        return DirectionsResult(
            routes=data.get("routes", []),
            waypoints=data.get("geocoded_waypoints", []),
        )
    
    async def get_distance_matrix(
        self,
        origins: List[str],  # List of "lat,lng" or addresses
        destinations: List[str],
        mode: str = "driving",
        avoid: Optional[str] = None,
        language: str = "en",
        units: str = "metric",
        departure_time: Optional[str] = None,
        arrival_time: Optional[str] = None,
        transit_mode: Optional[str] = None,
        transit_routing_preference: Optional[str] = None,
    ) -> List[DistanceMatrixResult]:
        """Get distance and duration between multiple origins and destinations"""
        client = await self._get_client()
        
        params = {
            "origins": "|".join(origins),
            "destinations": "|".join(destinations),
            "mode": mode,
            "key": self.api_key,
            "language": language,
            "units": units,
        }
        
        if avoid:
            params["avoid"] = avoid
        if departure_time:
            params["departure_time"] = departure_time
        if arrival_time:
            params["arrival_time"] = arrival_time
        if transit_mode:
            params["transit_mode"] = transit_mode
        if transit_routing_preference:
            params["transit_routing_preference"] = transit_routing_preference
        
        response = await client.get(
            f"{self.base_url}/distancematrix/json",
            params=params,
        )
        
        if response.status_code != 200:
            raise Exception(f"Distance Matrix API error: {response.status_code} - {response.text}")
        
        data = response.json()
        
        if data.get("status") != "OK":
            raise Exception(f"Distance Matrix API status: {data.get('status')} - {data.get('error_message', '')}")
        
        results = []
        rows = data.get("rows", [])
        for i, row in enumerate(rows):
            origin = data.get("origin_addresses", [])[i] if i < len(data.get("origin_addresses", [])) else origins[i]
            elements = row.get("elements", [])
            for j, element in enumerate(elements):
                destination = data.get("destination_addresses", [])[j] if j < len(data.get("destination_addresses", [])) else destinations[j]
                if element.get("status") == "OK":
                    results.append(DistanceMatrixResult(
                        origin=origin,
                        destination=destination,
                        distance=element.get("distance", {}),
                        duration=element.get("duration", {}),
                        duration_in_traffic=element.get("duration_in_traffic"),
                    ))
        
        return results
    
    async def get_elevation(
        self,
        locations: List[Tuple[float, float]],  # List of (lat, lng)
        samples: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Get elevation for locations"""
        client = await self._get_client()
        
        locations_str = "|".join([f"{lat},{lng}" for lat, lng in locations])
        
        params = {
            "locations": locations_str,
            "key": self.api_key,
        }
        
        if samples:
            params["samples"] = samples
        
        response = await client.get(
            f"{self.base_url}/elevation/json",
            params=params,
        )
        
        if response.status_code != 200:
            raise Exception(f"Elevation API error: {response.status_code} - {response.text}")
        
        data = response.json()
        
        if data.get("status") != "OK":
            raise Exception(f"Elevation API status: {data.get('status')} - {data.get('error_message', '')}")
        
        return data.get("results", [])
    
    async def get_timezone(
        self,
        lat: float,
        lng: float,
        timestamp: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get timezone for a location"""
        client = await self._get_client()
        
        params = {
            "location": f"{lat},{lng}",
            "key": self.api_key,
        }
        
        if timestamp:
            params["timestamp"] = timestamp
        
        response = await client.get(
            f"{self.base_url}/timezone/json",
            params=params,
        )
        
        if response.status_code != 200:
            raise Exception(f"Timezone API error: {response.status_code} - {response.text}")
        
        data = response.json()
        
        if data.get("status") != "OK":
            raise Exception(f"Timezone API status: {data.get('status')} - {data.get('error_message', '')}")
        
        return data


# Singleton instance
google_maps_service = GoogleMapsService()