# from flask import Flask, request, jsonify, send_file
# from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS
# from flask_bcrypt import Bcrypt
# from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
# from flask_mail import Mail, Message
# from werkzeug.utils import secure_filename
# from datetime import datetime, timedelta
# import os
# import PyPDF2
# import re
# from collections import Counter
# import json
# import numpy as np
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.preprocessing import LabelEncoder
# import pickle
# import pandas as pd

# # Initialize Flask app
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placement_portal.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['JWT_SECRET_KEY'] = 'jwt-secret-key-change-in-production'
# app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
# app.config['UPLOAD_FOLDER'] = 'uploads'
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# # Email configuration
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'your-email@gmail.com'  # Change this
# app.config['MAIL_PASSWORD'] = 'your-app-password'  # Change this
# app.config['MAIL_DEFAULT_SENDER'] = 'placement@sreyas.edu'

# # Initialize extensions
# db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)
# jwt = JWTManager(app)
# mail = Mail(app)
# CORS(app)

# # Create upload folder if it doesn't exist
# os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
# os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'resumes'), exist_ok=True)
# os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'profile_pics'), exist_ok=True)
# os.makedirs('models', exist_ok=True)

# # ==================== DATABASE MODELS ====================

# class Admin(db.Model):
#     __tablename__ = 'admins'
    
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     password_hash = db.Column(db.String(200), nullable=False)
#     email = db.Column(db.String(100))
#     role = db.Column(db.String(50), default='admin')  # admin, super_admin
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

# class Student(db.Model):
#     __tablename__ = 'students'
    
#     id = db.Column(db.Integer, primary_key=True)
#     student_id = db.Column(db.String(50), unique=True, nullable=False)
#     password_hash = db.Column(db.String(200), nullable=False)
#     name = db.Column(db.String(100))
#     roll_number = db.Column(db.String(50), unique=True)
#     stream = db.Column(db.String(50))
#     dob = db.Column(db.Date)
#     gender = db.Column(db.String(20))
#     phone = db.Column(db.String(20))
#     email = db.Column(db.String(100))
#     cgpa = db.Column(db.Float)
#     tenth_percentage = db.Column(db.Float)
#     twelfth_percentage = db.Column(db.Float)
#     backlogs = db.Column(db.Integer, default=0)
#     resume_path = db.Column(db.String(200))
#     profile_pic_path = db.Column(db.String(200))
#     is_active = db.Column(db.Boolean, default=True)
#     placement_prediction = db.Column(db.Float)  # Probability of getting placed
#     predicted_package = db.Column(db.Float)  # Predicted package in LPA
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
#     # Relationships
#     skills = db.relationship('Skill', backref='student', lazy=True, cascade='all, delete-orphan')
#     certifications = db.relationship('Certification', backref='student', lazy=True, cascade='all, delete-orphan')
#     internships = db.relationship('Internship', backref='student', lazy=True, cascade='all, delete-orphan')
#     projects = db.relationship('Project', backref='student', lazy=True, cascade='all, delete-orphan')
#     applications = db.relationship('JobApplication', backref='student', lazy=True, cascade='all, delete-orphan')
#     startup_ideas = db.relationship('StartupIdea', backref='student', lazy=True, cascade='all, delete-orphan')
#     notifications = db.relationship('Notification', backref='student', lazy=True, cascade='all, delete-orphan')

# class Skill(db.Model):
#     __tablename__ = 'skills'
    
#     id = db.Column(db.Integer, primary_key=True)
#     student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
#     skill_name = db.Column(db.String(100), nullable=False)
#     proficiency = db.Column(db.String(50))  # Beginner, Intermediate, Advanced

# class Certification(db.Model):
#     __tablename__ = 'certifications'
    
#     id = db.Column(db.Integer, primary_key=True)
#     student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
#     name = db.Column(db.String(200), nullable=False)
#     issuer = db.Column(db.String(200))
#     date_obtained = db.Column(db.Date)

# class Internship(db.Model):
#     __tablename__ = 'internships'
    
#     id = db.Column(db.Integer, primary_key=True)
#     student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
#     company = db.Column(db.String(200), nullable=False)
#     role = db.Column(db.String(200))
#     duration = db.Column(db.String(100))
#     description = db.Column(db.Text)

# class Project(db.Model):
#     __tablename__ = 'projects'
    
#     id = db.Column(db.Integer, primary_key=True)
#     student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
#     name = db.Column(db.String(200), nullable=False)
#     tech_stack = db.Column(db.String(500))
#     description = db.Column(db.Text)
#     github_url = db.Column(db.String(200))

# class Job(db.Model):
#     __tablename__ = 'jobs'
    
#     id = db.Column(db.Integer, primary_key=True)
#     job_type = db.Column(db.String(50))  # mnc, startup
#     role = db.Column(db.String(200), nullable=False)
#     company = db.Column(db.String(200), nullable=False)
#     description = db.Column(db.Text)
#     required_skills = db.Column(db.Text)  # JSON array of skills
#     location = db.Column(db.String(200))
#     package_min = db.Column(db.Float)
#     package_max = db.Column(db.Float)
#     min_cgpa = db.Column(db.Float)
#     max_backlogs = db.Column(db.Integer, default=0)
#     eligible_streams = db.Column(db.Text)  # JSON array of streams
#     is_active = db.Column(db.Boolean, default=True)
#     posted_date = db.Column(db.DateTime, default=datetime.utcnow)
#     deadline = db.Column(db.DateTime)
#     total_positions = db.Column(db.Integer)
    
#     applications = db.relationship('JobApplication', backref='job', lazy=True, cascade='all, delete-orphan')

# class JobApplication(db.Model):
#     __tablename__ = 'job_applications'
    
#     id = db.Column(db.Integer, primary_key=True)
#     student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
#     job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
#     resume_path = db.Column(db.String(200))
#     ats_score = db.Column(db.Integer)
#     status = db.Column(db.String(50), default='applied')  # applied, shortlisted, rejected, selected
#     applied_date = db.Column(db.DateTime, default=datetime.utcnow)
#     interview_date = db.Column(db.DateTime)
#     feedback = db.Column(db.Text)

# class StartupIdea(db.Model):
#     __tablename__ = 'startup_ideas'
    
#     id = db.Column(db.Integer, primary_key=True)
#     student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
#     title = db.Column(db.String(200), nullable=False)
#     domain = db.Column(db.String(100))
#     problem_statement = db.Column(db.Text)
#     solution = db.Column(db.Text)
#     technology = db.Column(db.String(500))
#     likes = db.Column(db.Integer, default=0)
#     status = db.Column(db.String(50), default='pending')  # pending, approved, rejected
#     admin_feedback = db.Column(db.Text)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
#     liked_by = db.relationship('IdeaLike', backref='idea', lazy=True, cascade='all, delete-orphan')

# class IdeaLike(db.Model):
#     __tablename__ = 'idea_likes'
    
#     id = db.Column(db.Integer, primary_key=True)
#     student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
#     idea_id = db.Column(db.Integer, db.ForeignKey('startup_ideas.id'), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)


# class Notification(db.Model):
#     __tablename__ = 'notifications'
    
#     id = db.Column(db.Integer, primary_key=True)
#     student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
#     title = db.Column(db.String(200), nullable=False)
#     message = db.Column(db.Text)
#     notification_type = db.Column(db.String(50))  # job_posted, application_update, interview_scheduled
#     is_read = db.Column(db.Boolean, default=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

# class PlacementRecord(db.Model):
#     __tablename__ = 'placement_records'
    
#     id = db.Column(db.Integer, primary_key=True)
#     student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
#     company = db.Column(db.String(200))
#     package = db.Column(db.Float)
#     placement_year = db.Column(db.Integer)
#     placement_date = db.Column(db.DateTime, default=datetime.utcnow)

# # ==================== HELPER FUNCTIONS ====================

# def extract_text_from_pdf(pdf_path):
#     """Extract text content from PDF file"""
#     try:
#         text = ""
#         with open(pdf_path, 'rb') as file:
#             pdf_reader = PyPDF2.PdfReader(file)
#             for page in pdf_reader.pages:
#                 text += page.extract_text()
#         return text
#     except Exception as e:
#         print(f"Error extracting PDF text: {str(e)}")
#         return ""

