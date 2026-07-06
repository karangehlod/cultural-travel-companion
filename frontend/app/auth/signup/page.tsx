'use client';

import { useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { 
  Globe, 
  Mail, 
  Lock, 
  User, 
  Eye, 
  EyeOff,
  Loader2,
  Sparkles,
  ArrowRight,
  CheckCircle,
  Utensils,
  Landmark,
  Mountain,
  Leaf,
  Palette,
  Home,
  Camera,
} from 'lucide-react';
import toast from 'react-hot-toast';

const signupSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  confirmPassword: z.string(),
  terms: z.boolean().refine(val => val === true, 'You must accept the terms'),
  travelStyle: z.string().optional(),
  interests: z.array(z.string()).optional(),
  budgetRange: z.string().optional(),
}).refine(data => data.password === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword'],
});

type SignupForm = z.infer<typeof signupSchema>;

const travelStyles = [
  { value: 'cultural_immersion', label: 'Cultural Immersion', description: 'Deep cultural connections, local life' },
  { value: 'food_wine', label: 'Food & Wine', description: 'Culinary traditions, local flavors' },
  { value: 'history_heritage', label: 'History & Heritage', description: 'Ancient sites, historical narratives' },
  { value: 'nature_adventure', label: 'Nature & Adventure', description: 'Outdoor exploration, natural wonders' },
  { value: 'spiritual_wellness', label: 'Spiritual & Wellness', description: 'Sacred sites, mindfulness practices' },
  { value: 'arts_crafts', label: 'Arts & Crafts', description: 'Traditional arts, hands-on workshops' },
  { value: 'slow_travel', label: 'Slow Travel', description: 'Relaxed pace, deep connections' },
  { value: 'photography', label: 'Photography', description: 'Visual storytelling, light & culture' },
];

const interestsList = [
  'Traditional Crafts', 'Local Cuisine', 'Religious Sites', 'Festivals & Ceremonies',
  'Indigenous Culture', 'Historical Architecture', 'Music & Dance', 'Language Learning',
  'Sustainable Tourism', 'Community Homestays', 'Artisan Workshops', 'Sacred Rituals',
  'Oral Traditions', 'Traditional Medicine', 'Agricultural Practices', 'Maritime Heritage',
];

const budgetRanges = [
  { value: 'budget', label: 'Budget ($30-80/day)', description: 'Hostels, street food, local transport' },
  { value: 'mid_range', label: 'Mid-Range ($80-250/day)', description: 'Comfortable hotels, mixed dining' },
  { value: 'luxury', label: 'Luxury ($250+/day)', description: 'Premium experiences, private guides' },
];

