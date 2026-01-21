// Authentication Helper Functions

const setAuthToken = (token) => {
    localStorage.setItem('auth_token', token);
};

const getAuthToken = () => {
    return localStorage.getItem('auth_token');
};

const removeAuthToken = () => {
    localStorage.removeItem('auth_token');
};

const setUserInfo = (userInfo) => {
    localStorage.setItem('user_info', JSON.stringify(userInfo));
};

const getUserInfo = () => {
    const userInfo = localStorage.getItem('user_info');
    return userInfo ? JSON.parse(userInfo) : null;
};

const removeUserInfo = () => {
    localStorage.removeItem('user_info');
};

const isAuthenticated = () => {
    return !!getAuthToken();
};

const getAuthHeaders = () => {
    const token = getAuthToken();
    return {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    };
};

const getAuthHeadersForUpload = () => {
    const token = getAuthToken();
    return {
        'Authorization': `Bearer ${token}`
    };
};

// Login function
const loginStudent = async (studentId, password) => {
    try {
        const response = await fetch(getApiUrl(API_CONFIG.ENDPOINTS.STUDENT_LOGIN), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                student_id: studentId,
                password: password
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Login failed');
        }

        const data = await response.json();
        
        setAuthToken(data.access_token);
        setUserInfo({
            id: data.student_id,
            name: data.name,
            student_id: data.student_id_number
        });

        return data;
    } catch (error) {
        console.error('Login error:', error);
        throw error;
    }
};

// Logout function (update your existing logout function)
const logout = () => {
    removeAuthToken();
    removeUserInfo();
    window.location.reload();
};