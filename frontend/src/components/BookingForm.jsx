import { useEffect, useMemo, useState } from 'react';
import { bookingAPI } from '../services/api';

export default function BookingForm({ timeSlots, defaultSlotId, onSuccess, onCancel }) {
  const initialSlotId = defaultSlotId || timeSlots.find((slot) => slot.available_spots > 0)?.id;
  const [formData, setFormData] = useState({
    time_slot_id: initialSlotId || '',
    attendee_name: '',
    email: '',
    number_of_seats: 1,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [bookingConfirmation, setBookingConfirmation] = useState(null);

  useEffect(() => {
    if (defaultSlotId) {
      setFormData((prev) => ({ ...prev, time_slot_id: defaultSlotId }));
    }
  }, [defaultSlotId]);

  const selectedSlot = useMemo(
    () => timeSlots.find((slot) => slot.id === formData.time_slot_id),
    [formData.time_slot_id, timeSlots]
  );

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
      if (selectedSlot && formData.number_of_seats > selectedSlot.available_spots) {
        setError(`Only ${selectedSlot.available_spots} spots are available for this slot.`);
        setLoading(false);
        return;
      }
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
          <p><strong>Magic Code:</strong> {bookingConfirmation.booking_token}</p>
          <p><strong>Name:</strong> {bookingConfirmation.attendee_name}</p>
          <p><strong>Email:</strong> {bookingConfirmation.email || '—'}</p>
          <p><strong>Seats:</strong> {bookingConfirmation.number_of_seats}</p>
        </div>
        <p className="mt-4 text-sm text-green-700">
          Save the magic code to update or cancel your booking later.
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
          <label htmlFor="time_slot_id" className="block text-sm font-medium text-gray-700 mb-1">
            Time Slot *
          </label>
          <select
            id="time_slot_id"
            name="time_slot_id"
            required
            value={formData.time_slot_id}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          >
            {timeSlots.map((slot) => (
              <option key={slot.id} value={slot.id} disabled={slot.available_spots === 0}>
                {slot.start_time.slice(0, 5)}–{slot.end_time.slice(0, 5)} · {slot.available_spots}/{slot.max_capacity} available
              </option>
            ))}
          </select>
        </div>

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
          <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
            Email Address (optional)
          </label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
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
            max={selectedSlot?.available_spots || 1}
            value={formData.number_of_seats}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          />
          {selectedSlot && (
            <p className="mt-1 text-xs text-gray-500">
              {selectedSlot.available_spots} spots available for this slot.
            </p>
          )}
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
