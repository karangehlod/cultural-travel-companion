'use client';

import { useState } from 'react';
import Link from 'next/link';
import { 
  Globe, 
  Compass, 
  Sparkles, 
  BookOpen, 
  MapPin, 
  Utensils, 
  Music, 
  Home,
  Search,
  ArrowRight,
  Sun,
  Moon,
  Heart,
  Star,
  Map,
  Camera,
  MessageSquare,
  Users,
  Leaf,
  Mountain,
  Building,
  Palette,
  Scroll,
  Landmark,
  Award
} from 'lucide-react';

// Mouse component for scroll indicator
function Mouse({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <rect x="5" y="2" width="14" height="20" rx="7" />
      <path d="M12 6v8" />
    </svg>
  );
}

const features = [
  {
    icon: Compass,
    title: 'Personalized Discovery',
    description: 'AI-powered recommendations matching your interests, budget, and travel style to destinations with authentic cultural depth.',
    color: 'from-blue-500 to-cyan-500',
  },
  {
    icon: BookOpen,
    title: 'Immersive Storytelling',
    description: 'Rich cultural narratives, historical context, and local legends that transform sightseeing into meaningful understanding.',
    color: 'from-amber-500 to-orange-500',
  },
  {
    icon: Sparkles,
    title: 'Hidden Gems',
    description: 'Uncover off-the-beaten-path locations, secret local spots, and community treasures that guidebooks never mention.',
    color: 'from-purple-500 to-pink-500',
  },
  {
    icon: Utensils,
    title: 'Culinary Heritage',
    description: 'Discover traditional dishes, family recipes, food markets, and dining customs with deep cultural significance.',
    color: 'from-red-500 to-rose-500',
  },
  {
    icon: Music,
    title: 'Cultural Events & Festivals',
    description: 'Find authentic festivals, ceremonies, workshops, and performances with insider guidance on respectful participation.',
    color: 'from-green-500 to-emerald-500',
  },
  {
    icon: Map,
    title: 'Smart Itineraries',
    description: 'Day-by-day cultural journeys with storytelling, practical logistics, cultural etiquette, and reflection prompts.',
    color: 'from-indigo-500 to-violet-500',
  },
];

const experienceTypes = [
  { icon: Home, label: 'Homestays', count: '1,200+' },
  { icon: Palette, label: 'Craft Workshops', count: '800+' },
  { icon: Utensils, label: 'Cooking Classes', count: '600+' },
  { icon: Music, label: 'Ceremonies', count: '400+' },
  { icon: Users, label: 'Cultural Exchange', count: '300+' },
  { icon: Leaf, label: 'Nature & Spirituality', count: '250+' },
  { icon: Mountain, label: 'Guided Treks', count: '450+' },
  { icon: Building, label: 'Heritage Tours', count: '700+' },
];

const destinations = [
  {
    name: 'Kyoto, Japan',
    country: 'Japan',
    image: 'https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=800',
    highlights: ['Tea Ceremony', 'Zen Gardens', 'Geisha Districts', 'Ancient Temples'],
    culturalDepth: 98,
  },
  {
    name: 'Oaxaca, Mexico',
    country: 'Mexico',
    image: 'https://images.unsplash.com/photo-1583417377828-1a1a1a1a1a1a?w=800',
    highlights: ['Mole Making', 'Day of the Dead', 'Textile Weaving', 'Mezcal Tasting'],
    culturalDepth: 95,
  },
  {
    name: 'Fez, Morocco',
    country: 'Morocco',
    image: 'https://images.unsplash.com/photo-1544717305-2782549b5136?w=800',
    highlights: ['Medina Crafts', 'Traditional Hammams', 'Sufi Music', 'Leather Tanning'],
    culturalDepth: 97,
  },
  {
    name: 'Luang Prabang, Laos',
    country: 'Laos',
    image: 'https://images.unsplash.com/photo-1528181304800-259b08848526?w=800',
    highlights: ['Alms Giving', 'Buddhist Temples', 'Textile Weaving', 'Mekong River Life'],
    culturalDepth: 96,
  },
  {
    name: 'Cusco, Peru',
    country: 'Peru',
    image: 'https://images.unsplash.com/photo-1587595431973-160d0d94add1?w=800',
    highlights: ['Inca Heritage', 'Quechua Culture', 'Traditional Weaving', 'Sacred Valley'],
    culturalDepth: 94,
  },
  {
    name: 'Varanasi, India',
    country: 'India',
    image: 'https://images.unsplash.com/photo-1561361512-4c17431f7e1a?w=800',
    highlights: ['Ganges Rituals', 'Classical Music', 'Silk Weaving', 'Spiritual Practices'],
    culturalDepth: 99,
  },
];

