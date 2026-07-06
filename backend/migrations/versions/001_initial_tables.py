"""Create initial tables

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create enum types
    user_role_enum = sa.Enum('user', 'admin', 'moderator', name='userrole')
    user_role_enum.create(op.get_bind(), checkfirst=True)
    
    trip_status_enum = sa.Enum('draft', 'planning', 'confirmed', 'in_progress', 'completed', 'cancelled', name='tripstatus')
    trip_status_enum.create(op.get_bind(), checkfirst=True)
    
    experience_type_enum = sa.Enum('workshop', 'homestay', 'craft', 'cooking_class', 'ceremony', 'festival', 'guided_tour', 'cultural_exchange', 'volunteer', 'performance', 'other', name='experiencetype')
    experience_type_enum.create(op.get_bind(), checkfirst=True)
    
    cuisine_type_enum = sa.Enum('street_food', 'family_recipe', 'restaurant', 'market', 'farm_to_table', 'cooking_class', 'food_tour', 'other', name='cuisinetype')
    cuisine_type_enum.create(op.get_bind(), checkfirst=True)
    
    # Users table
    op.create_table(
        'users',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('firebase_uid', sa.String(128), unique=True, nullable=False, index=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False, index=True),
        sa.Column('display_name', sa.String(255), nullable=True),
        sa.Column('photo_url', sa.String(500), nullable=True),
        sa.Column('role', user_role_enum, nullable=False, default='user'),
        sa.Column('travel_style', sa.Text, nullable=True),
        sa.Column('interests', sa.Text, nullable=True),
        sa.Column('budget_range', sa.String(50), nullable=True),
        sa.Column('dietary_restrictions', sa.Text, nullable=True),
        sa.Column('accessibility_needs', sa.Text, nullable=True),
        sa.Column('preferred_languages', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('last_login_at', sa.DateTime, nullable=True),
    )
    
    # Destinations table
    op.create_table(
        'destinations',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('google_place_id', sa.String(100), unique=True, index=True, nullable=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('short_description', sa.String(500), nullable=True),
        sa.Column('country', sa.String(100), nullable=False, index=True),
        sa.Column('region', sa.String(100), nullable=True, index=True),
        sa.Column('city', sa.String(100), nullable=True, index=True),
        sa.Column('address', sa.Text, nullable=True),
        sa.Column('latitude', sa.Float, nullable=True),
        sa.Column('longitude', sa.Float, nullable=True),
        sa.Column('categories', sa.Text, nullable=True),
        sa.Column('place_types', sa.Text, nullable=True),
        sa.Column('cultural_significance', sa.Text, nullable=True),
        sa.Column('unesco_heritage', sa.Boolean, nullable=False, default=False),
        sa.Column('photos', sa.Text, nullable=True),
        sa.Column('primary_photo', sa.String(500), nullable=True),
        sa.Column('opening_hours', sa.Text, nullable=True),
        sa.Column('website', sa.String(500), nullable=True),
        sa.Column('phone', sa.String(50), nullable=True),
        sa.Column('rating', sa.Float, nullable=True),
        sa.Column('review_count', sa.Integer, nullable=True),
        sa.Column('price_level', sa.Integer, nullable=True),
        sa.Column('historical_context', sa.Text, nullable=True),
        sa.Column('cultural_stories', sa.Text, nullable=True),
        sa.Column('local_tips', sa.Text, nullable=True),
        sa.Column('best_time_to_visit', sa.String(200), nullable=True),
        sa.Column('ai_summary', sa.Text, nullable=True),
        sa.Column('ai_cultural_narrative', sa.Text, nullable=True),
        sa.Column('ai_hidden_gems_nearby', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('last_verified_at', sa.DateTime, nullable=True),
    )
    
    # User saved destinations association table
    op.create_table(
        'user_saved_destinations',
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id'), primary_key=True),
        sa.Column('destination_id', sa.String(36), sa.ForeignKey('destinations.id'), primary_key=True),
        sa.Column('saved_at', sa.DateTime, nullable=False, default=sa.func.now()),
        sa.Column('notes', sa.Text, nullable=True),
    )
    
    # Trips table
    op.create_table(
        'trips',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id'), nullable=False, index=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('status', trip_status_enum, nullable=False, default='draft'),
        sa.Column('start_date', sa.DateTime, nullable=True),
        sa.Column('end_date', sa.DateTime, nullable=True),
        sa.Column('destination_country', sa.String(100), nullable=True),
        sa.Column('destination_city', sa.String(100), nullable=True),
        sa.Column('destination_region', sa.String(100), nullable=True),
        sa.Column('destination_coordinates', sa.String(100), nullable=True),
        sa.Column('budget_min', sa.Float, nullable=True),
        sa.Column('budget_max', sa.Float, nullable=True),
        sa.Column('currency', sa.String(3), nullable=False, default='USD'),
        sa.Column('travel_style', sa.Text, nullable=True),
        sa.Column('interests', sa.Text, nullable=True),
        sa.Column('group_size', sa.Integer, nullable=False, default=1),
        sa.Column('pace', sa.String(50), nullable=True),
        sa.Column('ai_generated_itinerary', sa.Text, nullable=True),
        sa.Column('ai_cultural_insights', sa.Text, nullable=True),
        sa.Column('ai_recommendations', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('confirmed_at', sa.DateTime, nullable=True),
    )
    
    # Hidden Gems table
    op.create_table(
        'hidden_gems',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('destination_id', sa.String(36), sa.ForeignKey('destinations.id'), nullable=False, index=True),
        sa.Column('google_place_id', sa.String(100), nullable=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('short_description', sa.String(500), nullable=True),
        sa.Column('address', sa.Text, nullable=True),
        sa.Column('latitude', sa.Float, nullable=True),
        sa.Column('longitude', sa.Float, nullable=True),
        sa.Column('cultural_significance', sa.Text, nullable=True),
        sa.Column('local_story', sa.Text, nullable=True),
        sa.Column('discovered_by', sa.String(255), nullable=True),
        sa.Column('categories', sa.Text, nullable=True),
        sa.Column('access_difficulty', sa.String(50), nullable=True),
        sa.Column('best_time_to_visit', sa.String(200), nullable=True),
        sa.Column('visit_duration_minutes', sa.Integer, nullable=True),
        sa.Column('photos', sa.Text, nullable=True),
        sa.Column('primary_photo', sa.String(500), nullable=True),
        sa.Column('verified_by_local', sa.Boolean, nullable=False, default=False),
        sa.Column('verification_notes', sa.Text, nullable=True),
        sa.Column('ai_cultural_narrative', sa.Text, nullable=True),
        sa.Column('ai_local_insights', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, default=sa.func.now(), onupdate=sa.func.now()),
    )
    
    # Cultural Events table
    op.create_table(
        'cultural_events',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('destination_id', sa.String(36), sa.ForeignKey('destinations.id'), nullable=False, index=True),
        sa.Column('external_id', sa.String(100), nullable=True),
        sa.Column('external_source', sa.String(50), nullable=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('short_description', sa.String(500), nullable=True),
        sa.Column('event_type', sa.String(100), nullable=False),
        sa.Column('categories', sa.Text, nullable=True),
        sa.Column('start_date', sa.DateTime, nullable=False, index=True),
        sa.Column('end_date', sa.DateTime, nullable=True),
        sa.Column('is_recurring', sa.Boolean, nullable=False, default=False),
        sa.Column('recurrence_pattern', sa.String(200), nullable=True),
        sa.Column('venue_name', sa.String(255), nullable=True),
        sa.Column('venue_address', sa.Text, nullable=True),
        sa.Column('latitude', sa.Float, nullable=True),
        sa.Column('longitude', sa.Float, nullable=True),
        sa.Column('cultural_significance', sa.Text, nullable=True),
        sa.Column('history', sa.Text, nullable=True),
        sa.Column('traditions', sa.Text, nullable=True),
        sa.Column('dress_code', sa.String(200), nullable=True),
        sa.Column('etiquette', sa.Text, nullable=True),
        sa.Column('ticket_required', sa.Boolean, nullable=False, default=False),
        sa.Column('ticket_url', sa.String(500), nullable=True),
        sa.Column('price_range', sa.String(100), nullable=True),
        sa.Column('capacity', sa.Integer, nullable=True),
        sa.Column('language', sa.String(100), nullable=True),
        sa.Column('accessibility_info', sa.Text, nullable=True),
        sa.Column('photos', sa.Text, nullable=True),
        sa.Column('primary_photo', sa.String(500), nullable=True),
        sa.Column('video_url', sa.String(500), nullable=True),
        sa.Column('organizer', sa.String(255), nullable=True),
        sa.Column('contact_email', sa.String(255), nullable=True),
        sa.Column('contact_phone', sa.String(50), nullable=True),
        sa.Column('website', sa.String(500), nullable=True),
        sa.Column('ai_cultural_narrative', sa.Text, nullable=True),
        sa.Column('ai_visitor_guide', sa.Text, nullable=True),
        sa.Column('ai_what_to_expect', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('last_verified_at', sa.DateTime, nullable=True),
    )
    
    # Cuisines table
    op.create_table(
        'cuisines',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('destination_id', sa.String(36), sa.ForeignKey('destinations.id'), nullable=False, index=True),
        sa.Column('google_place_id', sa.String(100), nullable=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('short_description', sa.String(500), nullable=True),
        sa.Column('cuisine_type', cuisine_type_enum, nullable=False),
        sa.Column('dish_category', sa.String(100), nullable=True),
        sa.Column('cultural_significance', sa.Text, nullable=True),
        sa.Column('history', sa.Text, nullable=True),
        sa.Column('region_of_origin', sa.String(200), nullable=True),
        sa.Column('traditional_occasion', sa.String(200), nullable=True),
        sa.Column('ingredients', sa.Text, nullable=True),
        sa.Column('allergens', sa.Text, nullable=True),
        sa.Column('dietary_tags', sa.Text, nullable=True),
        sa.Column('preparation_method', sa.Text, nullable=True),
        sa.Column('cooking_time_minutes', sa.Integer, nullable=True),
        sa.Column('venue_name', sa.String(255), nullable=True),
        sa.Column('address', sa.Text, nullable=True),
        sa.Column('latitude', sa.Float, nullable=True),
        sa.Column('longitude', sa.Float, nullable=True),
        sa.Column('price_range', sa.String(100), nullable=True),
        sa.Column('price_level', sa.Integer, nullable=True),
        sa.Column('photos', sa.Text, nullable=True),
        sa.Column('primary_photo', sa.String(500), nullable=True),
        sa.Column('recipe', sa.Text, nullable=True),
        sa.Column('serves', sa.Integer, nullable=True),
        sa.Column('ai_cultural_narrative', sa.Text, nullable=True),
        sa.Column('ai_pairing_suggestions', sa.Text, nullable=True),
        sa.Column('ai_local_insights', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, default=sa.func.now(), onupdate=sa.func.now()),
    )
    
    # Experiences table
    op.create_table(
        'experiences',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('destination_id', sa.String(36), sa.ForeignKey('destinations.id'), nullable=False, index=True),
        sa.Column('google_place_id', sa.String(100), nullable=True),
        sa.Column('external_id', sa.String(100), nullable=True),
        sa.Column('external_source', sa.String(50), nullable=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('short_description', sa.String(500), nullable=True),
        sa.Column('experience_type', experience_type_enum, nullable=False),
        sa.Column('categories', sa.Text, nullable=True),
        sa.Column('host_name', sa.String(255), nullable=True),
        sa.Column('host_bio', sa.Text, nullable=True),
        sa.Column('host_languages', sa.Text, nullable=True),
        sa.Column('host_verified', sa.Boolean, nullable=False, default=False),
        sa.Column('cultural_significance', sa.Text, nullable=True),
        sa.Column('tradition_preserved', sa.Text, nullable=True),
        sa.Column('community_impact', sa.Text, nullable=True),
        sa.Column('duration_hours', sa.Float, nullable=False),
        sa.Column('schedule', sa.Text, nullable=True),
        sa.Column('max_group_size', sa.Integer, nullable=True),
        sa.Column('min_group_size', sa.Integer, nullable=False, default=1),
        sa.Column('venue_name', sa.String(255), nullable=True),
        sa.Column('address', sa.Text, nullable=True),
        sa.Column('latitude', sa.Float, nullable=True),
        sa.Column('longitude', sa.Float, nullable=True),
        sa.Column('meeting_point', sa.Text, nullable=True),
        sa.Column('includes', sa.Text, nullable=True),
        sa.Column('excludes', sa.Text, nullable=True),
        sa.Column('what_to_bring', sa.Text, nullable=True),
        sa.Column('dress_code', sa.String(200), nullable=True),
        sa.Column('age_restriction', sa.String(100), nullable=True),
        sa.Column('skill_level', sa.String(50), nullable=True),
        sa.Column('physical_requirements', sa.Text, nullable=True),
        sa.Column('accessibility_info', sa.Text, nullable=True),
        sa.Column('language', sa.String(100), nullable=True),
        sa.Column('price_per_person', sa.Float, nullable=True),
        sa.Column('currency', sa.String(3), nullable=False, default='USD'),
        sa.Column('price_includes', sa.Text, nullable=True),
        sa.Column('booking_url', sa.String(500), nullable=True),
        sa.Column('cancellation_policy', sa.Text, nullable=True),
        sa.Column('instant_booking', sa.Boolean, nullable=False, default=False),
        sa.Column('rating', sa.Float, nullable=True),
        sa.Column('review_count', sa.Integer, nullable=True),
        sa.Column('photos', sa.Text, nullable=True),
        sa.Column('primary_photo', sa.String(500), nullable=True),
        sa.Column('video_url', sa.String(500), nullable=True),
        sa.Column('ai_cultural_narrative', sa.Text, nullable=True),
        sa.Column('ai_what_to_expect', sa.Text, nullable=True),
        sa.Column('ai_local_insights', sa.Text, nullable=True),
        sa.Column('ai_preparation_tips', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('last_verified_at', sa.DateTime, nullable=True),
    )
    
    # User saved experiences association table
    op.create_table(
        'user_saved_experiences',
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id'), primary_key=True),
        sa.Column('experience_id', sa.String(36), sa.ForeignKey('experiences.id'), primary_key=True),
        sa.Column('saved_at', sa.DateTime, nullable=False, default=sa.func.now()),
        sa.Column('notes', sa.Text, nullable=True),
    )
    
    # Stories table
    op.create_table(
        'stories',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('destination_id', sa.String(36), sa.ForeignKey('destinations.id'), nullable=False, index=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('summary', sa.String(500), nullable=True),
        sa.Column('story_type', sa.String(100), nullable=False),
        sa.Column('categories', sa.Text, nullable=True),
        sa.Column('culture_of_origin', sa.String(200), nullable=True),
        sa.Column('language_of_origin', sa.String(100), nullable=True),
        sa.Column('historical_period', sa.String(200), nullable=True),
        sa.Column('cultural_significance', sa.Text, nullable=True),
        sa.Column('source', sa.String(255), nullable=True),
        sa.Column('source_type', sa.String(100), nullable=True),
        sa.Column('collected_by', sa.String(255), nullable=True),
        sa.Column('collected_date', sa.DateTime, nullable=True),
        sa.Column('specific_location', sa.String(255), nullable=True),
        sa.Column('latitude', sa.Float, nullable=True),
        sa.Column('longitude', sa.Float, nullable=True),
        sa.Column('audio_url', sa.String(500), nullable=True),
        sa.Column('video_url', sa.String(500), nullable=True),
        sa.Column('photos', sa.Text, nullable=True),
        sa.Column('ai_generated', sa.Boolean, nullable=False, default=False),
        sa.Column('ai_model', sa.String(100), nullable=True),
        sa.Column('ai_prompt', sa.Text, nullable=True),
        sa.Column('ai_cultural_accuracy_reviewed', sa.Boolean, nullable=False, default=False),
        sa.Column('created_at', sa.DateTime, nullable=False, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, default=sa.func.now(), onupdate=sa.func.now()),
    )
    
    # Itinerary Days table
    op.create_table(
        'itinerary_days',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('trip_id', sa.String(36), sa.ForeignKey('trips.id'), nullable=False, index=True),
        sa.Column('day_number', sa.Integer, nullable=False),
        sa.Column('date', sa.DateTime, nullable=True),
        sa.Column('title', sa.String(255), nullable=True),
        sa.Column('theme', sa.String(255), nullable=True),
        sa.Column('notes', sa.Text, nullable=True),
        sa.Column('ai_day_narrative', sa.Text, nullable=True),
        sa.Column('ai_cultural_insights', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, default=sa.func.now(), onupdate=sa.func.now()),
    )
    
    # Itinerary Items table
    op.create_table(
        'itinerary_items',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('day_id', sa.String(36), sa.ForeignKey('itinerary_days.id'), nullable=False, index=True),
        sa.Column('destination_id', sa.String(36), sa.ForeignKey('destinations.id'), nullable=True),
        sa.Column('experience_id', sa.String(36), sa.ForeignKey('experiences.id'), nullable=True),
        sa.Column('hidden_gem_id', sa.String(36), sa.ForeignKey('hidden_gems.id'), nullable=True),
        sa.Column('cultural_event_id', sa.String(36), sa.ForeignKey('cultural_events.id'), nullable=True),
        sa.Column('cuisine_id', sa.String(36), sa.ForeignKey('cuisines.id'), nullable=True),
        sa.Column('item_type', sa.String(50), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('start_time', sa.String(10), nullable=True),
        sa.Column('end_time', sa.String(10), nullable=True),
        sa.Column('duration_minutes', sa.Integer, nullable=True),
        sa.Column('address', sa.Text, nullable=True),
        sa.Column('latitude', sa.Float, nullable=True),
        sa.Column('longitude', sa.Float, nullable=True),
        sa.Column('place_name', sa.String(255), nullable=True),
        sa.Column('estimated_cost', sa.Float, nullable=True),
        sa.Column('currency', sa.String(3), nullable=False, default='USD'),
        sa.Column('transport_mode', sa.String(50), nullable=True),
        sa.Column('transport_details', sa.Text, nullable=True),
        sa.Column('transport_duration_minutes', sa.Integer, nullable=True),
        sa.Column('transport_cost', sa.Float, nullable=True),
        sa.Column('ai_context', sa.Text, nullable=True),
        sa.Column('ai_cultural_tips', sa.Text, nullable=True),
        sa.Column('sort_order', sa.Integer, nullable=False, default=0),
        sa.Column('created_at', sa.DateTime, nullable=False, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, default=sa.func.now(), onupdate=sa.func.now()),
    )
    
    # Chat Sessions table
    op.create_table(
        'chat_sessions',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id'), nullable=False, index=True),
        sa.Column('trip_id', sa.String(36), sa.ForeignKey('trips.id'), nullable=True),
        sa.Column('title', sa.String(255), nullable=True),
        sa.Column('context', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('last_message_at', sa.DateTime, nullable=True),
    )
    
    # Chat Messages table
    op.create_table(
        'chat_messages',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('session_id', sa.String(36), sa.ForeignKey('chat_sessions.id'), nullable=False, index=True),
        sa.Column('role', sa.String(20), nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('tokens_used', sa.Integer, nullable=True),
        sa.Column('model', sa.String(100), nullable=True),
        sa.Column('function_calls', sa.Text, nullable=True),
        sa.Column('function_results', sa.Text, nullable=True),
        sa.Column('referenced_destinations', sa.Text, nullable=True),
        sa.Column('referenced_experiences', sa.Text, nullable=True),
        sa.Column('referenced_events', sa.Text, nullable=True),
        sa.Column('referenced_cuisines', sa.Text, nullable=True),
        sa.Column('referenced_stories', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, default=sa.func.now()),
    )
    
    # Create indexes
    op.create_index('ix_destinations_country_city', 'destinations', ['country', 'city'])
    op.create_index('ix_destinations_lat_lng', 'destinations', ['latitude', 'longitude'])
    op.create_index('ix_trips_user_status', 'trips', ['user_id', 'status'])
    op.create_index('ix_cultural_events_start_date', 'cultural_events', ['start_date'])
    op.create_index('ix_chat_sessions_user_last_msg', 'chat_sessions', ['user_id', 'last_message_at'])


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('chat_messages')
    op.drop_table('chat_sessions')
    op.drop_table('itinerary_items')
    op.drop_table('itinerary_days')
    op.drop_table('stories')
    op.drop_table('user_saved_experiences')
    op.drop_table('experiences')
    op.drop_table('cuisines')
    op.drop_table('cultural_events')
    op.drop_table('hidden_gems')
    op.drop_table('trips')
    op.drop_table('user_saved_destinations')
    op.drop_table('destinations')
    op.drop_table('users')
    
    # Drop enum types
    op.execute('DROP TYPE IF EXISTS userrole')
    op.execute('DROP TYPE IF EXISTS tripstatus')
    op.execute('DROP TYPE IF EXISTS experiencetype')
    op.execute('DROP TYPE IF EXISTS cuisinetype')