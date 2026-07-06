'use client';

import { useState } from 'react';
import Link from 'next/link';
import { 
  Globe, 
  Search, 
  MapPin, 
  Star, 
  Filter, 
  ChevronLeft, 
  ChevronRight,
  ArrowRight,
  Heart,
  BookOpen,
  Utensils,
  Music,
  Home,
  Camera
} from 'lucide-react';

interface Destination {
  id: string;
  name: string;
  country: string;
  city?: string;
  image: string;
  highlights: string[];
  culturalDepth: number;
  rating?: number;
}

const mockDestinations: Destination[] = [
  {
    id: '1',
    name: 'Kyoto, Japan',
    country: 'Japan',
    city: 'Kyoto',
    image: 'https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=800',
    highlights: ['Tea Ceremony', 'Zen Gardens', 'Geisha Districts', 'Ancient Temples'],
    culturalDepth: 98,
    rating: 4.9
  },
  {
    id: '2',
    name: 'Oaxaca, Mexico',
    country: 'Mexico',
    city: 'Oaxaca',
    image: 'https://images.unsplash.com/photo-1583417377828-1a1a1a1a1a1a?w=800',
    highlights: ['Mole Making', 'Day of the Dead', 'Textile Weaving', 'Mezcal Tasting'],
    culturalDepth: 95,
    rating: 4.8
  },
  {
    id: '3',
    name: 'Fez, Morocco',
    country: 'Morocco',
    city: 'Fez',
    image: 'https://images.unsplash.com/photo-1544717305-2782549b5136?w=800',
    highlights: ['Medina Crafts', 'Traditional Hammams', 'Sufi Music', 'Leather Tanning'],
    culturalDepth: 97,
    rating: 4.9
  },
  {
    id: '4',
    name: 'Luang Prabang, Laos',
    country: 'Laos',
    city: 'Luang Prabang',
    image: 'https://images.unsplash.com/photo-1528181304800-259b08848526?w=800',
    highlights: ['Alms Giving', 'Buddhist Temples', 'Textile Weaving', 'Mekong River Life'],
    culturalDepth: 96,
    rating: 4.8
  },
  {
    id: '5',
    name: 'Cusco, Peru',
    country: 'Peru',
    city: 'Cusco',
    image: 'https://images.unsplash.com/photo-1587595431973-160d0d94add1?w=800',
    highlights: ['Inca Heritage', 'Quechua Culture', 'Traditional Weaving', 'Sacred Valley'],
    culturalDepth: 94,
    rating: 4.7
  },
  {
    id: '6',
    name: 'Varanasi, India',
    country: 'India',
    city: 'Varanasi',
    image: 'https://images.unsplash.com/photo-1561361512-4c17431f7e1a?w=800',
    highlights: ['Ganges Rituals', 'Classical Music', 'Silk Weaving', 'Spiritual Practices'],
    culturalDepth: 99,
    rating: 4.9
  },
];

export default function DestinationsPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [filterCountry, setFilterCountry] = useState('all');
  const [currentPage, setCurrentPage] = useState(1);
  const destinationsPerPage = 6;

  const countries = ['all', ...Array.from(new Set(mockDestinations.map(d => d.country)))];
  const filtered = mockDestinations.filter(d => {
    const matchesSearch = d.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         d.country.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCountry = filterCountry === 'all' || d.country === filterCountry;
    return matchesSearch && matchesCountry;
  });

  const paginated = filtered.slice((currentPage - 1) * destinationsPerPage, currentPage * destinationsPerPage);
  const totalPages = Math.ceil(filtered.length / destinationsPerPage);

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
              <Link href="/auth/login" className="px-4 py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:bg-primary/90">Sign In</Link>
            </div>
          </div>
        </div>
      </nav>

      <main className="pt-24 pb-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mb-12">
            <h1 className="font-playfair text-4xl sm:text-5xl font-bold text-foreground mb-4">
              Discover Cultural Destinations
            </h1>
            <p className="text-lg text-muted-foreground max-w-2xl">
              Hand-curated destinations with deep cultural heritage, authentic experiences, and meaningful connections with local communities.
            </p>
          </div>

          <div className="flex flex-col md:flex-row gap-6 mb-8">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
              <input
                type="text"
                placeholder="Search destinations..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-3 border border-input bg-background rounded-lg text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
              />
            </div>
            <select
              value={filterCountry}
              onChange={(e) => setFilterCountry(e.target.value)}
              className="w-full md:w-48 px-4 py-3 border border-input bg-background rounded-lg text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
            >
              {countries.map(country => (
                <option key={country} value={country}>
                  {country === 'all' ? 'All Countries' : country}
                </option>
              ))}
            </select>
          </div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {paginated.map((destination, index) => (
              <Link
                key={destination.id}
                href={`/destinations/${destination.id}`}
                className="group cultural-card overflow-hidden rounded-2xl bg-card border border-border"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <div className="relative h-56 overflow-hidden">
                  <img
                    src={destination.image}
                    alt={destination.name}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-black/20 to-transparent" />
                  <div className="absolute bottom-4 left-4 right-4 text-white">
                    <span className="inline-flex items-center gap-1 px-3 py-1 bg-white/20 backdrop-blur-sm rounded-full text-sm font-medium">
                      <MapPin className="w-3 h-3" />
                      {destination.country}
                    </span>
                    <div className="absolute bottom-4 right-4">
                      <div className="flex items-center gap-1 bg-white/20 backdrop-blur-sm px-3 py-1 rounded-full">
                        <Star className="w-4 h-4 text-amber-400 fill-current" />
                        <span className="font-bold">{destination.culturalDepth}%</span>
                        <span className="text-xs opacity-75">Cultural Depth</span>
                      </div>
                    </div>
                  </div>
                </div>
                <div className="p-6">
                  <h3 className="font-playfair text-xl font-bold text-foreground mb-2">
                    {destination.name}
                  </h3>
                  <div className="flex flex-wrap gap-2 mb-4">
                    {destination.highlights.slice(0, 3).map((highlight) => (
                      <span
                        key={highlight}
                        className="px-2 py-1 bg-primary/10 text-primary text-xs rounded-full"
                      >
                        {highlight}
                      </span>
                    ))}
                    {destination.highlights.length > 3 && (
                      <span className="px-2 py-1 bg-muted text-muted-foreground text-xs rounded-full">
                        +{destination.highlights.length - 3} more
                      </span>
                    )}
                  </div>
                  <div className="flex items-center justify-between pt-4 border-t border-border">
                    <span className="text-sm text-muted-foreground">
                      {destination.highlights.length} cultural highlights
                    </span>
                    <ArrowRight className="w-5 h-5 text-muted-foreground group-hover:text-primary transition-colors" />
                  </div>
                </div>
              </Link>
            ))}
          </div>

          {totalPages > 1 && (
            <div className="flex items-center justify-center gap-2 mt-12">
              <button
                onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                disabled={currentPage === 1}
                className="px-4 py-2 border border-border rounded-lg text-sm font-medium hover:bg-muted disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
              <span className="px-4 text-sm font-medium text-foreground">
                Page {currentPage} of {totalPages}
              </span>
              <button
                onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                disabled={currentPage === totalPages}
                className="px-4 py-2 border border-border rounded-lg text-sm font-medium hover:bg-muted disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          )}
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