# def detect_skills_from_text(text):
#     """Detect technical skills from text"""
#     skills_database = [
#         'Java', 'Python', 'JavaScript', 'C', 'C++', 'C#', 'TypeScript', 'PHP', 'Ruby', 
#         'Swift', 'Kotlin', 'Go', 'Rust', 'Scala', 'R', 'MATLAB', 'HTML', 'CSS', 
#         'React', 'Angular', 'Vue', 'Node.js', 'Express', 'Django', 'Flask', 'Spring',
#         'MySQL', 'PostgreSQL', 'MongoDB', 'Oracle', 'Redis', 'Firebase',
#         'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins', 'Git',
#         'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch', 'NLP',
#         'REST API', 'GraphQL', 'Microservices', 'Agile', 'Scrum'
#     ]
    
#     text_lower = text.lower()
#     detected = []
    
#     for skill in skills_database:
#         if skill.lower() in text_lower:
#             detected.append(skill)
    
#     return detected

# def calculate_ats_score(resume_text, required_skills):
#     """Calculate ATS matching score"""
#     detected_skills = detect_skills_from_text(resume_text)
#     required = json.loads(required_skills) if isinstance(required_skills, str) else required_skills
    
#     matching = [skill for skill in required if skill.lower() in [s.lower() for s in detected_skills]]
#     missing = [skill for skill in required if skill.lower() not in [s.lower() for s in detected_skills]]
    
#     score = int((len(matching) / len(required)) * 100) if required else 0
    
#     return {
#         'score': score,
#         'detected_skills': detected_skills,
#         'matching_skills': matching,
#         'missing_skills': missing,
#         'total_required': len(required),
#         'total_matched': len(matching)
#     }

# def send_email_notification(to_email, subject, body):
#     """Send email notification"""
#     try:
#         msg = Message(subject, recipients=[to_email])
#         msg.body = body
#         mail.send(msg)
#         return True
#     except Exception as e:
#         print(f"Email sending failed: {str(e)}")
#         return False

# def create_notification(student_id, title, message, notification_type):
#     """Create in-app notification"""
#     notification = Notification(
#         student_id=student_id,
#         title=title,
#         message=message,
#         notification_type=notification_type
#     )
#     db.session.add(notification)
#     db.session.commit()

# # ==================== ML PREDICTION FUNCTIONS ====================

# def train_placement_model():
#     """Train ML model for placement prediction"""
#     # Get all students with placement records
#     students = Student.query.all()
    
#     if len(students) < 10:
#         print("Not enough data to train model")
#         return None
    
#     data = []
#     for student in students:
#         placement_record = PlacementRecord.query.filter_by(student_id=student.id).first()
#         is_placed = 1 if placement_record else 0
        
#         data.append({
#             'cgpa': student.cgpa or 0,
#             'tenth': student.tenth_percentage or 0,
#             'twelfth': student.twelfth_percentage or 0,
#             'backlogs': student.backlogs or 0,
#             'skills_count': len(student.skills),
#             'internships_count': len(student.internships),
#             'projects_count': len(student.projects),
#             'certifications_count': len(student.certifications),
#             'is_placed': is_placed
#         })
    
#     df = pd.DataFrame(data)
    
#     X = df[['cgpa', 'tenth', 'twelfth', 'backlogs', 'skills_count', 
#             'internships_count', 'projects_count', 'certifications_count']]
#     y = df['is_placed']
    
#     model = RandomForestClassifier(n_estimators=100, random_state=42)
#     model.fit(X, y)
    
#     # Save model
#     with open('models/placement_model.pkl', 'wb') as f:
#         pickle.dump(model, f)
    
#     return model

# def predict_placement(student):
#     """Predict placement probability for a student"""
#     try:
#         with open('models/placement_model.pkl', 'rb') as f:
#             model = pickle.load(f)
#     except:
#         model = train_placement_model()
#         if not model:
#             return None
    
#     features = np.array([[
#         student.cgpa or 0,
#         student.tenth_percentage or 0,
#         student.twelfth_percentage or 0,
#         student.backlogs or 0,
#         len(student.skills),
#         len(student.internships),
#         len(student.projects),
#         len(student.certifications)
#     ]])
    
#     probability = model.predict_proba(features)[0][1]
#     return probability

# def predict_package(student):
#     """Predict expected package for a student"""
#     # Simple rule-based prediction (can be enhanced with ML)
#     base_package = 4.0
    
#     if student.cgpa:
#         if student.cgpa >= 9.0:
#             base_package += 8.0
#         elif student.cgpa >= 8.0:
#             base_package += 5.0
#         elif student.cgpa >= 7.0:
#             base_package += 3.0
    
#     # Add based on skills
#     base_package += len(student.skills) * 0.3
    
#     # Add based on internships
#     base_package += len(student.internships) * 1.5
    
#     # Add based on projects
#     base_package += len(student.projects) * 1.0
    
#     # Reduce based on backlogs
#     base_package -= (student.backlogs or 0) * 0.5
    
#     return max(base_package, 3.5)

# # ==================== ADMIN API ROUTES ====================

# @app.route('/api/admin/login', methods=['POST'])
# def admin_login():
#     """Admin login"""
#     data = request.json
#     admin = Admin.query.filter_by(username=data['username']).first()
    
#     if admin and bcrypt.check_password_hash(admin.password_hash, data['password']):
#         access_token = create_access_token(identity={'id': admin.id, 'role': 'admin'})
#         return jsonify({
#             'access_token': access_token,
#             'admin_id': admin.id,
#             'username': admin.username,
#             'role': getattr(admin, 'role', 'admin')
#         }), 200
    
#     return jsonify({'error': 'Invalid credentials'}), 401

# @app.route('/api/admin/dashboard', methods=['GET'])
# @jwt_required()
# def admin_dashboard():
#     """Get admin dashboard statistics"""
#     total_students = Student.query.filter_by(is_active=True).count()
#     total_jobs = Job.query.filter_by(is_active=True).count()
#     total_applications = JobApplication.query.count()
#     placed_students = PlacementRecord.query.count()
    
#     # Applications by status
#     applied = JobApplication.query.filter_by(status='applied').count()
#     shortlisted = JobApplication.query.filter_by(status='shortlisted').count()
#     selected = JobApplication.query.filter_by(status='selected').count()
#     rejected = JobApplication.query.filter_by(status='rejected').count()
    
#     # Stream-wise statistics
#     streams = db.session.query(Student.stream, db.func.count(Student.id)).group_by(Student.stream).all()
    
#     # Recent applications
#     recent_apps = JobApplication.query.order_by(JobApplication.applied_date.desc()).limit(10).all()
    
#     return jsonify({
#         'total_students': total_students,
#         'total_jobs': total_jobs,
#         'total_applications': total_applications,
#         'placed_students': placed_students,
#         'placement_percentage': round((placed_students / total_students * 100), 2) if total_students > 0 else 0,
#         'application_stats': {
#             'applied': applied,
#             'shortlisted': shortlisted,
#             'selected': selected,
#             'rejected': rejected
#         },
#         'stream_stats': [{'stream': s[0], 'count': s[1]} for s in streams],
#         'recent_applications': [{
#             'id': app.id,
#             'student_name': app.student.name,
#             'job_role': app.job.role,
#             'company': app.job.company,
#             'status': app.status,
#             'date': app.applied_date.isoformat()
#         } for app in recent_apps]
#     }), 200

# @app.route('/api/admin/students', methods=['GET'])
# @jwt_required()
# def admin_get_students():
#     """Get all students with filters"""
#     page = request.args.get('page', 1, type=int)
#     per_page = request.args.get('per_page', 20, type=int)
#     stream = request.args.get('stream')
#     search = request.args.get('search')
    
#     query = Student.query
    
#     if stream:
#         query = query.filter_by(stream=stream)
    
#     if search:
#         query = query.filter(
#             (Student.name.ilike(f'%{search}%')) |
#             (Student.roll_number.ilike(f'%{search}%')) |
#             (Student.student_id.ilike(f'%{search}%'))
#         )
    
#     students = query.paginate(page=page, per_page=per_page, error_out=False)
    
#     return jsonify({
#         'students': [{
#             'id': s.id,
#             'student_id': s.student_id,
#             'name': s.name,
#             'roll_number': s.roll_number,
#             'stream': s.stream,
#             'cgpa': s.cgpa,
#             'email': s.email,
#             'phone': s.phone,
#             'is_active': s.is_active,
#             'skills_count': len(s.skills),
#             'applications_count': len(s.applications),
#             'placement_prediction': s.placement_prediction,
#             'predicted_package': s.predicted_package
#         } for s in students.items],
#         'total': students.total,
#         'pages': students.pages,
#         'current_page': page
#     }), 200