export default function HomePage() {
  const [isDark, setIsDark] = useState(false);

  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-background/95 backdrop-blur-sm border-b border-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-2">
              <Globe className="w-8 h-8 text-primary" />
              <span className="font-playfair text-2xl font-bold text-foreground">
                CultureCompass
              </span>
            </div>
            <div className="hidden md:flex items-center gap-8">
              <Link href="#features" className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">
                Features
              </Link>
              <Link href="#destinations" className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">
                Destinations
              </Link>
              <Link href="#experiences" className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">
                Experiences
              </Link>
              <Link href="#how-it-works" className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">
                How It Works
              </Link>
            </div>
            <div className="flex items-center gap-4">
              <button
                onClick={() => setIsDark(!isDark)}
                className="p-2 rounded-lg text-muted-foreground hover:bg-muted transition-colors"
                aria-label="Toggle theme"
              >
                {isDark ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
              </button>
              <Link href="/auth/login" className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">
                Sign In
              </Link>
              <Link
                href="/auth/signup"
                className="px-4 py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:bg-primary/90 transition-colors"
              >
                Start Your Journey
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden pt-16">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-background to-accent/5" />
        <div className="absolute inset-0 bg-[url('data:image/svg+xml,%3Csvg width=%2260%22 height=%2260%22 viewBox=%220 0 60 60%22 xmlns=%22http://www.w3.org/2000/svg%22%3E%3Cg fill=%22none%22 fill-rule=%22evenodd%22%3E%3Cg fill=%22%239C92AC%22 fill-opacity=%220.03%22%3E%3Cpath d=%22M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 36v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 6V0H4v4H0v2h4v4h2V6h4V4H6z%22/%3E%3C/g%3E%3C/g%3E%3C/svg%3E')]" />
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 lg:py-32">
          <div className="text-center max-w-4xl mx-auto animate-slide-up">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 text-primary text-sm font-medium mb-8">
              <Sparkles className="w-4 h-4" />
              <span>Google for Developers • PromptWars Hackathon</span>
            </div>
            <h1 className="font-playfair text-5xl sm:text-6xl lg:text-7xl font-bold text-foreground mb-6 leading-tight">
              Discover the{' '}
              <span className="relative">
                <span className="relative z-10">Soul of</span>
                <span className="absolute bottom-0 left-0 right-0 h-2 bg-primary/20" />
              </span>{' '}
              Every Destination
            </h1>
            <p className="text-lg sm:text-xl text-muted-foreground mb-10 max-w-2xl mx-auto leading-relaxed">
              An AI-powered cultural travel companion that goes beyond tourist attractions. 
              Experience authentic traditions, hidden gems, local stories, and meaningful connections 
              with communities around the world.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
              <Link
                href="/auth/signup"
                className="w-full sm:w-auto px-8 py-4 bg-primary text-primary-foreground rounded-lg text-lg font-medium hover:bg-primary/90 transition-all shadow-lg hover:shadow-xl"
              >
                <span className="flex items-center justify-center gap-2">
                  Start Your Cultural Journey
                  <ArrowRight className="w-5 h-5" />
                </span>
              </Link>
              <Link
                href="#destinations"
                className="w-full sm:w-auto px-8 py-4 border-2 border-border text-foreground rounded-lg text-lg font-medium hover:bg-muted transition-all"
              >
                Explore Destinations
              </Link>
            </div>
            
            {/* Trust indicators */}
            <div className="flex flex-wrap items-center justify-center gap-8 text-sm text-muted-foreground">
              <div className="flex items-center gap-2">
                <Globe className="w-4 h-4" />
                <span>50+ Countries</span>
              </div>
              <div className="flex items-center gap-2">
                <Heart className="w-4 h-4 text-red-500" />
                <span>12,000+ Experiences</span>
              </div>
              <div className="flex items-center gap-2">
                <Star className="w-4 h-4 text-amber-500" />
                <span>4.9/5 Traveler Rating</span>
              </div>
              <div className="flex items-center gap-2">
                <Award className="w-4 h-4" />
                <span>Google AI Hackathon</span>
              </div>
            </div>
          </div>
        </div>
        
        {/* Scroll indicator */}
        <div className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce">
          <Mouse className="w-6 h-10 text-muted-foreground" />
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 lg:py-32 bg-muted/30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="font-playfair text-4xl sm:text-5xl font-bold text-foreground mb-6">
              Transform How You Experience Culture
            </h2>
            <p className="text-lg text-muted-foreground">
              Every feature is designed to deepen your cultural understanding and create meaningful connections
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, index) => (
              <div
                key={feature.title}
                className="group cultural-card p-8 rounded-2xl bg-card border border-border"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <div className={`w-14 h-14 rounded-xl bg-gradient-to-br ${feature.color} flex items-center justify-center mb-6 group-hover:scale-110 transition-transform`}>
                  <feature.icon className="w-7 h-7 text-white" />
                </div>
                <h3 className="font-playfair text-2xl font-bold text-foreground mb-3">
                  {feature.title}
                </h3>
                <p className="text-muted-foreground leading-relaxed">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Destinations Section */}
      <section id="destinations" className="py-20 lg:py-32">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-4 mb-12">
            <div>
              <h2 className="font-playfair text-4xl sm:text-5xl font-bold text-foreground mb-4">
                Featured Cultural Destinations
              </h2>
              <p className="text-muted-foreground text-lg">
                Hand-curated destinations with deep cultural heritage and authentic experiences
              </p>
            </div>
            <Link
              href="/destinations"
              className="inline-flex items-center gap-2 px-4 py-2 border border-border rounded-lg text-sm font-medium hover:bg-muted transition-colors"
            >
              View All Destinations
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
          
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {destinations.map((destination, index) => (
              <Link
                key={destination.name}
                href={`/destinations/${destination.name.toLowerCase().replace(/[^a-z0-9]+/g, '-')}`}
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
        </div>
      </section>

      {/* Experiences Section */}
      <section id="experiences" className="py-20 lg:py-32 bg-muted/30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="font-playfair text-4xl sm:text-5xl font-bold text-foreground mb-6">
              Authentic Cultural Experiences
            </h2>
            <p className="text-lg text-muted-foreground">
              Connect with local communities through hands-on workshops, ceremonies, and daily life experiences
            </p>
          </div>
          
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6">
            {experienceTypes.map((exp, index) => (
              <div
                key={exp.label}
                className="cultural-card p-6 rounded-xl bg-card border border-border text-center"
                style={{ animationDelay: `${index * 80}ms` }}
              >
                <div className="w-14 h-14 mx-auto mb-4 rounded-xl bg-primary/10 flex items-center justify-center group-hover:bg-primary group-hover:text-primary-foreground transition-colors">
                  <exp.icon className="w-7 h-7 text-primary group-hover:text-primary-foreground transition-colors" />
                </div>
                <h3 className="font-semibold text-foreground mb-1">{exp.label}</h3>
                <p className="text-2xl font-bold text-primary">{exp.count}</p>
                <p className="text-sm text-muted-foreground mt-2">Available experiences</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="py-20 lg:py-32">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="font-playfair text-4xl sm:text-5xl font-bold text-foreground mb-6">
              Your Cultural Journey in 4 Steps
            </h2>
            <p className="text-lg text-muted-foreground">
              From discovery to deep connection, our AI guides you every step of the way
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              {
                step: '01',
                icon: Search,
                title: 'Tell Us Your Interests',
                description: 'Share your travel style, cultural passions, budget, and dream experiences. Our AI learns what moves you.',
              },
              {
                step: '02',
                icon: Sparkles,
                title: 'Get Personalized Matches',
                description: 'Receive curated destination recommendations with cultural depth scores, hidden gems, and authentic experiences.',
              },
              {
                step: '03',
                icon: BookOpen,
                title: 'Explore Deep Cultural Context',
                description: 'Dive into immersive storytelling, historical narratives, local legends, and cultural etiquette before you go.',
              },
              {
                step: '04',
                icon: Map,
                title: 'Journey with Meaning',
                description: 'Follow AI-crafted itineraries with day-by-day cultural insights, reflection prompts, and real-time guidance.',
              },
            ].map((step, index) => (
              <div
                key={step.step}
                className="cultural-card p-8 rounded-2xl bg-card border border-border relative"
                style={{ animationDelay: `${index * 120}ms` }}
              >
                <div className="absolute -top-3 -right-3 w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center font-bold text-primary text-2xl">
                  {step.step}
                </div>
                <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center mb-6">
                  <step.icon className="w-6 h-6 text-primary" />
                </div>
                <h3 className="font-playfair text-xl font-bold text-foreground mb-3">
                  {step.title}
                </h3>
                <p className="text-muted-foreground leading-relaxed">
                  {step.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* AI Technology Section */}
      <section className="py-20 lg:py-32 bg-gradient-to-br from-primary/5 via-background to-accent/5">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center">
            <div>
              <h2 className="font-playfair text-4xl sm:text-5xl font-bold text-foreground mb-6">
                Powered by Google&apos;s Most Advanced AI
              </h2>
              <p className="text-lg text-muted-foreground mb-8">
                Built with Gemini 1.5 Pro, Google Places API (New), and Google Maps Platform 
                for real-time, authentic cultural intelligence.
              </p>
              <div className="space-y-4">
                {[
                  { icon: Globe, title: 'Gemini 1.5 Pro', desc: 'Cultural storytelling, itinerary generation, and conversational AI companion' },
                  { icon: MapPin, title: 'Places API (New)', desc: 'Real-time place data, photos, reviews, and opening hours for cultural sites' },
                  { icon: Map, title: 'Maps Platform', desc: 'Geocoding, directions, distance matrix, and elevation for seamless navigation' },
                  { icon: Sparkles, title: 'Firebase & Cloud', desc: 'Authentication, real-time sync, and serverless deployment at scale' },
                ].map((tech, index) => (
                  <div key={index} className="flex items-start gap-4 p-4 rounded-xl bg-card border border-border">
                    <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
                      <tech.icon className="w-5 h-5 text-primary" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-foreground">{tech.title}</h4>
                      <p className="text-sm text-muted-foreground">{tech.desc}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            <div className="relative">
              <div className="aspect-video rounded-2xl bg-gradient-to-br from-primary/20 to-accent/20 flex items-center justify-center border border-border">
                <div className="text-center p-8">
                  <MessageSquare className="w-24 h-24 text-primary/30 mx-auto mb-6" />
                  <h3 className="font-playfair text-2xl font-bold text-foreground mb-4">
                    Your AI Cultural Companion
                  </h3>
                  <p className="text-muted-foreground mb-6 max-w-md mx-auto">
                    Chat naturally with an AI that understands cultural nuance, remembers your preferences, and helps you plan meaningful journeys.
                  </p>
                  <div className="space-y-3 max-w-md mx-auto text-left">
                    {[
                      '"What\'s the significance of the tea ceremony in Kyoto?"',
                      '"Find me a homestay with a family in Oaxaca"',
                      '"Explain the history behind Fez\'s leather tanneries"',
                      '"Create a 7-day spiritual journey in Luang Prabang"',
                    ].map((q, i) => (
                      <div key={i} className="bg-card/80 backdrop-blur-sm p-3 rounded-lg border border-border/50">
                        <p className="text-sm text-foreground italic">&quot;{q}&quot;</p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 lg:py-32">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="rounded-3xl bg-gradient-to-r from-primary via-primary/80 to-accent p-12 md:p-16 text-center">
            <div className="max-w-3xl mx-auto">
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/20 text-white text-sm font-medium mb-6">
                <Sparkles className="w-4 h-4" />
                <span>Limited Early Access for Hackathon Reviewers</span>
              </div>
              <h2 className="font-playfair text-4xl sm:text-5xl font-bold text-white mb-6">
                Ready to Travel Differently?
              </h2>
              <p className="text-lg text-white/90 mb-8 max-w-2xl mx-auto">
                Join thousands of travelers discovering the world through authentic cultural connections. 
                Your meaningful journey starts with a single conversation.
              </p>
              <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                <Link
                  href="/auth/signup"
                  className="w-full sm:w-auto px-8 py-4 bg-white text-primary rounded-lg text-lg font-medium hover:bg-white/90 transition-all shadow-lg"
                >
                  Start Free Journey
                  <ArrowRight className="w-5 h-5 ml-2 inline" />
                </Link>
                <Link
                  href="#demo"
                  className="w-full sm:w-auto px-8 py-4 border-2 border-white/30 text-white rounded-lg text-lg font-medium hover:bg-white/10 transition-all"
                >
                  Watch Demo
                </Link>
              </div>
              <p className="mt-6 text-white/70 text-sm">
                No credit card required • 14-day free trial • Cancel anytime
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-muted/30 border-t border-border py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8 mb-12">
            <div className="md:col-span-2">
              <div className="flex items-center gap-2 mb-4">
                <Globe className="w-8 h-8 text-primary" />
                <span className="font-playfair text-2xl font-bold text-foreground">CultureCompass</span>
              </div>
              <p className="text-muted-foreground max-w-md">
                AI-powered cultural travel companion helping you discover the soul of every destination 
                through authentic experiences, immersive storytelling, and meaningful connections.
              </p>
            </div>
            <div>
              <h4 className="font-semibold text-foreground mb-4">Product</h4>
              <ul className="space-y-2 text-muted-foreground">
                <li><Link href="/destinations" className="hover:text-foreground transition-colors">Destinations</Link></li>
                <li><Link href="/experiences" className="hover:text-foreground transition-colors">Experiences</Link></li>
                <li><Link href="/itineraries" className="hover:text-foreground transition-colors">Itineraries</Link></li>
                <li><Link href="/stories" className="hover:text-foreground transition-colors">Cultural Stories</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-foreground mb-4">Company</h4>
              <ul className="space-y-2 text-muted-foreground">
                <li><Link href="/about" className="hover:text-foreground transition-colors">About Us</Link></li>
                <li><Link href="/blog" className="hover:text-foreground transition-colors">Blog</Link></li>
                <li><Link href="/careers" className="hover:text-foreground transition-colors">Careers</Link></li>
                <li><Link href="/contact" className="hover:text-foreground transition-colors">Contact</Link></li>
              </ul>
            </div>
          </div>
          <div className="pt-8 border-t border-border flex flex-col md:flex-row items-center justify-between gap-4">
            <p className="text-muted-foreground text-sm">
              © 2024 CultureCompass. Built for Google for Developers PromptWars Hackathon.
            </p>
            <div className="flex items-center gap-6">
              <a href="https://github.com" className="text-muted-foreground hover:text-foreground transition-colors" aria-label="GitHub">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/></svg>
              </a>
              <a href="https://twitter.com" className="text-muted-foreground hover:text-foreground transition-colors" aria-label="Twitter">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M23 3a10.9 10.9 0 01-3.14 1.53 4.48 4.48 0 00-7.86 3v1A10.66 10.66 0 013 4s-4 9 5 13a11.64 11.64 0 01-7 2c9 5 20 0 20-11.5a4.5 4.5 0 00-.08-.83A7.72 7.72 0 0023 3z"/></svg>
              </a>
              <a href="https://linkedin.com" className="text-muted-foreground hover:text-foreground transition-colors" aria-label="LinkedIn">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}