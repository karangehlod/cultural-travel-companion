'use client';

import Link from 'next/link';
import { 
  Globe, 
  BookOpen, 
  Scroll, 
  Clock, 
  MapPin,
  ArrowRight,
  Heart,
  Star,
  Calendar,
  Volume2,
  Video
} from 'lucide-react';

const mockStories = [
  {
    id: '1',
    title: 'The Legend of the Golden Pavilion',
    type: 'Legend',
    culture: 'Japanese',
    period: '14th Century',
    summary: 'How a retired shogun\'s villa became Kyoto\'s most iconic Zen temple, and the monk who burned it down in 1950.',
    content: 'Full story content here...',
    readTime: '8 min',
    hasAudio: true,
    hasVideo: false,
    image: 'https://images.unsplash.com/photo-1528360983277-13d401cdc186?w=800',
  },
  {
    id: '2',
    title: 'The Seven Moles of Oaxaca',
    type: 'Culinary History',
    culture: 'Mexican (Zapotec/Mixtec)',
    period: 'Pre-Hispanic to Present',
    summary: 'How seven distinct mole sauces emerged from indigenous ingredients and Spanish influence, each telling a story of cultural fusion.',
    content: 'Full story content here...',
    readTime: '12 min',
    hasAudio: true,
    hasVideo: true,
    image: 'https://images.unsplash.com/photo-1628840042765-356cda07504e?w=800',
  },
  {
    id: '3',
    title: 'The Blue Men of the Sahara',
    type: 'Oral History',
    culture: 'Tuareg (Berber)',
    period: 'Ancient to Present',
    summary: 'The story of the Tuareg people, their indigo-dyed veils, and their ancient salt caravans across the Sahara.',
    content: 'Full story content here...',
    readTime: '10 min',
    hasAudio: true,
    hasVideo: false,
    image: 'https://images.unsplash.com/photo-1529919126747519-9c6c3f2c5b06?w=800',
  },
  {
    id: '4',
    title: 'The Alms Giving Ceremony of Luang Prabang',
    type: 'Living Tradition',
    culture: 'Lao Buddhist',
    period: '14th Century to Present',
    summary: 'Every dawn, barefoot monks walk silently through misty streets collecting alms—a tradition that binds community and monastic life.',
    content: 'Full story content here...',
    readTime: '7 min',
    hasAudio: false,
    hasVideo: true,
    image: 'https://images.unsplash.com/photo-1528181304800-259b08848526?w=800',
  },
  {
    id: '5',
    title: 'The Inca Bridge Keepers of Q\'eswachaka',
    type: 'Living Heritage',
    culture: 'Quechua (Inca)',
    period: 'Inca Empire to Present',
    summary: 'Four communities rebuild a grass suspension bridge every year using only Inca techniques—no modern tools allowed.',
    content: 'Full story content here...',
    readTime: '9 min',
    hasAudio: false,
    hasVideo: true,
    image: 'https://images.unsplash.com/photo-1587595431973-160d0d94add1?w=800',
  },
  {
    id: '6',
    title: 'The Eternal Fire of Varanasi',
    type: 'Sacred Geography',
    culture: 'Hindu',
    period: 'Ancient to Present',
    summary: 'Why the cremation ghats of Varanasi have burned continuously for millennia, and what it means for the cycle of life and death.',
    content: 'Full story content here...',
    readTime: '11 min',
    hasAudio: true,
    hasVideo: false,
    image: 'https://images.unsplash.com/photo-1561361512-4c17431f7e1a?w=800',
  },
];

export default function StoriesPage() {
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
              <Link href="/itineraries" className="text-sm font-medium text-muted-foreground hover:text-foreground">Itineraries</Link>
              <Link href="/auth/login" className="px-4 py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:bg-primary/90">Sign In</Link>
            </div>
          </div>
        </div>
      </nav>

      <main className="pt-24 pb-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 text-primary text-sm font-medium mb-6">
              <BookOpen className="w-4 h-4" />
              <span>Cultural Stories & Oral Histories</span>
            </div>
            <h1 className="font-playfair text-4xl sm:text-5xl font-bold text-foreground mb-6">
              Stories That Shape Cultures
            </h1>
            <p className="text-lg text-muted-foreground max-w-3xl mx-auto">
              Immerse yourself in the legends, oral histories, and living traditions that define communities around the world. 
              Each story is curated for cultural accuracy and deep meaning.
            </p>
          </div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {mockStories.map((story, index) => (
              <Link
                key={story.id}
                href={`/stories/${story.id}`}
                className="group cultural-card overflow-hidden rounded-2xl bg-card border border-border"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <div className="relative h-56 overflow-hidden">
                  <img
                    src={story.image}
                    alt={story.title}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-black/20 to-transparent" />
                  <div className="absolute bottom-4 left-4 right-4 text-white">
                    <span className="inline-flex items-center gap-1 px-3 py-1 bg-white/20 backdrop-blur-sm rounded-full text-sm font-medium">
                      <MapPin className="w-3 h-3" />
                      {story.culture}
                    </span>
                    <div className="absolute bottom-4 right-4 flex items-center gap-2">
                      {story.hasAudio && (
                        <button className="px-2 py-1 bg-white/20 backdrop-blur-sm rounded-full text-white text-xs" aria-label="Listen to story">
                          <Volume2 className="w-4 h-4" />
                        </button>
                      )}
                      {story.hasVideo && (
                        <button className="px-2 py-1 bg-white/20 backdrop-blur-sm rounded-full text-white text-xs" aria-label="Watch story">
                          <Video className="w-4 h-4" />
                        </button>
                      )}
                    </div>
                  </div>
                </div>
                <div className="p-6">
                  <div className="flex items-center gap-2 mb-3">
                    <span className="px-2 py-1 bg-primary/10 text-primary text-xs rounded-full">{story.type}</span>
                    <span className="px-2 py-1 bg-muted text-muted-foreground text-xs rounded-full">{story.period}</span>
                  </div>
                  <h3 className="font-playfair text-xl font-bold text-foreground mb-2 line-clamp-1">{story.title}</h3>
                  <p className="text-sm text-muted-foreground mb-4 line-clamp-2">{story.summary}</p>
                  <div className="flex items-center justify-between pt-4 border-t border-border">
                    <div className="flex items-center gap-3 text-sm text-muted-foreground">
                      <span className="flex items-center gap-1"><Clock className="w-3 h-3" /> {story.readTime}</span>
                      <span className="flex items-center gap-1"><Heart className="w-3 h-3 text-red-500" /> Cultural Treasure</span>
                    </div>
                    <ArrowRight className="w-4 h-4 text-muted-foreground group-hover:text-primary transition-colors" />
                  </div>
                </div>
              </Link>
            ))}
          </div>

          <div className="mt-16 text-center">
            <p className="text-muted-foreground mb-4">Want to contribute a story from your culture?</p>
            <Link
              href="/auth/signup"
              className="inline-flex items-center gap-2 px-8 py-4 bg-primary text-primary-foreground rounded-lg text-lg font-medium hover:bg-primary/90 transition-all shadow-lg"
            >
              Share Your Culture
              <ArrowRight className="w-5 h-5" />
            </Link>
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