# @app.route('/api/admin/students/<int:student_id>', methods=['GET'])
# @jwt_required()
# def admin_get_student_detail(student_id):
#     """Get detailed student information"""
#     student = Student.query.get(student_id)
    
#     if not student:
#         return jsonify({'error': 'Student not found'}), 404
    
#     return jsonify({
#         'id': student.id,
#         'student_id': student.student_id,
#         'name': student.name,
#         'roll_number': student.roll_number,
#         'stream': student.stream,
#         'dob': student.dob.isoformat() if student.dob else None,
#         'gender': student.gender,
#         'phone': student.phone,
#         'email': student.email,
#         'cgpa': student.cgpa,
#         'tenth_percentage': student.tenth_percentage,
#         'twelfth_percentage': student.twelfth_percentage,
#         'backlogs': student.backlogs,
#         'is_active': student.is_active,
#         'placement_prediction': student.placement_prediction,
#         'predicted_package': student.predicted_package,
#         'skills': [{'id': s.id, 'name': s.skill_name, 'proficiency': s.proficiency} for s in student.skills],
#         'certifications': [{'id': c.id, 'name': c.name, 'issuer': c.issuer, 'date': c.date_obtained.isoformat() if c.date_obtained else None} for c in student.certifications],
#         'internships': [{'id': i.id, 'company': i.company, 'role': i.role, 'duration': i.duration} for i in student.internships],
#         'projects': [{'id': p.id, 'name': p.name, 'tech': p.tech_stack, 'description': p.description} for p in student.projects],
#         'applications': [{
#             'id': app.id,
#             'job_role': app.job.role,
#             'company': app.job.company,
#             'status': app.status,
#             'ats_score': app.ats_score,
#             'applied_date': app.applied_date.isoformat()
#         } for app in student.applications]
#     }), 200

# @app.route('/api/admin/students/<int:student_id>/toggle-status', methods=['PUT'])
# @jwt_required()
# def admin_toggle_student_status(student_id):
#     """Activate/Deactivate student"""
#     student = Student.query.get(student_id)
    
#     if not student:
#         return jsonify({'error': 'Student not found'}), 404
    
#     student.is_active = not student.is_active
#     db.session.commit()
    
#     return jsonify({'message': 'Status updated', 'is_active': student.is_active}), 200


# @app.route('/api/admin/jobs', methods=['POST'])
# @jwt_required()
# def admin_create_job():
#     """Create new job posting"""
#     data = request.json
    
#     try:
#         # Parse deadline
#         deadline = None
#         if data.get('deadline'):
#             try:
#                 deadline = datetime.strptime(data['deadline'], '%Y-%m-%d')
#             except:
#                 pass
        
#         job = Job(
#             job_type=data['job_type'],
#             role=data['role'],
#             company=data['company'],
#             description=data['description'],
#             required_skills=json.dumps(data['required_skills']),
#             location=data['location'],
#             package_min=data['package_min'],
#             package_max=data['package_max'],
#             min_cgpa=data.get('min_cgpa', 0),
#             max_backlogs=data.get('max_backlogs', 0),
#             eligible_streams=json.dumps(data.get('eligible_streams', [])),
#             total_positions=data.get('total_positions'),
#             deadline=deadline
#         )
        
#         db.session.add(job)
#         db.session.commit()
        
#         # Send notifications WITHOUT email (to avoid errors)
#         try:
#             eligible_students = Student.query.filter(
#                 Student.is_active == True,
#                 Student.cgpa >= job.min_cgpa
#             ).all()
            
#             for student in eligible_students:
#                 try:
#                     create_notification(
#                         student.id,
#                         "New Job Posted",
#                         f"{job.role} at {job.company} - ₹{job.package_min}-{job.package_max} LPA",
#                         "job_posted"
#                     )
#                 except Exception as notif_error:
#                     print(f"Failed to create notification for student {student.id}: {str(notif_error)}")
#         except Exception as notification_error:
#             print(f"Notification error (non-critical): {str(notification_error)}")
        
#         return jsonify({'message': 'Job created successfully', 'id': job.id}), 201
        
#     except Exception as e:
#         db.session.rollback()
#         print(f"Error creating job: {str(e)}")
#         return jsonify({'error': str(e)}), 500
    
# @app.route('/api/admin/jobs/<int:job_id>', methods=['PUT'])
# @jwt_required()
# def admin_update_job(job_id):
#     """Update job posting"""
#     job = Job.query.get(job_id)
    
#     if not job:
#         return jsonify({'error': 'Job not found'}), 404
    
#     data = request.json
    
#     job.job_type = data.get('job_type', job.job_type)
#     job.role = data.get('role', job.role)
#     job.company = data.get('company', job.company)
#     job.description = data.get('description', job.description)
#     job.required_skills = json.dumps(data['required_skills']) if 'required_skills' in data else job.required_skills
#     job.location = data.get('location', job.location)
#     job.package_min = data.get('package_min', job.package_min)
#     job.package_max = data.get('package_max', job.package_max)
#     job.min_cgpa = data.get('min_cgpa', job.min_cgpa)
#     job.is_active = data.get('is_active', job.is_active)
    
#     db.session.commit()
    
#     return jsonify({'message': 'Job updated successfully'}), 200

# @app.route('/api/admin/jobs/<int:job_id>', methods=['DELETE'])
# @jwt_required()
# def admin_delete_job(job_id):
#     """Delete job posting"""
#     job = Job.query.get(job_id)
    
#     if not job:
#         return jsonify({'error': 'Job not found'}), 404
    
#     db.session.delete(job)
#     db.session.commit()
    
#     return jsonify({'message': 'Job deleted successfully'}), 200

# @app.route('/api/admin/applications', methods=['GET'])
# @jwt_required()
# def admin_get_applications():
#     """Get all job applications"""
#     job_id = request.args.get('job_id', type=int)
#     status = request.args.get('status')
    
#     query = JobApplication.query
    
#     if job_id:
#         query = query.filter_by(job_id=job_id)
    
#     if status:
#         query = query.filter_by(status=status)
    
#     applications = query.order_by(JobApplication.applied_date.desc()).all()
    
#     return jsonify([{
#         'id': app.id,
#         'student_id': app.student.id,
#         'student_name': app.student.name,
#         'student_roll': app.student.roll_number,
#         'student_cgpa': app.student.cgpa,
#         'job_id': app.job.id,
#         'job_role': app.job.role,
#         'company': app.job.company,
#         'ats_score': app.ats_score,
#         'status': app.status,
#         'applied_date': app.applied_date.isoformat(),
#         'interview_date': app.interview_date.isoformat() if app.interview_date else None
#     } for app in applications]), 200

# @app.route('/api/admin/applications/<int:app_id>/update-status', methods=['PUT'])
# @jwt_required()
# def admin_update_application_status(app_id):
#     """Update application status"""
#     application = JobApplication.query.get(app_id)
    
#     if not application:
#         return jsonify({'error': 'Application not found'}), 404
    
#     data = request.json
#     old_status = application.status
#     application.status = data['status']
    
#     if 'interview_date' in data:
#         application.interview_date = datetime.strptime(data['interview_date'], '%Y-%m-%d %H:%M')
    
#     if 'feedback' in data:
#         application.feedback = data['feedback']
    
#     db.session.commit()
    
#     # Send notification to student
#     student = application.student
#     status_messages = {
#         'shortlisted': f"Congratulations! You've been shortlisted for {application.job.role} at {application.job.company}",
#         'selected': f"Congratulations! You've been selected for {application.job.role} at {application.job.company}",
#         'rejected': f"Thank you for applying to {application.job.role} at {application.job.company}. Unfortunately, we're moving forward with other candidates.",
#         'interview_scheduled': f"Interview scheduled for {application.job.role} at {application.job.company}"
#     }
    
#     if student.email and data['status'] in status_messages:
#         send_email_notification(
#             student.email,
#             f"Application Update: {application.job.role}",
#             status_messages[data['status']]
#         )
    
#     create_notification(
#         student.id,
#         "Application Update",
#         status_messages.get(data['status'], f"Your application status has been updated to {data['status']}"),
#         "application_update"
#     )
    
#     # If selected, create placement record
#     if data['status'] == 'selected' and old_status != 'selected':
#         placement = PlacementRecord(
#             student_id=student.id,
#             company=application.job.company,
#             package=(application.job.package_min + application.job.package_max) / 2,
#             placement_year=datetime.now().year
#         )
#         db.session.add(placement)
#         db.session.commit()
    
#     return jsonify({'message': 'Application status updated'}), 200

