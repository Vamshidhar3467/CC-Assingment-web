"""
TALYOUTH SDG Leadership Program - Enhanced Flask Application
Complete version with video library, fixed mentor authentication, and SDG courses
"""

import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from sqlalchemy.orm import DeclarativeBase
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import xml.etree.ElementTree as ET

# Configure logging
logging.basicConfig(level=logging.INFO)

class Base(DeclarativeBase):
    pass

# Initialize extensions
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

# Enhanced Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    age = db.Column(db.Integer)
    location = db.Column(db.String(100))
    user_type = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    participant_profile = db.relationship('ParticipantProfile', backref='user', uselist=False)
    mentor_profile = db.relationship('MentorProfile', backref='user', uselist=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

class ParticipantProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    chosen_sdg = db.Column(db.Integer, nullable=False)
    school_organization = db.Column(db.String(200))
    availability = db.Column(db.String(100))
    program_theme = db.Column(db.String(50))
    progress_percentage = db.Column(db.Integer, default=0)
    current_week = db.Column(db.Integer, default=1)
    
    # Relationships
    weekly_reflections = db.relationship('WeeklyReflection', backref='participant')
    mentor_feedbacks = db.relationship('MentorFeedback', backref='participant')
    course_progress = db.relationship('CourseProgress', backref='participant')

class MentorProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    expertise_areas = db.Column(db.Text)
    organization = db.Column(db.String(200))
    bio = db.Column(db.Text)
    is_approved = db.Column(db.Boolean, default=True)
    phone = db.Column(db.String(20))
    linkedin_url = db.Column(db.String(200))
    
    # Relationships
    assigned_participants = db.relationship('ParticipantProfile', 
                                          secondary='mentor_participant_assignment',
                                          backref='assigned_mentors')
    mentor_feedbacks = db.relationship('MentorFeedback', backref='mentor')

# Association table for mentor-participant assignments
mentor_participant_assignment = db.Table('mentor_participant_assignment',
    db.Column('mentor_id', db.Integer, db.ForeignKey('mentor_profile.id'), primary_key=True),
    db.Column('participant_id', db.Integer, db.ForeignKey('participant_profile.id'), primary_key=True)
)

# NEW: Video and Course Models
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    sdg_focus = db.Column(db.Integer, nullable=False)
    difficulty_level = db.Column(db.String(20), default='Beginner')
    duration_weeks = db.Column(db.Integer, default=4)
    thumbnail_url = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    videos = db.relationship('Video', backref='course', lazy='dynamic')
    course_progress = db.relationship('CourseProgress', backref='course')

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    video_url = db.Column(db.String(500), nullable=False)
    duration_minutes = db.Column(db.Integer)
    week_number = db.Column(db.Integer, nullable=False)
    order_in_week = db.Column(db.Integer, default=1)
    thumbnail_url = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    video_progress = db.relationship('VideoProgress', backref='video')

class CourseProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey('participant_profile.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    current_week = db.Column(db.Integer, default=1)
    completion_percentage = db.Column(db.Integer, default=0)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Relationships
    video_progress = db.relationship('VideoProgress', backref='course_progress')

class VideoProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_progress_id = db.Column(db.Integer, db.ForeignKey('course_progress.id'), nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    watched_duration = db.Column(db.Integer, default=0)
    completed_at = db.Column(db.DateTime)

class WeeklyReflection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey('participant_profile.id'), nullable=False)
    week_number = db.Column(db.Integer, nullable=False)
    theme = db.Column(db.String(50), nullable=False)
    
    # Reflection questions
    what_learned = db.Column(db.Text)
    challenges_faced = db.Column(db.Text)
    team_contribution = db.Column(db.Text)
    additional_notes = db.Column(db.Text)
    
    # File uploads
    uploaded_files = db.Column(db.Text)
    
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_complete = db.Column(db.Boolean, default=False)

class MentorFeedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey('participant_profile.id'), nullable=False)
    mentor_id = db.Column(db.Integer, db.ForeignKey('mentor_profile.id'), nullable=False)
    week_number = db.Column(db.Integer, nullable=False)
    
    # Ratings (1-5 scale)
    participation_rating = db.Column(db.Integer)
    creativity_rating = db.Column(db.Integer)
    collaboration_rating = db.Column(db.Integer)
    initiative_rating = db.Column(db.Integer)
    
    # Qualitative feedback
    comments = db.Column(db.Text)
    suggestions = db.Column(db.Text)
    flag_for_support = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey('participant_profile.id'), nullable=False)
    badge_name = db.Column(db.String(100), nullable=False)
    badge_description = db.Column(db.Text)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)
    week_earned = db.Column(db.Integer)
    
    participant = db.relationship('ParticipantProfile', backref='achievements')

