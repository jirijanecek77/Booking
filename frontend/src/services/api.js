import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const eventAPI = {
    getAllEvents: () => api.get('/events'),
    getEvent: (id) => api.get(`/events/${id}`),
    getEventSlots: (id) => api.get(`/events/${id}/slots`),
    createEvent: (data) => api.post('/events', data),
};

export const bookingAPI = {
    createBooking: (data) => api.post('/bookings', data),
    getBooking: (token) => api.get(`/bookings/${token}`),
    updateBooking: (token, data) => api.put(`/bookings/${token}`, data),
    cancelBooking: (token) => api.delete(`/bookings/${token}`),
};

export default api;