# @app.route('/api/admin/startup-ideas', methods=['GET'])
# @jwt_required()
# def admin_get_startup_ideas():
#     """Get all startup ideas"""
#     status = request.args.get('status')
    
#     query = StartupIdea.query
#     if status:
#         query = query.filter_by(status=status)
    
#     ideas = query.order_by(StartupIdea.created_at.desc()).all()
    
#     return jsonify([{
#         'id': idea.id,
#         'title': idea.title,
#         'domain': idea.domain,
#         'problem': idea.problem_statement,
#         'solution': idea.solution,
#         'tech': idea.technology,
#         'likes': idea.likes,
#         'status': idea.status,
#         'student_name': idea.student.name,
#         'student_id': idea.student.student_id,
#         'admin_feedback': idea.admin_feedback,
#         'created_at': idea.created_at.isoformat()
#     } for idea in ideas]), 200

# @app.route('/api/admin/startup-ideas/<int:idea_id>/review', methods=['PUT'])
# @jwt_required()
# def admin_review_startup_idea(idea_id):
#     """Review startup idea"""
#     idea = StartupIdea.query.get(idea_id)
    
#     if not idea:
#         return jsonify({'error': 'Idea not found'}), 404
    
#     data = request.json
#     idea.status = data['status']
#     idea.admin_feedback = data.get('feedback')
    
#     db.session.commit()
    
#     # Notify student
#     if idea.student.email:
#         send_email_notification(
#             idea.student.email,
#             f"Startup Idea Review: {idea.title}",
#             f"Your startup idea '{idea.title}' has been {data['status']}.\n\nFeedback: {data.get('feedback', 'No feedback provided')}"
#         )
    
#     create_notification(
#         idea.student.id,
#         "Startup Idea Reviewed",
#         f"Your idea '{idea.title}' has been {data['status']}",
#         "idea_review"
#     )
    
#     return jsonify({'message': 'Idea reviewed successfully'}), 200

# @app.route('/api/admin/analytics/placement-trends', methods=['GET'])
# @jwt_required()
# def admin_placement_trends():
#     """Get placement trends over years"""
#     trends = db.session.query(
#         PlacementRecord.placement_year,
#         db.func.count(PlacementRecord.id).label('count'),
#         db.func.avg(PlacementRecord.package).label('avg_package'),
#         db.func.max(PlacementRecord.package).label('max_package'),
#         db.func.min(PlacementRecord.package).label('min_package')
#     ).group_by(PlacementRecord.placement_year).all()
    
#     return jsonify([{
#         'year': t[0],
#         'placements': t[1],
#         'avg_package': round(t[2], 2) if t[2] else 0,
#         'max_package': t[3],
#         'min_package': t[4]
#     } for t in trends]), 200

# @app.route('/api/admin/analytics/company-wise', methods=['GET'])
# @jwt_required()
# def admin_company_analytics():
#     """Get company-wise placement statistics"""
#     companies = db.session.query(
#         PlacementRecord.company,
#         db.func.count(PlacementRecord.id).label('count'),
#         db.func.avg(PlacementRecord.package).label('avg_package')
#     ).group_by(PlacementRecord.company).all()
    
#     return jsonify([{
#         'company': c[0],
#         'placements': c[1],
#         'avg_package': round(c[2], 2) if c[2] else 0
#     } for c in companies]), 200

# @app.route('/api/admin/analytics/stream-wise', methods=['GET'])
# @jwt_required()
# def admin_stream_analytics():
#     """Get stream-wise placement statistics"""
#     streams = db.session.query(
#         Student.stream,
#         db.func.count(Student.id).label('total_students')
#     ).group_by(Student.stream).all()
    
#     result = []
#     for stream, total in streams:
#         placed = db.session.query(db.func.count(PlacementRecord.id)).join(
#             Student, Student.id == PlacementRecord.student_id
#         ).filter(Student.stream == stream).scalar()
        
#         result.append({
#             'stream': stream,
#             'total_students': total,
#             'placed': placed or 0,
#             'placement_percentage': round((placed / total * 100), 2) if total > 0 else 0
#         })
    
#     return jsonify(result), 200

# @app.route('/api/admin/predict-placements', methods=['POST'])
# @jwt_required()
# def admin_predict_all_placements():
#     """Predict placement probability for all active students"""
#     students = Student.query.filter_by(is_active=True).all()
    
#     # Train or load model
#     model = train_placement_model()
    
#     updated_count = 0
#     for student in students:
#         prediction = predict_placement(student)
#         package_pred = predict_package(student)
        
#         if prediction is not None:
#             student.placement_prediction = round(prediction * 100, 2)
#             student.predicted_package = round(package_pred, 2)
#             updated_count += 1
    
#     db.session.commit()
    
#     return jsonify({
#         'message': f'Predictions updated for {updated_count} students',
#         'total_students': len(students)
#     }), 200

# @app.route('/api/admin/bulk-email', methods=['POST'])
# @jwt_required()
# def admin_bulk_email():
#     """Send bulk email to students"""
#     data = request.json
    
#     # Get target students based on filters
#     query = Student.query.filter_by(is_active=True)
    
#     if data.get('stream'):
#         query = query.filter_by(stream=data['stream'])
    
#     if data.get('min_cgpa'):
#         query = query.filter(Student.cgpa >= data['min_cgpa'])
    
#     students = query.all()
    
#     sent_count = 0
#     for student in students:
#         if student.email:
#             if send_email_notification(student.email, data['subject'], data['body']):
#                 sent_count += 1
            
#             create_notification(
#                 student.id,
#                 data['subject'],
#                 data['body'],
#                 "announcement"
#             )
    
#     return jsonify({
#         'message': f'Email sent to {sent_count} students',
#         'total_recipients': len(students)
#     }), 200

# # ==================== STUDENT API ROUTES (Enhanced) ====================

# @app.route('/api/auth/register', methods=['POST'])
# def register():
#     """Register new student"""
#     data = request.json
    
#     if Student.query.filter_by(student_id=data['student_id']).first():
#         return jsonify({'error': 'Student ID already exists'}), 400
    
#     hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    
#     student = Student(
#         student_id=data['student_id'],
#         password_hash=hashed_password,
#         name=data.get('name'),
#         email=data.get('email')
#     )
    
#     db.session.add(student)
#     db.session.commit()
    
#     # Send welcome email
#     if student.email:
#         send_email_notification(
#             student.email,
#             "Welcome to Sreyas Placement Portal",
#             f"Dear {student.name},\n\nWelcome to the Sreyas Placement Portal! Complete your profile to get better job recommendations.\n\nBest regards,\nPlacement Team"
#         )
    
#     return jsonify({'message': 'Student registered successfully'}), 201

# @app.route('/api/auth/login', methods=['POST'])
# def login():
#     """Student login"""
#     data = request.json
    
#     student = Student.query.filter_by(student_id=data['student_id']).first()
    
#     if student and bcrypt.check_password_hash(student.password_hash, data['password']):
#         if not student.is_active:
#             return jsonify({'error': 'Account is deactivated. Contact admin.'}), 403
        
#         access_token = create_access_token(identity=student.id)
#         return jsonify({
#             'access_token': access_token,
#             'student_id': student.id,
#             'name': student.name,
#             'student_id_number': student.student_id
#         }), 200
    
#     return jsonify({'error': 'Invalid credentials'}), 401

# @app.route('/api/student/profile', methods=['GET'])
# @jwt_required()
# def get_profile():
#     """Get student profile"""
#     student_id = get_jwt_identity()
#     student = Student.query.get(student_id)
    
#     if not student:
#         return jsonify({'error': 'Student not found'}), 404
    
#     return jsonify({
#         'id': student.id,
#         'student_id': student.student_id,
#         'name': student.name,
#         'roll_number': student.roll_number,
#         'stream': student.stream,
#         'dob': student.dob.isoformat() if student.dob else None,
#         'gender': student.gender,
#         'phone': student.phone,
#         'email': student.email,
#         'cgpa': student.cgpa,
#         'tenth_percentage': student.tenth_percentage,
#         'twelfth_percentage': student.twelfth_percentage,
#         'backlogs': student.backlogs,
#         'profile_pic': student.profile_pic_path,
#         'resume': student.resume_path,
#         'placement_prediction': student.placement_prediction,
#         'predicted_package': student.predicted_package,
#         'skills': [{'id': s.id, 'name': s.skill_name, 'proficiency': s.proficiency} for s in student.skills],
#         'certifications': [{'id': c.id, 'name': c.name, 'issuer': c.issuer, 'date': c.date_obtained.isoformat() if c.date_obtained else None} for c in student.certifications],
#         'internships': [{'id': i.id, 'company': i.company, 'role': i.role, 'duration': i.duration, 'description': i.description} for i in student.internships],
#         'projects': [{'id': p.id, 'name': p.name, 'tech': p.tech_stack, 'description': p.description, 'github': p.github_url} for p in student.projects]
#     }), 200

