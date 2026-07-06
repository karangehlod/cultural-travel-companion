'use client';

import Link from 'next/link';
import { 
  Globe, 
  Home, 
  Palette, 
  Utensils, 
  Music, 
  Users, 
  Leaf, 
  Mountain, 
  Building,
  BookOpen,
  Sparkles,
  MapPin,
  Heart,
  ArrowRight,
  Star
} from 'lucide-react';

const experienceCategories = [
  { 
    icon: Home, 
    label: 'Homestays', 
    count: '1,200+',
    description: 'Live with local families, share meals, learn traditions',
    color: 'from-amber-500 to-orange-500'
  },
  { 
    icon: Palette, 
    label: 'Craft Workshops', 
    count: '800+',
    description: 'Learn pottery, weaving, painting from master artisans',
    color: 'from-purple-500 to-pink-500'
  },
  { 
    icon: Utensils, 
    label: 'Cooking Classes', 
    count: '600+',
    description: 'Master traditional recipes with local chefs and families',
    color: 'from-red-500 to-rose-500'
  },
  { 
    icon: Music, 
    label: 'Ceremonies & Festivals', 
    count: '400+',
    description: 'Participate in sacred rituals and cultural celebrations',
    color: 'from-green-500 to-emerald-500'
  },
  { 
    icon: Users, 
    label: 'Cultural Exchange', 
    count: '300+',
    description: 'Language exchange, community projects, skill sharing',
    color: 'from-blue-500 to-cyan-500'
  },
  { 
    icon: Leaf, 
    label: 'Nature & Spirituality', 
    count: '250+',
    description: 'Sacred walks, meditation retreats, nature ceremonies',
    color: 'from-teal-500 to-green-500'
  },
  { 
    icon: Mountain, 
    label: 'Guided Treks', 
    count: '450+',
    description: 'Cultural hiking with local guides, ancient paths',
    color: 'from-orange-500 to-red-500'
  },
  { 
    icon: Building, 
    label: 'Heritage Tours', 
    count: '700+',
    description: 'Expert-led tours of UNESCO sites and hidden history',
    color: 'from-indigo-500 to-violet-500'
  },
];

const mockExperiences = [
  {
    id: '1',
    title: 'Traditional Tea Ceremony in Kyoto',
    location: 'Kyoto, Japan',
    type: 'Cultural Exchange',
    duration: '2 hours',
    price: 85,
    rating: 4.9,
    image: 'https://images.unsplash.com/photo-1515823064-d6e0c04616a7?w=600',
    description: 'Learn the ancient art of Japanese tea ceremony from a tea master in a historic machiya townhouse.',
  },
  {
    id: '2',
    title: 'Mole Making Workshop in Oaxaca',
    location: 'Oaxaca, Mexico',
    type: 'Cooking Class',
    duration: '4 hours',
    price: 120,
    rating: 4.8,
    image: 'https://images.unsplash.com/photo-1628840042765-356cda07504e?w=600',
    description: 'Learn to make authentic mole negro from scratch using 20+ ingredients with a local abuela.',
  },
  {
    id: '3',
    title: 'Berber Carpet Weaving in Fez',
    location: 'Fez, Morocco',
    type: 'Craft Workshop',
    duration: 'Full day',
    price: 150,
    rating: 4.9,
    image: 'https://images.unsplash.com/photo-1601255655608-0d8c0f5c9c9a?w=600',
    description: 'Master traditional Berber weaving techniques on a vertical loom with a master artisan.',
  },
  {
    id: '4',
    title: 'Luang Prabang Alms Giving & Monk Chat',
    location: 'Luang Prabang, Laos',
    type: 'Spiritual',
    duration: '3 hours',
    price: 65,
    rating: 4.8,
    image: 'https://images.unsplash.com/photo-1561894043-9c9acfc6a7d8?w=600',
    description: 'Participate in the dawn alms giving ceremony and share a conversation with novice monks.',
  },
  {
    id: '5',
    title: 'Andean Weaving in Sacred Valley',
    location: 'Cusco, Peru',
    type: 'Craft Workshop',
    duration: '6 hours',
    price: 95,
    rating: 4.7,
    image: 'https://images.unsplash.com/photo-1583417377828-1a1a1a1a1a1a?w=600',
    description: 'Learn backstrap weaving from Quechua women in their mountain community above the Sacred Valley.',
  },
  {
    id: '6',
    title: 'Varanasi Dawn Boat & Ganges Rituals',
    location: 'Varanasi, India',
    type: 'Spiritual',
    duration: '3 hours',
    price: 55,
    rating: 4.9,
    image: 'https://images.unsplash.com/photo-1561361512-4c17431f7e1a?w=600',
    description: 'Witness ancient fire rituals on the ghats and learn their significance from a local priest.',
  },
];

