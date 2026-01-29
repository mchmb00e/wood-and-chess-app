import axios from 'axios';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    headers: {
        'Content-Type': 'application/json'
    },
    validateStatus: function (status) {
        return status >= 200 && status < 500;
    }
});

export default api;