# @app.route('/api/student/profile', methods=['PUT'])
# @jwt_required()
# def update_profile():
#     """Update student profile"""
#     student_id = get_jwt_identity()
#     student = Student.query.get(student_id)
#     data = request.json
    
#     student.name = data.get('name', student.name)
#     student.roll_number = data.get('roll_number', student.roll_number)
#     student.stream = data.get('stream', student.stream)
#     student.gender = data.get('gender', student.gender)
#     student.phone = data.get('phone', student.phone)
#     student.email = data.get('email', student.email)
#     student.cgpa = data.get('cgpa', student.cgpa)
#     student.tenth_percentage = data.get('tenth_percentage', student.tenth_percentage)
#     student.twelfth_percentage = data.get('twelfth_percentage', student.twelfth_percentage)
#     student.backlogs = data.get('backlogs', student.backlogs)
    
#     if data.get('dob'):
#         student.dob = datetime.strptime(data['dob'], '%Y-%m-%d').date()
    
#     db.session.commit()
    
#     # Update predictions after profile update
#     prediction = predict_placement(student)
#     package_pred = predict_package(student)
    
#     if prediction is not None:
#         student.placement_prediction = round(prediction * 100, 2)
#         student.predicted_package = round(package_pred, 2)
#         db.session.commit()
    
#     return jsonify({'message': 'Profile updated successfully'}), 200

# @app.route('/api/student/notifications', methods=['GET'])
# @jwt_required()
# def get_notifications():
#     """Get student notifications"""
#     student_id = get_jwt_identity()
    
#     notifications = Notification.query.filter_by(
#         student_id=student_id
#     ).order_by(Notification.created_at.desc()).limit(50).all()
    
#     return jsonify([{
#         'id': n.id,
#         'title': n.title,
#         'message': n.message,
#         'type': n.notification_type,
#         'is_read': n.is_read,
#         'created_at': n.created_at.isoformat()
#     } for n in notifications]), 200

# @app.route('/api/student/notifications/<int:notif_id>/mark-read', methods=['PUT'])
# @jwt_required()
# def mark_notification_read(notif_id):
#     """Mark notification as read"""
#     notification = Notification.query.get(notif_id)
    
#     if notification and notification.student_id == get_jwt_identity():
#         notification.is_read = True
#         db.session.commit()
#         return jsonify({'message': 'Notification marked as read'}), 200
    
#     return jsonify({'error': 'Notification not found'}), 404

# @app.route('/api/student/predict-placement', methods=['GET'])
# @jwt_required()
# def get_placement_prediction():
#     """Get placement prediction for current student"""
#     student_id = get_jwt_identity()
#     student = Student.query.get(student_id)
    
#     prediction = predict_placement(student)
#     package_pred = predict_package(student)
    
#     if prediction is not None:
#         student.placement_prediction = round(prediction * 100, 2)
#         student.predicted_package = round(package_pred, 2)
#         db.session.commit()
        
#         # Provide recommendations
#         recommendations = []
        
#         if student.cgpa < 7.0:
#             recommendations.append("Focus on improving CGPA")
        
#         if len(student.skills) < 5:
#             recommendations.append("Add more technical skills")
        
#         if len(student.internships) == 0:
#             recommendations.append("Complete at least one internship")
        
#         if len(student.projects) < 2:
#             recommendations.append("Build more projects to showcase your skills")
        
#         if student.backlogs > 0:
#             recommendations.append("Clear your backlogs")
        
#         return jsonify({
#             'placement_probability': student.placement_prediction,
#             'predicted_package': student.predicted_package,
#             'recommendations': recommendations
#         }), 200
    
#     return jsonify({'error': 'Unable to generate prediction'}), 400

# # Continue with remaining student routes (skills, certifications, etc. - same as before)
# @app.route('/api/student/upload/resume', methods=['POST'])
# @jwt_required()
# def upload_resume():
#     """Upload student resume"""
#     student_id = get_jwt_identity()
#     student = Student.query.get(student_id)
    
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file provided'}), 400
    
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No file selected'}), 400
    
#     if file:
#         filename = secure_filename(f"{student.student_id}_{file.filename}")
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'resumes', filename)
#         file.save(filepath)
        
#         student.resume_path = filepath
#         db.session.commit()
        
#         return jsonify({
#             'message': 'Resume uploaded successfully',
#             'filename': filename,
#             'path': filepath
#         }), 200

# @app.route('/api/student/upload/profile-pic', methods=['POST'])
# @jwt_required()
# def upload_profile_pic():
#     """Upload profile picture"""
#     student_id = get_jwt_identity()
#     student = Student.query.get(student_id)
    
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file provided'}), 400
    
#     file = request.files['file']
#     if file:
#         filename = secure_filename(f"profile_{student.student_id}_{file.filename}")
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'profile_pics', filename)
#         file.save(filepath)
        
#         student.profile_pic_path = filepath
#         db.session.commit()
        
#         return jsonify({
#             'message': 'Profile picture uploaded successfully',
#             'path': filepath
#         }), 200

# @app.route('/api/student/skills', methods=['POST'])
# @jwt_required()
# def add_skill():
#     """Add skill"""
#     student_id = get_jwt_identity()
#     data = request.json
    
#     skill = Skill(
#         student_id=student_id,
#         skill_name=data['skill_name'],
#         proficiency=data.get('proficiency', 'Intermediate')
#     )
    
#     db.session.add(skill)
#     db.session.commit()
    
#     return jsonify({'message': 'Skill added', 'id': skill.id}), 201

# @app.route('/api/student/skills/<int:skill_id>', methods=['DELETE'])
# @jwt_required()
# def delete_skill(skill_id):
#     """Delete skill"""
#     skill = Skill.query.get(skill_id)
#     if skill and skill.student_id == get_jwt_identity():
#         db.session.delete(skill)
#         db.session.commit()
#         return jsonify({'message': 'Skill deleted'}), 200
#     return jsonify({'error': 'Skill not found'}), 404

# @app.route('/api/student/certifications', methods=['POST'])
# @jwt_required()
# def add_certification():
#     """Add certification"""
#     student_id = get_jwt_identity()
#     data = request.json
    
#     cert = Certification(
#         student_id=student_id,
#         name=data['name'],
#         issuer=data['issuer'],
#         date_obtained=datetime.strptime(data['date'], '%Y-%m-%d').date() if data.get('date') else None
#     )
    
#     db.session.add(cert)
#     db.session.commit()
    
#     return jsonify({'message': 'Certification added', 'id': cert.id}), 201

# @app.route('/api/student/certifications/<int:cert_id>', methods=['DELETE'])
# @jwt_required()
# def delete_certification(cert_id):
#     """Delete certification"""
#     cert = Certification.query.get(cert_id)
#     if cert and cert.student_id == get_jwt_identity():
#         db.session.delete(cert)
#         db.session.commit()
#         return jsonify({'message': 'Certification deleted'}), 200
#     return jsonify({'error': 'Certification not found'}), 404

# @app.route('/api/student/internships', methods=['POST'])
# @jwt_required()
# def add_internship():
#     """Add internship"""
#     student_id = get_jwt_identity()
#     data = request.json
    
#     internship = Internship(
#         student_id=student_id,
#         company=data['company'],
#         role=data['role'],
#         duration=data['duration'],
#         description=data.get('description')
#     )
    
#     db.session.add(internship)
#     db.session.commit()
    
#     return jsonify({'message': 'Internship added', 'id': internship.id}), 201

# @app.route('/api/student/internships/<int:internship_id>', methods=['DELETE'])
# @jwt_required()
# def delete_internship(internship_id):
#     """Delete internship"""
#     internship = Internship.query.get(internship_id)
#     if internship and internship.student_id == get_jwt_identity():
#         db.session.delete(internship)
#         db.session.commit()
#         return jsonify({'message': 'Internship deleted'}), 200
#     return jsonify({'error': 'Internship not found'}), 404

# @app.route('/api/student/projects', methods=['POST'])
# @jwt_required()
# def add_project():
#     """Add project"""
#     student_id = get_jwt_identity()
#     data = request.json
    
