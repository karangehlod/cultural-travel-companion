'use client';

import Link from 'next/link';
import { 
  Globe, 
  Calendar, 
  MapPin, 
  Clock, 
  DollarSign,
  Utensils,
  Home,
  BookOpen,
  Sparkles,
  ArrowRight,
  ChevronDown,
  ChevronUp,
  Star,
  Heart,
  Map,
  Sun
} from 'lucide-react';

const mockItineraries = [
  {
    id: '1',
    title: '7-Day Soul of Kyoto Journey',
    destination: 'Kyoto, Japan',
    duration: '7 days',
    price: 2450,
    rating: 4.9,
    image: 'https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=800',
    themes: ['Temples', 'Tea Ceremony', 'Zen Gardens', 'Geisha Culture'],
    pace: 'Relaxed',
    groupSize: 'Small (4-8)',
  },
  {
    id: '2',
    title: 'Oaxaca Culinary & Cultural Immersion',
    destination: 'Oaxaca, Mexico',
    duration: '8 days',
    price: 2850,
    rating: 4.8,
    image: 'https://images.unsplash.com/photo-1583417377828-1a1a1a1a1a1a?w=800',
    themes: ['Mole Making', 'Markets', 'Mezcal', 'Day of the Dead'],
    pace: 'Moderate',
    groupSize: 'Small (6-10)',
  },
  {
    id: '3',
    title: 'Fez Medina & Atlas Mountains',
    destination: 'Fez, Morocco',
    duration: '9 days',
    price: 3200,
    rating: 4.9,
    image: 'https://images.unsplash.com/photo-1544717305-2782549b5136?w=800',
    themes: ['Medina Crafts', 'Berber Villages', 'Sahara Desert', 'Sufi Music'],
    pace: 'Active',
    groupSize: 'Small (4-8)',
  },
  {
    id: '4',
    title: 'Luang Prabang Spiritual Journey',
    destination: 'Luang Prabang, Laos',
    duration: '6 days',
    price: 1850,
    rating: 4.8,
    image: 'https://images.unsplash.com/photo-1528181304800-259b08848526?w=800',
    themes: ['Alms Giving', 'Buddhist Temples', 'Mekong River', 'Waterfalls'],
    pace: 'Relaxed',
    groupSize: 'Small (4-8)',
  },
  {
    id: '5',
    title: 'Cusco & Sacred Valley Explorer',
    destination: 'Cusco, Peru',
    duration: '8 days',
    price: 2650,
    rating: 4.7,
    image: 'https://images.unsplash.com/photo-1587595431973-160d0d94add1?w=800',
    themes: ['Inca Ruins', 'Weaving', 'Machu Picchu', 'Andean Culture'],
    pace: 'Moderate',
    groupSize: 'Small (6-10)',
  },
  {
    id: '6',
    title: 'Varanasi Spiritual Awakening',
    destination: 'Varanasi, India',
    duration: '5 days',
    price: 1650,
    rating: 4.9,
    image: 'https://images.unsplash.com/photo-1561361512-4c17431f7e1a?w=800',
    themes: ['Ganges Rituals', 'Temples', 'Classical Music', 'Silk Weaving'],
    pace: 'Relaxed',
    groupSize: 'Small (4-8)',
  },
];

