// API Configuration
const API_CONFIG = {
    // Backend URL - change this if deploying
    BASE_URL: 'http://localhost:5000',
    
    // API Endpoints
    ENDPOINTS: {
        // Authentication
        STUDENT_LOGIN: '/api/auth/login',
        STUDENT_REGISTER: '/api/auth/register',
        ADMIN_LOGIN: '/api/admin/login',
        
        // Student Profile
        STUDENT_PROFILE: '/api/student/profile',
        UPLOAD_RESUME: '/api/student/upload/resume',
        UPLOAD_PROFILE_PIC: '/api/student/upload/profile-pic',
        
        // Skills
        SKILLS: '/api/student/skills',
        DELETE_SKILL: (id) => `/api/student/skills/${id}`,
        
        // Certifications
        CERTIFICATIONS: '/api/student/certifications',
        DELETE_CERTIFICATION: (id) => `/api/student/certifications/${id}`,
        
        // Internships
        INTERNSHIPS: '/api/student/internships',
        DELETE_INTERNSHIP: (id) => `/api/student/internships/${id}`,
        
        // Projects
        PROJECTS: '/api/student/projects',
        DELETE_PROJECT: (id) => `/api/student/projects/${id}`,
        
        // Jobs
        JOBS: '/api/jobs',
        JOB_APPLY: (id) => `/api/jobs/${id}/apply`,
        JOB_ATS_CHECK: (id) => `/api/jobs/${id}/ats-check`,
        
        // Startup Ideas
        STARTUP_IDEAS: '/api/startup-ideas',
        LIKE_IDEA: (id) => `/api/startup-ideas/${id}/like`,
        
        // Analytics
        PLACEMENT_STATS: '/api/analytics/placement-stats'
    }
};

// Helper function to get full URL
const getApiUrl = (endpoint) => {
    return `${API_CONFIG.BASE_URL}${endpoint}`;
};