#     project = Project(
#         student_id=student_id,
#         name=data['name'],
#         tech_stack=data['tech'],
#         description=data.get('description'),
#         github_url=data.get('github')
#     )
    
#     db.session.add(project)
#     db.session.commit()
    
#     return jsonify({'message': 'Project added', 'id': project.id}), 201

# @app.route('/api/student/projects/<int:project_id>', methods=['DELETE'])
# @jwt_required()
# def delete_project(project_id):
#     """Delete project"""
#     project = Project.query.get(project_id)
#     if project and project.student_id == get_jwt_identity():
#         db.session.delete(project)
#         db.session.commit()
#         return jsonify({'message': 'Project deleted'}), 200
#     return jsonify({'error': 'Project not found'}), 404

# @app.route('/api/jobs', methods=['GET'])
# @jwt_required()
# def get_jobs():
#     """Get all active jobs"""
#     job_type = request.args.get('type', 'all')
    
#     query = Job.query.filter_by(is_active=True)
#     if job_type != 'all':
#         query = query.filter_by(job_type=job_type)
    
#     jobs = query.all()
    
#     return jsonify([{
#         'id': job.id,
#         'type': job.job_type,
#         'role': job.role,
#         'company': job.company,
#         'description': job.description,
#         'skills': json.loads(job.required_skills) if job.required_skills else [],
#         'location': job.location,
#         'package': f"₹{job.package_min}-{job.package_max} LPA",
#         'package_min': job.package_min,  # ADD THIS
#         'package_max': job.package_max,  # ADD THIS
#         'min_cgpa': job.min_cgpa,
#         'applications_count': len(job.applications),  # ADD THIS
#         'deadline': job.deadline.isoformat() if job.deadline else None
#     } for job in jobs]), 200

# @app.route('/api/jobs/<int:job_id>/apply', methods=['POST'])
# @jwt_required()
# def apply_job(job_id):
#     """Apply for a job"""
#     student_id = get_jwt_identity()
#     student = Student.query.get(student_id)
#     job = Job.query.get(job_id)
    
#     if not job:
#         return jsonify({'error': 'Job not found'}), 404
    
#     existing = JobApplication.query.filter_by(student_id=student_id, job_id=job_id).first()
#     if existing:
#         return jsonify({'error': 'Already applied'}), 400
    
#     if job.min_cgpa and student.cgpa < job.min_cgpa:
#         return jsonify({'error': 'CGPA requirement not met'}), 400
    
#     application = JobApplication(
#         student_id=student_id,
#         job_id=job_id
#     )
    
#     db.session.add(application)
#     db.session.commit()
    
#     return jsonify({'message': 'Application submitted successfully', 'id': application.id}), 201

# @app.route('/api/jobs/<int:job_id>/ats-check', methods=['POST'])
# @jwt_required()
# def ats_check(job_id):
#     """Check ATS score for job application"""
#     student_id = get_jwt_identity()
#     job = Job.query.get(job_id)
    
#     if not job:
#         return jsonify({'error': 'Job not found'}), 404
    
#     if 'file' not in request.files:
#         return jsonify({'error': 'No resume provided'}), 400
    
#     file = request.files['file']
#     if file:
#         filename = secure_filename(f"temp_{student_id}_{file.filename}")
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'resumes', filename)
#         file.save(filepath)
        
#         resume_text = extract_text_from_pdf(filepath)
#         ats_result = calculate_ats_score(resume_text, job.required_skills)
        
#         return jsonify(ats_result), 200

# @app.route('/api/startup-ideas', methods=['GET'])
# @jwt_required()
# def get_startup_ideas():
#     """Get all startup ideas"""
#     ideas = StartupIdea.query.filter_by(status='approved').order_by(StartupIdea.created_at.desc()).all()
#     student_id = get_jwt_identity()
    
#     return jsonify([{
#         'id': idea.id,
#         'title': idea.title,
#         'domain': idea.domain,
#         'problem': idea.problem_statement,
#         'solution': idea.solution,
#         'tech': idea.technology,
#         'likes': idea.likes,
#         'liked': any(like.student_id == student_id for like in idea.liked_by),
#         'author': idea.student.name,
#         'created_at': idea.created_at.isoformat()
#     } for idea in ideas]), 200

# @app.route('/api/startup-ideas', methods=['POST'])
# @jwt_required()
# def create_startup_idea():
#     """Submit startup idea"""
#     student_id = get_jwt_identity()
#     data = request.json
    
#     idea = StartupIdea(
#         student_id=student_id,
#         title=data['title'],
#         domain=data['domain'],
#         problem_statement=data['problem'],
#         solution=data['solution'],
#         technology=data['tech']
#     )
    
#     db.session.add(idea)
#     db.session.commit()
    
#     return jsonify({'message': 'Idea submitted successfully', 'id': idea.id}), 201

# @app.route('/api/startup-ideas/<int:idea_id>/like', methods=['POST'])
# @jwt_required()
# def like_idea(idea_id):
#     """Like/unlike startup idea"""
#     student_id = get_jwt_identity()
#     idea = StartupIdea.query.get(idea_id)
    
#     if not idea:
#         return jsonify({'error': 'Idea not found'}), 404
    
#     existing_like = IdeaLike.query.filter_by(student_id=student_id, idea_id=idea_id).first()
    
#     if existing_like:
#         db.session.delete(existing_like)
#         idea.likes -= 1
#     else:
#         like = IdeaLike(student_id=student_id, idea_id=idea_id)
#         db.session.add(like)
#         idea.likes += 1
    
#     db.session.commit()
    
#     return jsonify({'likes': idea.likes}), 200

# @app.route('/api/analytics/placement-stats', methods=['GET'])
# def get_placement_stats():
#     """Get placement statistics"""
#     total_students = Student.query.count()
#     placed_students = PlacementRecord.query.count()
    
#     return jsonify({
#         'total_students': total_students,
#         'placed': placed_students,
#         'not_placed': total_students - placed_students,
#         'placement_percentage': round((placed_students / total_students * 100), 2) if total_students > 0 else 0
#     }), 200

# # ==================== SEED INITIAL DATA ====================

# @app.route('/api/seed-data', methods=['POST'])
# def seed_data():
#     """Seed initial job data and create default admin"""
#     # Create default admin
#     if not Admin.query.filter_by(username='admin').first():
#         admin = Admin(
#             username='admin',
#             password_hash=bcrypt.generate_password_hash('admin123').decode('utf-8'),
#             email='admin@sreyas.edu',
#             role='super_admin'
#         )
#         db.session.add(admin)
    
#     # Seed job data
#     jobs_data = [
#         {
#             'job_type': 'mnc',
#             'role': 'Software Developer',
#             'company': 'Google',
#             'description': 'Develop and maintain large-scale applications',
#             'required_skills': json.dumps(['Java', 'Python', 'Cloud Computing', 'Problem Solving']),
#             'location': 'Bangalore, Hyderabad',
#             'package_min': 25,
#             'package_max': 30,
#             'min_cgpa': 7.5,
#             'max_backlogs': 0,
#             'eligible_streams': json.dumps(['CSE', 'CSE-AIML', 'CSE-DS']),
#             'total_positions': 10
#         },
#         {
#             'job_type': 'mnc',
#             'role': 'Data Analyst',
#             'company': 'Microsoft',
#             'description': 'Analyze data and provide insights',
#             'required_skills': json.dumps(['SQL', 'Python', 'Data Visualization', 'Statistics']),
#             'location': 'Bangalore',
#             'package_min': 18,
#             'package_max': 22,
#             'min_cgpa': 7.0,
#             'max_backlogs': 1,
#             'eligible_streams': json.dumps(['CSE', 'CSE-AIML', 'CSE-DS', 'ECE']),
#             'total_positions': 8
#         },
#         {
#             'job_type': 'startup',
#             'role': 'Full Stack Developer',
#             'company': 'TechStartup Inc',
#             'description': 'Build innovative web applications',
#             'required_skills': json.dumps(['React', 'Node.js', 'MongoDB', 'JavaScript']),
#             'location': 'Remote',
#             'package_min': 8,
#             'package_max': 12,
#             'min_cgpa': 6.5,
#             'max_backlogs': 2,
#             'eligible_streams': json.dumps(['CSE', 'CSE-AIML', 'CSE-DS']),
#             'total_positions': 5
#         },
#         {
#             'job_type': 'startup',
#             'role': 'Frontend Developer',
#             'company': 'InnovateLabs',
#             'description': 'Create responsive user interfaces',
#             'required_skills': json.dumps(['HTML', 'CSS', 'JavaScript', 'React']),
#             'location': 'Pune',
#             'package_min': 6,
#             'package_max': 10,
#             'min_cgpa': 6.0,
#             'max_backlogs': 2,
#             'eligible_streams': json.dumps(['CSE', 'CSE-AIML', 'CSE-DS']),
#             'total_positions': 6
#         },
#         {
#             'job_type': 'mnc',
#             'role': 'Cloud Engineer',
#             'company': 'Amazon',
#             'description': 'Design and manage cloud infrastructure',
#             'required_skills': json.dumps(['AWS', 'Docker', 'Kubernetes', 'Linux']),
#             'location': 'Chennai, Bangalore',
#             'package_min': 20,
#             'package_max': 25,
#             'min_cgpa': 7.5,
#             'max_backlogs': 0,
#             'eligible_streams': json.dumps(['CSE', 'CSE-AIML', 'ECE']),
#             'total_positions': 7
#         }
#     ]
    