export default function ItinerariesPage() {
  return (
    <div className="min-h-screen bg-background">
      <nav className="fixed top-0 left-0 right-0 z-50 bg-background/95 backdrop-blur-sm border-b border-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <Link href="/" className="flex items-center gap-2">
              <Globe className="w-8 h-8 text-primary" />
              <span className="font-playfair text-2xl font-bold text-foreground">CultureCompass</span>
            </Link>
            <div className="flex items-center gap-4">
              <Link href="/" className="text-sm font-medium text-muted-foreground hover:text-foreground">Home</Link>
              <Link href="/destinations" className="text-sm font-medium text-muted-foreground hover:text-foreground">Destinations</Link>
              <Link href="/experiences" className="text-sm font-medium text-muted-foreground hover:text-foreground">Experiences</Link>
              <Link href="/auth/login" className="px-4 py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:bg-primary/90">Sign In</Link>
            </div>
          </div>
        </div>
      </nav>

      <main className="pt-24 pb-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h1 className="font-playfair text-4xl sm:text-5xl font-bold text-foreground mb-6">
              Curated Cultural Itineraries
            </h1>
            <p className="text-lg text-muted-foreground max-w-3xl mx-auto">
              Hand-crafted journeys with day-by-day cultural narratives, authentic experiences, and local expert guides. 
              Every itinerary includes cultural etiquette, reflection prompts, and insider access.
            </p>
          </div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {mockItineraries.map((itinerary, index) => (
              <Link
                key={itinerary.id}
                href={`/itineraries/${itinerary.id}`}
                className="group cultural-card overflow-hidden rounded-2xl bg-card border border-border"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <div className="relative h-56 overflow-hidden">
                  <img
                    src={itinerary.image}
                    alt={itinerary.title}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-black/20 to-transparent" />
                  <div className="absolute bottom-4 left-4 right-4 text-white">
                    <span className="inline-flex items-center gap-1 px-3 py-1 bg-white/20 backdrop-blur-sm rounded-full text-sm font-medium">
                      <MapPin className="w-3 h-3" />
                      {itinerary.destination.split(',')[0]}
                    </span>
                    <div className="absolute bottom-4 right-4">
                      <div className="flex items-center gap-1 bg-white/20 backdrop-blur-sm px-3 py-1 rounded-full">
                        <Star className="w-4 h-4 text-amber-400 fill-current" />
                        <span className="font-bold">{itinerary.rating}</span>
                      </div>
                    </div>
                  </div>
                </div>
                <div className="p-6">
                  <div className="flex items-center gap-2 mb-3">
                    <span className="px-2 py-1 bg-primary/10 text-primary text-xs rounded-full">{itinerary.duration}</span>
                    <span className="px-2 py-1 bg-muted text-muted-foreground text-xs rounded-full">{itinerary.pace}</span>
                    <span className="px-2 py-1 bg-muted text-muted-foreground text-xs rounded-full">{itinerary.groupSize}</span>
                  </div>
                  <h3 className="font-playfair text-xl font-bold text-foreground mb-2 line-clamp-1">{itinerary.title}</h3>
                  <div className="flex flex-wrap gap-2 mb-4">
                    {itinerary.themes.slice(0, 3).map((theme) => (
                      <span key={theme} className="px-2 py-1 bg-primary/10 text-primary text-xs rounded-full">{theme}</span>
                    ))}
                    {itinerary.themes.length > 3 && (
                      <span className="px-2 py-1 bg-muted text-muted-foreground text-xs rounded-full">+{itinerary.themes.length - 3} more</span>
                    )}
                  </div>
                  <div className="flex items-center justify-between pt-4 border-t border-border">
                    <span className="font-bold text-foreground">${itinerary.price.toLocaleString()}</span>
                    <div className="flex items-center gap-2">
                      <ArrowRight className="w-4 h-4 text-muted-foreground group-hover:text-primary transition-colors" />
                    </div>
                  </div>
                </div>
              </Link>
            ))}
          </div>

          <div className="mt-16 text-center">
            <Link
              href="/auth/signup"
              className="inline-flex items-center gap-2 px-8 py-4 bg-primary text-primary-foreground rounded-lg text-lg font-medium hover:bg-primary/90 transition-all shadow-lg"
            >
              Create Your Custom Journey
              <ArrowRight className="w-5 h-5" />
            </Link>
            <p className="mt-4 text-muted-foreground">
              Or build your own cultural journey with our AI itinerary planner
            </p>
          </div>
        </div>
      </main>

      <footer className="bg-muted/30 border-t border-border py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-muted-foreground text-sm">
          © 2024 CultureCompass. Built for Google for Developers PromptWars Hackathon.
        </div>
      </footer>
    </div>
  );
}