# Helper for safe XML text extraction
def get_xml_text(element, tag):
    found = element.find(tag)
    return found.text if found is not None else ""

def load_curriculum_xml():
    """Load curriculum data from XML file"""
    try:
        tree = ET.parse('static/data/curriculum.xml')
        root = tree.getroot()
        
        curriculum = []
        for theme in root.findall('theme'):
            theme_data = {
                'name': theme.get('name'),
                'title': get_xml_text(theme, 'title'),
                'description': get_xml_text(theme, 'description'),
                'weeks': []
            }
            
            for week in theme.findall('week'):
                number_str = week.get('number')
                week_data = {
                    'number': int(number_str) if number_str is not None else 0,
                    'title': get_xml_text(week, 'title'),
                    'description': get_xml_text(week, 'description'),
                    'activities': [activity.text for activity in week.findall('activity') if activity is not None and activity.text is not None]
                }
                theme_data['weeks'].append(week_data)
            
            curriculum.append(theme_data)
        
        return curriculum
    except Exception as e:
        logging.error(f"Error loading curriculum XML: {e}")
        return []

def load_sdg_xml():
    """Load SDG data from XML file"""
    try:
        tree = ET.parse('static/data/sdgs.xml')
        root = tree.getroot()
        
        sdgs = []
        for sdg in root.findall('sdg'):
            number_str = sdg.get('number')
            sdg_data = {
                'number': int(number_str) if number_str is not None else 0,
                'title': get_xml_text(sdg, 'title'),
                'description': get_xml_text(sdg, 'description'),
                'color': get_xml_text(sdg, 'color')
            }
            sdgs.append(sdg_data)
        
        return sdgs
    except Exception as e:
        logging.error(f"Error loading SDG XML: {e}")
        return []