#     for job_data in jobs_data:
#         if not Job.query.filter_by(role=job_data['role'], company=job_data['company']).first():
#             job = Job(**job_data)
#             db.session.add(job)
    
#     db.session.commit()
    
#     return jsonify({'message': 'Database seeded successfully'}), 201

# # ==================== INITIALIZE DATABASE ====================

# with app.app_context():
#     db.create_all()
#     print("Database tables created successfully!")

# # ==================== RUN APPLICATION ====================

# if __name__ == '__main__':

#     app.run(debug=True, host='0.0.0.0', port=5000)

import os
from datetime import datetime, timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_mail import Mail
import pymysql


# ---------------- MySQL setup ----------------
pymysql.install_as_MySQLdb()

app = Flask(__name__)

# ---------------- DATABASE -------------------
# URL-encode any special characters in password
MYSQL_USER = "root"
MYSQL_PASSWORD = "Karthik30%4005"  # '@' replaced by %40
MYSQL_HOST = "localhost"
MYSQL_DB = "placement_portal"

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:3306/{MYSQL_DB}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ---------------- OTHER CONFIG ----------------
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'sreyas-placement-portal-secret-2024')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'sreyas-jwt-secret-2024')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# ---------------- EXTENSIONS -----------------
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
mail = Mail(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# ---------------- CREATE FOLDERS ----------------
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'resumes'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'profile_pics'), exist_ok=True)
os.makedirs('models', exist_ok=True)


# ==================== DATABASE MODELS ====================

class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default='admin')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100))
    roll_number = db.Column(db.String(50))
    stream = db.Column(db.String(50))
    dob = db.Column(db.Date)
    gender = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    cgpa = db.Column(db.Float)
    backlogs = db.Column(db.Integer, default=0)
    resume_path = db.Column(db.String(200))
    profile_pic_path = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    placement_prediction = db.Column(db.Float)
    predicted_package = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    skills = db.relationship('Skill', backref='student', lazy=True, cascade='all, delete-orphan')
    certifications = db.relationship('Certification', backref='student', lazy=True, cascade='all, delete-orphan')
    internships = db.relationship('Internship', backref='student', lazy=True, cascade='all, delete-orphan')
    projects = db.relationship('Project', backref='student', lazy=True, cascade='all, delete-orphan')
    applications = db.relationship('JobApplication', backref='student', lazy=True, cascade='all, delete-orphan')
    startup_ideas = db.relationship('StartupIdea', backref='student', lazy=True, cascade='all, delete-orphan')
    notifications = db.relationship('Notification', backref='student', lazy=True, cascade='all, delete-orphan')

class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    job_type = db.Column(db.String(50))
    role = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    required_skills = db.Column(db.Text)
    location = db.Column(db.String(200))
    package_min = db.Column(db.Float)
    package_max = db.Column(db.Float)
    min_cgpa = db.Column(db.Float)
    max_backlogs = db.Column(db.Integer, default=0)
    eligible_streams = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    posted_date = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime)
    total_positions = db.Column(db.Integer)
    
    applications = db.relationship('JobApplication', backref='job', lazy=True, cascade='all, delete-orphan')

class JobApplication(db.Model):
    __tablename__ = 'job_applications'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    resume_path = db.Column(db.String(200))
    ats_score = db.Column(db.Integer)
    status = db.Column(db.String(50), default='applied')
    applied_date = db.Column(db.DateTime, default=datetime.utcnow)
    interview_date = db.Column(db.DateTime)
    feedback = db.Column(db.Text)

class Skill(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    skill_name = db.Column(db.String(100), nullable=False)
    proficiency = db.Column(db.String(50))

class Certification(db.Model):
    __tablename__ = 'certifications'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    issuer = db.Column(db.String(200))
    date_obtained = db.Column(db.Date)

class Internship(db.Model):
    __tablename__ = 'internships'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(200))
    duration = db.Column(db.String(100))
    description = db.Column(db.Text)

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    tech_stack = db.Column(db.String(500))
    description = db.Column(db.Text)
    github_url = db.Column(db.String(200))

class StartupIdea(db.Model):
    __tablename__ = 'startup_ideas'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    domain = db.Column(db.String(100))
    problem_statement = db.Column(db.Text)
    solution = db.Column(db.Text)
    technology = db.Column(db.String(500))
    likes = db.Column(db.Integer, default=0)
    status = db.Column(db.String(50), default='pending')
    admin_feedback = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    liked_by = db.relationship('IdeaLike', backref='idea', lazy=True, cascade='all, delete-orphan')

