import { useState } from 'react';
import { bookingAPI } from '../services/api';

export default function BookingForm({ eventId, onSuccess, onCancel }) {
  const [formData, setFormData] = useState({
    event_id: eventId,
    attendee_name: '',
    attendee_email: '',
    number_of_seats: 1,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [bookingConfirmation, setBookingConfirmation] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === 'number_of_seats' ? parseInt(value) : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await bookingAPI.createBooking(formData);
      setBookingConfirmation(response.data);
      setTimeout(() => {
        onSuccess();
      }, 3000);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        'Failed to create booking. Please try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  if (bookingConfirmation) {
    return (
      <div className="bg-green-50 border border-green-200 rounded-lg p-6 mt-6">
        <div className="flex items-center mb-4">
          <svg className="w-8 h-8 text-green-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <h3 className="text-xl font-semibold text-green-900">Booking Confirmed!</h3>
        </div>
        <div className="space-y-2 text-green-800">
          <p><strong>Booking ID:</strong> {bookingConfirmation.id}</p>
          <p><strong>Name:</strong> {bookingConfirmation.attendee_name}</p>
          <p><strong>Email:</strong> {bookingConfirmation.attendee_email}</p>
          <p><strong>Seats:</strong> {bookingConfirmation.number_of_seats}</p>
          <p><strong>Status:</strong> <span className="font-semibold capitalize">{bookingConfirmation.status}</span></p>
        </div>
        <p className="mt-4 text-sm text-green-700">
          A confirmation email has been sent to your email address.
        </p>
      </div>
    );
  }

  return (
    <div className="bg-gray-50 rounded-lg p-6 mt-6">
      <h3 className="text-xl font-semibold text-gray-900 mb-4">Book Your Seat</h3>

      {error && (
        <div className="mb-4 bg-red-50 border border-red-200 rounded-lg p-3 text-red-800 text-sm">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="attendee_name" className="block text-sm font-medium text-gray-700 mb-1">
            Full Name *
          </label>
          <input
            type="text"
            id="attendee_name"
            name="attendee_name"
            required
            value={formData.attendee_name}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            placeholder="John Doe"
          />
        </div>

        <div>
          <label htmlFor="attendee_email" className="block text-sm font-medium text-gray-700 mb-1">
            Email Address *
          </label>
          <input
            type="email"
            id="attendee_email"
            name="attendee_email"
            required
            value={formData.attendee_email}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            placeholder="john@example.com"
          />
        </div>

        <div>
          <label htmlFor="number_of_seats" className="block text-sm font-medium text-gray-700 mb-1">
            Number of Seats *
          </label>
          <input
            type="number"
            id="number_of_seats"
            name="number_of_seats"
            required
            min="1"
            max="10"
            value={formData.number_of_seats}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>

        <div className="flex gap-3 pt-4">
          <button
            type="submit"
            disabled={loading}
            className="flex-1 px-6 py-3 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-400 text-white font-semibold rounded-lg transition-colors duration-200"
          >
            {loading ? 'Processing...' : 'Confirm Booking'}
          </button>
          <button
            type="button"
            onClick={onCancel}
            disabled={loading}
            className="px-6 py-3 bg-gray-200 hover:bg-gray-300 disabled:bg-gray-100 text-gray-700 font-semibold rounded-lg transition-colors duration-200"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}