def initialize_sample_courses():
    """Initialize sample SDG courses with videos"""
    if Course.query.count() == 0:
        # SDG 2: Zero Hunger Course
        course_sdg2 = Course(
            title="SDG 2: Zero Hunger - Building Food Security",
            description="Learn about sustainable agriculture, food systems, and combating hunger worldwide through innovative solutions and community action.",
            sdg_focus=2,
            difficulty_level="Beginner",
            duration_weeks=4,
            thumbnail_url="https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=800"
        )
        db.session.add(course_sdg2)
        db.session.flush()
        
        # SDG 2 Videos (2-3 per week)
        sdg2_videos = [
            # Week 1
            {"title": "Understanding Global Hunger", "description": "Overview of food insecurity worldwide", "url": "https://www.youtube.com/embed/TlXYNk1hBrw", "week": 1, "order": 1, "duration": 15},
            {"title": "Sustainable Agriculture Basics", "description": "Introduction to sustainable farming practices", "url": "https://www.youtube.com/embed/QnddqZoJ8wQ", "week": 1, "order": 2, "duration": 20},
            
            # Week 2  
            {"title": "Food Systems and Supply Chains", "description": "How food gets from farm to table", "url": "https://www.youtube.com/embed/ykfp1WvVqAY", "week": 2, "order": 1, "duration": 18},
            {"title": "Community Gardens and Urban Farming", "description": "Local solutions for food security", "url": "https://www.youtube.com/embed/YhvfOlPYifY", "week": 2, "order": 2, "duration": 22},
            {"title": "Technology in Agriculture", "description": "Modern tech solutions for farming", "url": "https://www.youtube.com/embed/F7o8gm4LQU8", "week": 2, "order": 3, "duration": 16},
            
            # Week 3
            {"title": "Food Waste Reduction", "description": "Strategies to minimize food waste", "url": "https://www.youtube.com/embed/6RlxySFrkIM", "week": 3, "order": 1, "duration": 19},
            {"title": "Nutrition and Health", "description": "Understanding nutritional needs", "url": "https://www.youtube.com/embed/bpFk7tR8L30", "week": 3, "order": 2, "duration": 21},
            
            # Week 4
            {"title": "Policy and Advocacy", "description": "How policy affects food security", "url": "https://www.youtube.com/embed/VhIhLZTb_mA", "week": 4, "order": 1, "duration": 17},
            {"title": "Taking Action: Your Food Security Project", "description": "Planning your community project", "url": "https://www.youtube.com/embed/M-4Ay3JaBcw", "week": 4, "order": 2, "duration": 25}
        ]
        
        for video_data in sdg2_videos:
            video = Video(
                course_id=course_sdg2.id,
                title=video_data["title"],
                description=video_data["description"],
                video_url=video_data["url"],
                duration_minutes=video_data["duration"],
                week_number=video_data["week"],
                order_in_week=video_data["order"],
                thumbnail_url="https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400"
            )
            db.session.add(video)
        
        # SDG 3: Good Health Course
        course_sdg3 = Course(
            title="SDG 3: Good Health and Well-being for All",
            description="Explore global health challenges, healthcare systems, and innovative approaches to promoting health and well-being in communities.",
            sdg_focus=3,
            difficulty_level="Beginner", 
            duration_weeks=4,
            thumbnail_url="https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=800"
        )
        db.session.add(course_sdg3)
        db.session.flush()
        
        # SDG 3 Videos (2-3 per week)
        sdg3_videos = [
            # Week 1
            {"title": "Global Health Overview", "description": "Understanding world health challenges", "url": "https://www.youtube.com/embed/36xvKx0NbI0", "week": 1, "order": 1, "duration": 16},
            {"title": "Healthcare Systems Around the World", "description": "Comparing different healthcare models", "url": "https://www.youtube.com/embed/yN-MkRcOJjY", "week": 1, "order": 2, "duration": 23},
            
            # Week 2
            {"title": "Mental Health Awareness", "description": "Breaking stigma around mental health", "url": "https://www.youtube.com/embed/DxIDKZHW3-E", "week": 2, "order": 1, "duration": 20},
            {"title": "Community Health Programs", "description": "Grassroots health initiatives", "url": "https://www.youtube.com/embed/CuFMGjFx3-8", "week": 2, "order": 2, "duration": 18},
            {"title": "Health Technology and Innovation", "description": "Tech solutions for healthcare", "url": "https://www.youtube.com/embed/CMn-nYCwmvo", "week": 2, "order": 3, "duration": 21},
            
            # Week 3
            {"title": "Health Education and Promotion", "description": "Teaching healthy lifestyle choices", "url": "https://www.youtube.com/embed/aUaInS6HIGo", "week": 3, "order": 1, "duration": 19},
            {"title": "Access to Healthcare", "description": "Addressing healthcare inequality", "url": "https://www.youtube.com/embed/U8FzGlgVGdo", "week": 3, "order": 2, "duration": 17},
            
            # Week 4
            {"title": "Health Policy and Advocacy", "description": "Influencing health policy change", "url": "https://www.youtube.com/embed/sJoxTktUHDU", "week": 4, "order": 1, "duration": 22},
            {"title": "Creating Your Health Initiative", "description": "Designing a community health project", "url": "https://www.youtube.com/embed/C74amJRp730", "week": 4, "order": 2, "duration": 26}
        ]
        
        for video_data in sdg3_videos:
            video = Video(
                course_id=course_sdg3.id,
                title=video_data["title"],
                description=video_data["description"],
                video_url=video_data["url"],
                duration_minutes=video_data["duration"],
                week_number=video_data["week"],
                order_in_week=video_data["order"],
                thumbnail_url="https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=400"
            )
            db.session.add(video)
        
        db.session.commit()
        logging.info("Sample SDG courses initialized successfully")

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Configuration
    app.secret_key = os.environ.get("SESSION_SECRET", "talyouth-local-dev-secret-2024")
    
    # Database configuration
    database_url = os.environ.get("DATABASE_URL", "sqlite:///talyouth.db")
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Create tables and initialize data
    with app.app_context():
        db.create_all()
        initialize_sample_courses()
    
    # Routes
    @app.route('/')
    def index():
        """Landing page with program overview"""
        sdgs = load_sdg_xml()
        recent_courses = Course.query.filter_by(is_active=True).order_by(Course.created_at.desc()).limit(4).all()
        return render_template('index.html', sdgs=sdgs, recent_courses=recent_courses)
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """Registration page for participants, mentors, and chapter heads"""
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            age = request.form.get('age')
            location = request.form.get('location')
            user_type = request.form.get('user_type')
            
            # Validation
            if not all([email, password, first_name, last_name, user_type]):
                flash('Please fill in all required fields.', 'error')
                return render_template('register.html', sdgs=load_sdg_xml())
            
            # Check if user already exists
            if User.query.filter_by(email=email).first():
                flash('Email already registered. Please use a different email or login.', 'error')
                return render_template('register.html', sdgs=load_sdg_xml())
            
            # Create new user
            user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                age=int(age) if age else None,
                location=location,
                user_type=user_type
            )
            user.set_password(password)
            
            try:
                db.session.add(user)
                db.session.commit()
                
                # Create profile based on user type
                if user_type == 'participant':
                    chosen_sdg = request.form.get('chosen_sdg')
                    school = request.form.get('school_organization')
                    availability = request.form.get('availability')
                    
                    profile = ParticipantProfile(
                        user_id=user.id,
                        chosen_sdg=int(chosen_sdg) if chosen_sdg else 1,
                        school_organization=school,
                        availability=availability
                    )
                    db.session.add(profile)
                    
                elif user_type == 'mentor':
                    expertise = request.form.get('expertise_areas')
                    organization = request.form.get('organization')
                    bio = request.form.get('bio')
                    phone = request.form.get('phone')
                    linkedin = request.form.get('linkedin_url')
                    
                    profile = MentorProfile(
                        user_id=user.id,
                        expertise_areas=expertise,
                        organization=organization,
                        bio=bio,
                        phone=phone,
                        linkedin_url=linkedin,
                        is_approved=True  # Auto-approve for demo
                    )
                    db.session.add(profile)
                
                db.session.commit()
                
                flash('Registration successful! Please login to continue.', 'success')
                return redirect(url_for('login'))
                
            except Exception as e:
                db.session.rollback()
                logging.error(f"Registration error: {e}")
                flash('Registration failed. Please try again.', 'error')
        
        return render_template('register.html', sdgs=load_sdg_xml())
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """FIXED: Login page with improved mentor authentication"""
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            
            if not email or not password:
                flash('Please enter both email and password.', 'error')
                return render_template('login.html')
            
            user = User.query.filter_by(email=email).first()
            
            if user and user.check_password(password):
                # Check if user is active
                if not user.is_active:
                    flash('Your account has been deactivated. Please contact support.', 'error')
                    return render_template('login.html')
                
                # FIXED: Mentor login validation
                if user.user_type == 'mentor':
                    if not user.mentor_profile:
                        flash('Mentor profile not found. Please contact admin.', 'error')
                        return render_template('login.html')
                    
                    if not user.mentor_profile.is_approved:
                        flash('Your mentor account is pending approval. Please contact admin.', 'warning')
                        return render_template('login.html')
                
                # Update last login
                user.last_login = datetime.utcnow()
                db.session.commit()
                
                # Convert remember_me to boolean (checkbox returns 'on' if checked)
                remember = request.form.get('remember_me') == 'on'
                login_user(user, remember=remember)
                flash(f'Welcome back, {user.first_name}!', 'success')
                
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)
                
                # Redirect based on user type
                if user.user_type == 'participant':
                    return redirect(url_for('learning_hub'))
                elif user.user_type == 'mentor':
                    return redirect(url_for('mentor_dashboard'))
                else:
                    return redirect(url_for('index'))
            else:
                flash('Invalid email or password.', 'error')
        
        return render_template('login.html')
    
    @app.route('/logout')
    @login_required
    def logout():
        """Logout user"""
        name = current_user.first_name
        logout_user()
        flash(f'Goodbye, {name}! You have been logged out.', 'info')
        return redirect(url_for('index'))
    
    @app.route('/learning-hub')
    @login_required
    def learning_hub():
        """Learning hub - restricted to registered participants"""
        if current_user.user_type not in ['participant', 'mentor']:
            flash('Access denied. This section is for program participants and mentors only.', 'error')
            return redirect(url_for('index'))
        
        curriculum_data = load_curriculum_xml()
        return render_template('learning_hub.html', curriculum=curriculum_data)
    
    # NEW: Video Library Routes
    @app.route('/video-library')
    @login_required
    def video_library():
        """Video library with SDG courses"""
        if current_user.user_type not in ['participant', 'mentor']:
            flash('Access denied. This section is for program participants and mentors only.', 'error')
            return redirect(url_for('index'))
        
        courses = Course.query.filter_by(is_active=True).all()
        
        # Get user's course progress if participant
        user_progress = {}
        if current_user.user_type == 'participant' and current_user.participant_profile:
            progress_records = CourseProgress.query.filter_by(
                participant_id=current_user.participant_profile.id
            ).all()
            user_progress = {progress.course_id: progress for progress in progress_records}
        
        return render_template('video_library.html', courses=courses, user_progress=user_progress)
    
    @app.route('/course/<int:course_id>')
    @login_required
    def course_detail(course_id):
        """Course detail page with videos organized by week"""
        if current_user.user_type not in ['participant', 'mentor']:
            flash('Access denied.', 'error')
            return redirect(url_for('index'))
        
        course = Course.query.get_or_404(course_id)
        
        # Get videos organized by week
        videos_by_week = {}
        videos = Video.query.filter_by(course_id=course_id).order_by(Video.week_number, Video.order_in_week).all()
        
        for video in videos:
            if video.week_number not in videos_by_week:
                videos_by_week[video.week_number] = []
            videos_by_week[video.week_number].append(video)
        
        # Get or create course progress for participants
        course_progress = None
        if current_user.user_type == 'participant' and current_user.participant_profile:
            course_progress = CourseProgress.query.filter_by(
                participant_id=current_user.participant_profile.id,
                course_id=course_id
            ).first()
            
            if not course_progress:
                course_progress = CourseProgress(
                    participant_id=current_user.participant_profile.id,
                    course_id=course_id
                )
                db.session.add(course_progress)
                db.session.commit()
        
        return render_template('course_detail.html', 
                             course=course, 
                             videos_by_week=videos_by_week,
                             course_progress=course_progress)
    
    @app.route('/watch/<int:video_id>')
    @login_required
    def watch_video(video_id):
        """Video watching page"""
        if current_user.user_type not in ['participant', 'mentor']:
            flash('Access denied.', 'error')
            return redirect(url_for('index'))
        
        video = Video.query.get_or_404(video_id)
        course = video.course
        
        # Get other videos in the course for navigation
        other_videos = Video.query.filter_by(course_id=course.id).order_by(Video.week_number, Video.order_in_week).all()

    
        return render_template('watch_video.html', 
                             video=video, 
                             course=course,
                             other_videos=other_videos)
    
    @app.route('/student-progress')
    @login_required
    def student_progress():
        # Get the participant profile for the current user
        participant = getattr(current_user, 'participant_profile', None)
        if not participant:
            flash('Participant profile not found. This page is only for participants.', 'error')
            return redirect(url_for('index'))

        # Safe fallback values
        completed_videos = 0
        total_videos = 18
        current_week = participant.current_week if hasattr(participant, 'current_week') else 1
        achievements = []
        overall_progress = participant.progress_percentage if hasattr(participant, 'progress_percentage') else 0
        course_progress = []

        try:
            # Count all videos
            total_videos = Video.query.count() if Video.query.count() > 0 else 18
            # Calculate overall progress 
            overall_progress = participant.progress_percentage if hasattr(participant, 'progress_percentage') else 0
            # Mock completed videos based on progress
            completed_videos = int((overall_progress / 100) * total_videos)
            # Get course progress
            courses = Course.query.all()
            for course in courses:
                course_progress.append({
                    'course': course,
                    'completion_percentage': overall_progress,
                    'current_week': current_week,
                    'started_at': getattr(current_user, 'created_at', None)
                })
            # Mock achievements
            achievements = [
                {'name': 'Getting Started', 'description': 'Completed Week 1', 'icon': 'fa-play', 'earned': overall_progress >= 25},
                {'name': 'Halfway There', 'description': 'Completed Week 2', 'icon': 'fa-star', 'earned': overall_progress >= 50},
                {'name': 'Almost There', 'description': 'Completed Week 3', 'icon': 'fa-trophy', 'earned': overall_progress >= 75},
                {'name': 'Course Complete', 'description': 'Complete all 4 weeks', 'icon': 'fa-graduation-cap', 'earned': overall_progress == 100}
            ]
        except Exception as e:
            print(f"Error calculating progress: {e}")
            pass

        return render_template('student_progress.html',
                            participant=participant,
                            overall_progress=overall_progress,
                            completed_videos=completed_videos,
                            total_videos=total_videos,
                            current_week=current_week,
                            achievements=achievements,
                            course_progress=course_progress)
    # Add this to your app_local.py file
    @app.template_filter('datetimeformat')
    def datetimeformat(value, format='%B %d, %Y at %I:%M %p'):
        """Format a datetime object."""
        if value is None:
            return ""
        return value.strftime(format)

    @app.route('/mentor-dashboard')
    @login_required
    def mentor_dashboard():
        """FIXED: Mentor dashboard with proper authentication"""
        if current_user.user_type != 'mentor':
            flash('Access denied. This section is for mentors only.', 'error')
            return redirect(url_for('index'))
        
        mentor = current_user.mentor_profile
        if not mentor:
            flash('Mentor profile not found. Please contact admin.', 'error')
            return redirect(url_for('index'))
        
        # Get assigned participants
        assigned_participants = mentor.assigned_participants
        
        # Get all participants for potential assignment (for demo)
        all_participants = ParticipantProfile.query.all()
        
        # Get recent feedback given
        recent_feedback = MentorFeedback.query.filter_by(
            mentor_id=mentor.id
        ).order_by(MentorFeedback.created_at.desc()).limit(10).all()
        
        return render_template('mentor_dashboard.html',
                             mentor=mentor,
                             mentor_profile=mentor,
                             assigned_participants=assigned_participants,
                             all_participants=all_participants,
                             recent_feedback=recent_feedback)
    
    @app.route('/api/mark-video-complete', methods=['POST'])
    @login_required
    def mark_video_complete():
        """API endpoint to mark video as completed"""
        if current_user.user_type != 'participant':
            return jsonify({'error': 'Access denied'}), 403
        
        data = request.get_json()
        video_id = data.get('video_id')
        
        if not video_id:
            return jsonify({'error': 'Video ID required'}), 400
        
        video = Video.query.get_or_404(video_id)
        participant = current_user.participant_profile
        
        # Get or create course progress
        course_progress = CourseProgress.query.filter_by(
            participant_id=participant.id,
            course_id=video.course_id
        ).first()
        
        if not course_progress:
            course_progress = CourseProgress(
                participant_id=participant.id,
                course_id=video.course_id
            )
            db.session.add(course_progress)
            db.session.flush()
        
        # Get or create video progress
        video_progress = VideoProgress.query.filter_by(
            course_progress_id=course_progress.id,
            video_id=video_id
        ).first()
        
        if not video_progress:
            video_progress = VideoProgress(
                course_progress_id=course_progress.id,
                video_id=video_id
            )
            db.session.add(video_progress)
        
        video_progress.is_completed = True
        video_progress.completed_at = datetime.utcnow()
        
        # Update course completion percentage
        total_videos = Video.query.filter_by(course_id=video.course_id).count()
        completed_videos = VideoProgress.query.join(Video).filter(
            VideoProgress.course_progress_id == course_progress.id,
            VideoProgress.is_completed == True,
            Video.course_id == video.course_id
        ).count()
        
        course_progress.completion_percentage = int((completed_videos / total_videos) * 100)
        
        if course_progress.completion_percentage == 100:
            course_progress.completed_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'completion_percentage': course_progress.completion_percentage
        })
    
    @app.route('/submit-reflection', methods=['POST'])
    @login_required
    def submit_reflection():
        # Placeholder: In the future, process and save the reflection form data here
        flash('Reflection submitted!', 'success')
        return redirect(url_for('student_progress'))
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)