export default function ExperiencesPage() {
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
              <Link href="/auth/login" className="px-4 py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:bg-primary/90">Sign In</Link>
            </div>
          </div>
        </div>
      </nav>

      <main className="pt-24 pb-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h1 className="font-playfair text-4xl sm:text-5xl font-bold text-foreground mb-6">
              Authentic Cultural Experiences
            </h1>
            <p className="text-lg text-muted-foreground max-w-max-w-3xl mx-auto">
              Connect with local communities through hands-on workshops, sacred ceremonies, and daily life experiences. 
              Every experience is curated for authenticity and cultural depth.
            </p>
          </div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 mb-16">
            {experienceCategories.map((cat, index) => (
              <Link
                key={cat.label}
                href={`/experiences?type=${cat.label.toLowerCase().replace(/\s+/g, '-')}`}
                className="cultural-card p-6 rounded-xl bg-card border border-border text-center hover:border-primary/50 transition-colors"
                style={{ animationDelay: `${index * 80}ms` }}
              >
                <div className={`w-14 h-14 mx-auto mb-4 rounded-xl bg-gradient-to-br ${cat.color} flex items-center justify-center`}>
                  <cat.icon className="w-7 h-7 text-white" />
                </div>
                <h3 className="font-semibold text-foreground mb-1">{cat.label}</h3>
                <p className="text-2xl font-bold text-primary">{cat.count}</p>
                <p className="text-sm text-muted-foreground mt-2">{cat.description}</p>
              </Link>
            ))}
          </div>

          <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-4 mb-8">
            <div>
              <h2 className="font-playfair text-3xl font-bold text-foreground mb-2">
                Featured Experiences
              </h2>
              <p className="text-muted-foreground">Curated for authenticity and cultural depth</p>
            </div>
          </div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {mockExperiences.map((exp, index) => (
              <Link
                key={exp.id}
                href={`/experiences/${exp.id}`}
                className="group cultural-card overflow-hidden rounded-2xl bg-card border border-border"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <div className="relative h-48 overflow-hidden">
                  <img
                    src={exp.image}
                    alt={exp.title}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-black/20 to-transparent" />
                  <div className="absolute bottom-3 left-3 right-3 text-white">
                    <span className="inline-flex items-center gap-1 px-2 py-1 bg-white/20 backdrop-blur-sm rounded-full text-xs font-medium">
                      <MapPin className="w-3 h-3" />
                      {exp.location}
                    </span>
                    <div className="absolute bottom-3 right-3">
                      <div className="flex items-center gap-1 bg-white/20 backdrop-blur-sm px-2 py-1 rounded-full">
                        <Star className="w-4 h-4 text-amber-400 fill-current" />
                        <span className="font-bold">{exp.rating}</span>
                      </div>
                    </div>
                  </div>
                </div>
                <div className="p-5">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="px-2 py-1 bg-primary/10 text-primary text-xs rounded-full">{exp.type}</span>
                    <span className="px-2 py-1 bg-muted text-muted-foreground text-xs rounded-full">{exp.duration}</span>
                  </div>
                  <h3 className="font-playfair text-lg font-bold text-foreground mb-2 line-clamp-1">{exp.title}</h3>
                  <p className="text-sm text-muted-foreground mb-3 line-clamp-2">{exp.description}</p>
                  <div className="flex items-center justify-between pt-3 border-t border-border">
                    <span className="font-bold text-foreground">${exp.price}</span>
                    <ArrowRight className="w-4 h-4 text-muted-foreground group-hover:text-primary transition-colors" />
                  </div>
                </div>
              </Link>
            ))}
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