class IdeaLike(db.Model):
    __tablename__ = 'idea_likes'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    idea_id = db.Column(db.Integer, db.ForeignKey('startup_ideas.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text)
    notification_type = db.Column(db.String(50))
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PlacementRecord(db.Model):
    __tablename__ = 'placement_records'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    company = db.Column(db.String(200))
    package = db.Column(db.Float)
    placement_year = db.Column(db.Integer)
    placement_date = db.Column(db.DateTime, default=datetime.utcnow)

# ==================== HELPERS ====================

def create_notification(student_id, title, message, notification_type):
    try:
        notification = Notification(
            student_id=student_id,
            title=str(title),
            message=str(message),
            notification_type=str(notification_type)
        )
        db.session.add(notification)
        db.session.commit()
    except Exception as e:
        print(f"Notification error: {e}")
        db.session.rollback()

def notify_eligible_students(job):
    try:
        students = Student.query.filter_by(is_active=True).all()
        for student in students:
            create_notification(
                student.id,
                f"New Job: {job.role}",
                f"{job.company} is hiring! Check Current Hirings.",
                "job_posted"
            )
    except:
        pass

# ==================== AUTH ROUTES ====================

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    print(f"Admin login: {data.get('username')}")
    
    admin = Admin.query.filter_by(username=data.get('username')).first()
    
    if admin and bcrypt.check_password_hash(admin.password_hash, data.get('password')):
        # String Identity for Admin to avoid conflict
        access_token = create_access_token(identity=f"admin_{admin.id}")
        return jsonify({
            'access_token': access_token,
            'role': 'admin',
            'username': admin.username
        }), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    print(f"Registering: {data}")
    
    if Student.query.filter_by(student_id=data['student_id']).first():
        return jsonify({'error': 'Student ID already exists'}), 400
    
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    
    student = Student(
        student_id=data['student_id'],
        password_hash=hashed_password,
        name=data.get('name'),
        email=data.get('email')
    )
    
    db.session.add(student)
    db.session.commit()
    
    return jsonify({'message': 'Student registered successfully'}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    print(f"Student login: {data.get('student_id')}")
    
    student = Student.query.filter_by(student_id=data.get('student_id')).first()
    
    if student and bcrypt.check_password_hash(student.password_hash, data.get('password')):
        if not student.is_active:
            return jsonify({'error': 'Account deactivated'}), 403
        
        # ✅ FIX: Convert ID to String to prevent 422 Errors
        access_token = create_access_token(identity=str(student.id))
        
        return jsonify({
            'access_token': access_token,
            'student_id': student.id,
            'name': student.name,
            'student_id_number': student.student_id
        }), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401

# ==================== ADMIN JOB MANAGEMENT ====================

@app.route('/api/admin/jobs', methods=['GET'])
@jwt_required()
def admin_get_jobs():
    jobs = Job.query.order_by(Job.posted_date.desc()).all()
    result = []
    
    for job in jobs:
        try:
            skills = json.loads(job.required_skills) if job.required_skills else []
        except:
            skills = []
        
        try:
            streams = json.loads(job.eligible_streams) if job.eligible_streams else []
        except:
            streams = []
            
        result.append({
            'id': job.id,
            'job_type': job.job_type,
            'type': job.job_type,
            'role': job.role,
            'company': job.company,
            'description': job.description,
            'required_skills': skills,
            'skills': skills,
            'location': job.location,
            'package_min': job.package_min,
            'package_max': job.package_max,
            'package': f"₹{job.package_min}-{job.package_max} LPA",
            'min_cgpa': job.min_cgpa,
            'eligible_streams': streams,
            'applications_count': len(job.applications)
        })
    
    return jsonify(result), 200

@app.route('/api/admin/jobs', methods=['POST'])
@jwt_required()
def admin_create_job():
    data = request.json
    print(f"Creating job: {data}")
    
    try:
        def parse_list(val):
            if isinstance(val, list): return val
            if isinstance(val, str): return [s.strip() for s in val.split(',') if s.strip()]
            return []

        required_skills = parse_list(data.get('required_skills'))
        eligible_streams = parse_list(data.get('eligible_streams'))
        
        def safe_float(val):
            try: return float(val)
            except: return 0.0

        job = Job(
            job_type=data.get('job_type', 'mnc'),
            role=data.get('role', 'Software Developer'),
            company=data.get('company', 'Unknown'),
            description=data.get('description', ''),
            required_skills=json.dumps(required_skills),
            location=data.get('location', ''),
            package_min=safe_float(data.get('package_min')),
            package_max=safe_float(data.get('package_max')),
            min_cgpa=safe_float(data.get('min_cgpa')),
            max_backlogs=int(data.get('max_backlogs', 0)),
            eligible_streams=json.dumps(eligible_streams),
            total_positions=int(data.get('total_positions', 1)),
            is_active=True,
            posted_date=datetime.utcnow()
        )
        
        db.session.add(job)
        db.session.commit()
        
        notify_eligible_students(job)
        
        return jsonify({'message': 'Job created successfully', 'id': job.id}), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating job: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/jobs/<int:job_id>', methods=['DELETE'])
@jwt_required()
def admin_delete_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    db.session.delete(job)
    db.session.commit()
    return jsonify({'message': 'Job deleted'}), 200

# ==================== APPLICATION LOGIC (THE CRITICAL PART) ====================

@app.route('/api/jobs/<int:job_id>/apply', methods=['POST'])
@jwt_required()
def apply_job(job_id):
    identity = get_jwt_identity()
    print(f"⚡ Applying for job... Raw Identity: {identity}")
    
    if identity and isinstance(identity, str) and identity.startswith('admin_'):
        return jsonify({'error': 'Admins cannot apply for jobs'}), 403
        
    # ✅ FIX: Convert String identity back to Integer
    try:
        student_id = int(identity)
    except:
        return jsonify({'error': 'Invalid student token'}), 422

    job = Job.query.get(job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    existing = JobApplication.query.filter_by(student_id=student_id, job_id=job_id).first()
    if existing:
        return jsonify({'error': 'You have already applied for this job'}), 400
    
    application = JobApplication(
        student_id=student_id,
        job_id=job_id,
        status='applied',
        applied_date=datetime.utcnow(),
        ats_score=0
    )
    
    db.session.add(application)
    db.session.commit()
    
    print(f"✅ Application saved! App ID: {application.id}")
    
    return jsonify({'message': 'Application submitted successfully', 'id': application.id}), 201

@app.route('/api/admin/applications', methods=['GET'])
@jwt_required()
def admin_get_applications():
    job_id = request.args.get('job_id', type=int)
    print(f"Fetching applications for Job ID: {job_id}")
    
    query = JobApplication.query
    if job_id:
        query = query.filter_by(job_id=job_id)
    
    applications = query.order_by(JobApplication.applied_date.desc()).all()
    print(f"Found {len(applications)} applications")
    
    result = []
    for app in applications:
        # Check if student relation exists to avoid errors if student was deleted
        if app.student:
            result.append({
                'id': app.id,
                'student_id': app.student.id,
                'student_name': app.student.name,
                'student_roll': app.student.roll_number,
                'student_cgpa': app.student.cgpa,
                'job_id': app.job.id,
                'job_role': app.job.role,
                'company': app.job.company,
                'ats_score': app.ats_score,
                'status': app.status,
                'applied_date': app.applied_date.isoformat()
            })
        else:
            print(f"⚠️ Warning: Application {app.id} has no linked student.")
            
    return jsonify(result), 200

@app.route('/api/admin/applications/<int:app_id>/update-status', methods=['PUT'])
@jwt_required()
def update_application_status(app_id):
    application = JobApplication.query.get(app_id)
    if not application:
        return jsonify({'error': 'Application not found'}), 404
    
    data = request.json
    application.status = data.get('status', application.status)
    db.session.commit()
    
    try:
        create_notification(
            application.student_id,
            "Application Status Update",
            f"Your application for {application.job.role} is now {application.status}",
            "application_update"
        )
    except:
        pass
    
    return jsonify({'message': 'Status updated'}), 200

# ==================== STUDENT ROUTES ====================

@app.route('/api/jobs', methods=['GET'])
@jwt_required()
def get_jobs():
    job_type = request.args.get('type', 'all')
    query = Job.query.filter_by(is_active=True)
    if job_type != 'all':
        query = query.filter_by(job_type=job_type)
    
    jobs = query.all()
    result = []
    
    for job in jobs:
        try:
            skills = json.loads(job.required_skills) if job.required_skills else []
        except:
            skills = []
            
        result.append({
            'id': job.id,
            'type': job.job_type,
            'role': job.role,
            'company': job.company,
            'description': job.description,
            'skills': skills,
            'location': job.location,
            'package': f"₹{job.package_min}-{job.package_max} LPA",
            'package_min': job.package_min,
            'package_max': job.package_max,
            'min_cgpa': job.min_cgpa,
            'applications_count': len(job.applications)
        })
    
    return jsonify(result), 200

@app.route('/api/student/profile', methods=['GET'])
@jwt_required()
def get_profile():
    identity = get_jwt_identity()
    
    # Check if this is an admin token
    if identity and isinstance(identity, str) and identity.startswith('admin_'):
         return jsonify({'error': 'Admin cannot access student profile'}), 403
    
    # ✅ FIX: Convert String identity back to Integer for DB query
    try:
        student_id = int(identity)
    except:
        return jsonify({'error': 'Invalid token identity'}), 422

    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
        
    return jsonify({
        'id': student.id,
        'name': student.name,
        'roll_number': student.roll_number,
        'stream': student.stream,
        'cgpa': student.cgpa,
        'email': student.email,
        'phone': student.phone,
        'skills': [{'id': s.id, 'name': s.skill_name} for s in student.skills],
        'projects': [{'id': p.id, 'name': p.name} for p in student.projects],
        'internships': [{'id': i.id, 'role': i.role} for i in student.internships],
        'certifications': [{'id': c.id, 'name': c.name} for c in student.certifications]
    }), 200

@app.route('/api/student/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    student_id = get_jwt_identity()
    student = Student.query.get(student_id)
    data = request.json
    
    student.name = data.get('name', student.name)
    student.roll_number = data.get('roll_number', student.roll_number)
    student.stream = data.get('stream', student.stream)
    student.cgpa = data.get('cgpa', student.cgpa)
    student.email = data.get('email', student.email)
    
    db.session.commit()
    return jsonify({'message': 'Profile updated'}), 200

# ==================== SEED DATA ====================

@app.route('/api/seed-data', methods=['POST'])
def seed_data():
    print("Seeding database...")
    
    # Create Admin
    if not Admin.query.filter_by(username='admin').first():
        admin = Admin(
            username='admin',
            password_hash=bcrypt.generate_password_hash('admin123').decode('utf-8')
        )
        db.session.add(admin)
        print("✅ Admin created: admin / admin123")
    
    # Create Student (Simple ID)
    if not Student.query.filter_by(student_id='student').first():
        student = Student(
            student_id='student',
            password_hash=bcrypt.generate_password_hash('student123').decode('utf-8'),
            name='Test Student',
            roll_number='21A91A0501',
            stream='CSE',
            cgpa=8.5,
            email='student@sreyas.edu'
        )
        db.session.add(student)
        print("✅ Student created: student / student123")

    db.session.commit()
    return jsonify({'message': 'Database seeded successfully'}), 201

# ==================== RUN ====================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✅ Database tables created")
    
    print("🚀 Server running on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