export default function SignupPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const callbackUrl = searchParams.get('callbackUrl') || '/onboarding';
  
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [step, setStep] = useState(1);
  
  const {
    register,
    handleSubmit,
    watch,
    setValue,
    formState: { errors },
  } = useForm<SignupForm>({
    resolver: zodResolver(signupSchema),
    defaultValues: {
      terms: false,
    },
  });

  const onSubmit = async (data: SignupForm) => {
    if (step === 1) {
      setStep(2);
      return;
    }
    
    setIsLoading(true);
    try {
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      toast.success('Account created! Welcome to CultureCompass!');
      router.push(callbackUrl);
      router.refresh();
    } catch (error) {
      toast.error('Signup failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const renderStep1 = () => (
    <div className="space-y-6 animate-slide-up">
      <div>
        <label htmlFor="name" className="block text-sm font-medium text-foreground mb-2">
          Full Name
        </label>
        <div className="relative">
          <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
          <input
            {...register('name')}
            id="name"
            type="text"
            autoComplete="name"
            className="w-full pl-10 pr-4 py-3 border border-input bg-background rounded-lg text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
            placeholder="Alex Johnson"
            disabled={isLoading}
          />
        </div>
        {errors.name && <p className="mt-1 text-sm text-destructive">{errors.name.message}</p>}
      </div>

      <div>
        <label htmlFor="email" className="block text-sm font-medium text-foreground mb-2">
          Email Address
        </label>
        <div className="relative">
          <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
          <input
            {...register('email')}
            id="email"
            type="email"
            autoComplete="email"
            className="w-full pl-10 pr-4 py-3 border border-input bg-background rounded-lg text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
            placeholder="you@example.com"
            disabled={isLoading}
          />
        </div>
        {errors.email && <p className="mt-1 text-sm text-destructive">{errors.email.message}</p>}
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium text-foreground mb-2">
          Password
        </label>
        <div className="relative">
          <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
          <input
            {...register('password')}
            id="password"
            type={showPassword ? 'text' : 'password'}
            autoComplete="new-password"
            className="w-full pl-10 pr-12 py-3 border border-input bg-background rounded-lg text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
            placeholder="••••••••"
            disabled={isLoading}
          />
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
          >
            {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
          </button>
        </div>
        {errors.password && <p className="mt-1 text-sm text-destructive">{errors.password.message}</p>}
      </div>

      <div>
        <label htmlFor="confirmPassword" className="block text-sm font-medium text-foreground mb-2">
          Confirm Password
        </label>
        <div className="relative">
          <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
          <input
            {...register('confirmPassword')}
            id="confirmPassword"
            type={showConfirmPassword ? 'text' : 'password'}
            autoComplete="new-password"
            className="w-full pl-10 pr-12 py-3 border border-input bg-background rounded-lg text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
            placeholder="••••••••"
            disabled={isLoading}
          />
          <button
            type="button"
            onClick={() => setShowConfirmPassword(!showConfirmPassword)}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
          >
            {showConfirmPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
          </button>
        </div>
        {errors.confirmPassword && <p className="mt-1 text-sm text-destructive">{errors.confirmPassword.message}</p>}
      </div>

      <div className="flex items-start gap-3">
        <input
          {...register('terms')}
          id="terms"
          type="checkbox"
          className="mt-1 w-4 h-4 rounded border-border text-primary focus:ring-primary"
        />
        <label htmlFor="terms" className="text-sm text-muted-foreground">
          I agree to the{' '}
          <Link href="/terms" className="text-primary hover:underline">Terms of Service</Link>
          {' '}and{' '}
          <Link href="/privacy" className="text-primary hover:underline">Privacy Policy</Link>
        </label>
      </div>
      {errors.terms && <p className="text-sm text-destructive">{errors.terms.message}</p>}

      <button
        type="submit"
        disabled={isLoading}
        className="w-full py-3 px-4 bg-primary text-primary-foreground rounded-lg font-medium text-base hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 disabled:opacity-50 transition-all flex items-center justify-center gap-2"
      >
        {isLoading ? (
          <>
            <Loader2 className="w-5 h-5 animate-spin" />
            Creating account...
          </>
        ) : (
          <>
            Continue
            <ArrowRight className="w-4 h-4" />
          </>
        )}
      </button>
    </div>
  );

  const renderStep2 = () => {
    const watchedTravelStyle = watch('travelStyle');
    const watchedInterests = watch('interests') || [];
    
    return (
      <div className="space-y-6 animate-slide-up">
        <div>
          <label className="block text-sm font-medium text-foreground mb-3">
            What\'s your travel style? <span className="text-muted-foreground font-normal">(Select one)</span>
          </label>
          <div className="grid grid-cols-2 gap-3">
            {travelStyles.map((style) => (
              <button
                type="button"
                onClick={() => setValue('travelStyle', style.value)}
                className={`p-4 rounded-xl border-2 text-left transition-all ${
                  watchedTravelStyle === style.value
                    ? 'border-primary bg-primary/5'
                    : 'border-border hover:border-primary/50'
                }`}
              >
                <div className="font-medium text-foreground">{style.label}</div>
                <div className="text-sm text-muted-foreground mt-1">{style.description}</div>
              </button>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-foreground mb-3">
            What cultural interests excite you? <span className="text-muted-foreground font-normal">(Select all that apply)</span>
          </label>
          <div className="flex flex-wrap gap-2 max-h-60 overflow-y-auto pr-2">
            {interestsList.map((interest) => (
              <button
                key={interest}
                type="button"
                onClick={() => {
                  const current = watchedInterests || [];
                  if (current.includes(interest)) {
                    setValue('interests', current.filter(i => i !== interest));
                  } else {
                    setValue('interests', [...current, interest]);
                  }
                }}
                className={`px-3 py-2 rounded-full text-sm transition-all ${
                  watchedInterests.includes(interest)
                    ? 'bg-primary text-primary-foreground'
                    : 'bg-muted text-muted-foreground hover:bg-primary/10 hover:text-primary'
                }`}
              >
                {interest}
              </button>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-foreground mb-3">
            What\'s your typical daily budget?
          </label>
          <div className="grid grid-cols-3 gap-3">
            {budgetRanges.map((budget) => (
              <button
                type="button"
                onClick={() => setValue('budgetRange', budget.value)}
                className={`p-4 rounded-xl border-2 text-center transition-all ${
                  watchedInterests === budget.value
                    ? 'border-primary bg-primary/5'
                    : 'border-border hover:border-primary/50/50'
                }`}
              >
                <div className="font-medium text-foreground">{budget.label}</div>
                <div className="text-sm text-muted-foreground mt-1">{budget.description}</div>
              </button>
            ))}
          </div>
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className="w-full py-3 px-4 bg-primary text-primary-foreground rounded-lg font-medium text-base hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 disabled:opacity-50 transition-all flex items-center justify-center gap-2"
        >
          {isLoading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Creating account...
            </>
          ) : (
            <>
              Create Account
              <ArrowRight className="w-4 h-4" />
            </>
          )}
        </button>
      </div>
    );
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary/5 via-background to-accent/5 px-4 py-12">
      <div className="w-full max-w-md">
        <Link href="/" className="inline-flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors mb-8">
          <Globe className="w-5 h-5" />
          Back to Home
        </Link>

        <div className="bg-card border border-border rounded-2xl p-8 shadow-xl">
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-primary to-accent mx-auto mb-4">
              <Globe className="w-8 h-8 text-white" />
            </div>
            <h1 className="font-playfair text-3xl font-bold text-foreground mb-2">
              {step === 1 ? 'Create Your Account' : 'Personalize Your Journey'}
            </h1>
            <p className="text-muted-foreground">
              {step === 1 
                ? 'Start your cultural travel journey in minutes'
                : 'Help us curate experiences that match your passions'}
            </p>
          </div>

          <div className="mb-8">
            <div className="flex items-center justify-between">
              {[1, 2].map((s) => (
                <div key={s} className="flex items-center gap-2">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${
                    step >= s ? 'bg-primary text-primary-foreground' : 'bg-muted text-muted-foreground'
                  }`}>
                    {step > s ? <CheckCircle className="w-5 h-5" /> : s}
                  </div>
                  {s < 2 && <div className={`w-16 h-1 ${
                    step > s ? 'bg-primary' : 'bg-border'
                  }`} />}
                </div>
              ))}
            </div>
            <div className="flex justify-between text-xs text-muted-foreground mt-2 px-4">
              <span>Account</span>
              <span>Preferences</span>
            </div>
          </div>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            {step === 1 ? renderStep1() : renderStep2()}
          </form>

          <div className="mt-6 text-center">
            <p className="text-muted-foreground">
              Already have an account?{' '}
              <Link href="/auth/login" className="text-primary font-medium hover:underline">
                Sign in
              </Link>
            </p>
          </div>
        </div>

        <div className="mt-6 p-4 bg-muted/50 rounded-xl border border-border/50">
          <div className="flex items-start gap-3">
            <Sparkles className="w-5 h-5 text-primary mt-0.5 flex-shrink-0" />
            <div className="text-sm text-muted-foreground">
              <p className="font-medium text-foreground mb-1">Demo Mode</p>
              <p>
                This is a hackathon demo. In production, this would integrate with Firebase Authentication
                and store preferences for personalized AI recommendations.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}