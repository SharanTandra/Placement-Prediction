// API Helper Functions

const apiCall = async (endpoint, options = {}) => {
    try {
        const url = getApiUrl(endpoint);
        const response = await fetch(url, options);

        if (response.status === 401) {
            logout();
            throw new Error('Session expired. Please login again.');
        }

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'API call failed');
        }

        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
};

// Profile APIs
const fetchStudentProfile = async () => {
    return await apiCall(API_CONFIG.ENDPOINTS.STUDENT_PROFILE, {
        method: 'GET',
        headers: getAuthHeaders()
    });
};

const updateStudentProfile = async (profileData) => {
    return await apiCall(API_CONFIG.ENDPOINTS.STUDENT_PROFILE, {
        method: 'PUT',
        headers: getAuthHeaders(),
        body: JSON.stringify(profileData)
    });
};

// Jobs APIs
const fetchJobs = async (type = 'all') => {
    const endpoint = `${API_CONFIG.ENDPOINTS.JOBS}?type=${type}`;
    return await apiCall(endpoint, {
        method: 'GET',
        headers: getAuthHeaders()
    });
};

const applyForJob = async (jobId) => {
    return await apiCall(API_CONFIG.ENDPOINTS.JOB_APPLY(jobId), {
        method: 'POST',
        headers: getAuthHeaders()
    });
};

const checkATSScore = async (jobId, resumeFile) => {
    const formData = new FormData();
    formData.append('file', resumeFile);

    return await apiCall(API_CONFIG.ENDPOINTS.JOB_ATS_CHECK(jobId), {
        method: 'POST',
        headers: getAuthHeadersForUpload(),
        body: formData
    });
};

// Skills APIs
const addSkillAPI = async (skillName, proficiency = 'Intermediate') => {
    return await apiCall(API_CONFIG.ENDPOINTS.SKILLS, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ skill_name: skillName, proficiency })
    });
};

const deleteSkillAPI = async (skillId) => {
    return await apiCall(API_CONFIG.ENDPOINTS.DELETE_SKILL(skillId), {
        method: 'DELETE',
        headers: getAuthHeaders()
    });
};

// Startup Ideas APIs
const fetchStartupIdeas = async () => {
    return await apiCall(API_CONFIG.ENDPOINTS.STARTUP_IDEAS, {
        method: 'GET',
        headers: getAuthHeaders()
    });
};

const submitStartupIdea = async (ideaData) => {
    return await apiCall(API_CONFIG.ENDPOINTS.STARTUP_IDEAS, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(ideaData)
    });
};

const likeStartupIdea = async (ideaId) => {
    return await apiCall(API_CONFIG.ENDPOINTS.LIKE_IDEA(ideaId), {
        method: 'POST',
        headers: getAuthHeaders()
    });
};
