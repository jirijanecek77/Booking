import {useEffect, useMemo, useState} from 'react';
import {useNavigate, useParams} from 'react-router-dom';
import {bookingAPI, eventAPI} from '../services/api';
import BookingForm from './BookingForm';

export default function EventDetails() {
    const {id} = useParams();
    const navigate = useNavigate();
    const [event, setEvent] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [showBookingForm, setShowBookingForm] = useState(false);
    const [selectedSlotId, setSelectedSlotId] = useState(null);

    const [manageToken, setManageToken] = useState('');
    const [manageBooking, setManageBooking] = useState(null);
    const [manageSlotId, setManageSlotId] = useState('');
    const [manageLoading, setManageLoading] = useState(false);
    const [manageError, setManageError] = useState(null);
    const [manageSuccess, setManageSuccess] = useState(null);

    useEffect(() => {
        loadEvent();
    }, [id]);

    const loadEvent = async () => {
        try {
            setLoading(true);
            const response = await eventAPI.getEvent(id);
            setEvent(response.data);
            setError(null);
        } catch (err) {
            setError('Failed to load event details. Please try again later.');
            console.error('Error loading event:', err);
        } finally {
            setLoading(false);
        }
    };

    const sortedSlots = useMemo(() => {
        if (!event?.time_slots) return [];
        return [...event.time_slots].sort((a, b) => a.start_time.localeCompare(b.start_time));
    }, [event]);

    const handleBookingSuccess = () => {
        setShowBookingForm(false);
        setSelectedSlotId(null);
        loadEvent();
    };

    const handleStartBooking = (slotId) => {
        setSelectedSlotId(slotId);
        setShowBookingForm(true);
    };

    const handleLoadBooking = async (e) => {
        e.preventDefault();
        setManageLoading(true);
        setManageError(null);
        setManageSuccess(null);

        try {
            const response = await bookingAPI.getBooking(manageToken.trim());
            setManageBooking(response.data);
            setManageSlotId(response.data.time_slot_id);
        } catch (err) {
            setManageError(err.response?.data?.detail || 'Unable to find that booking.');
            setManageBooking(null);
        } finally {
            setManageLoading(false);
        }
    };

    const handleUpdateBooking = async () => {
        if (!manageToken || !manageSlotId) return;
        setManageLoading(true);
        setManageError(null);
        setManageSuccess(null);

        try {
            const response = await bookingAPI.updateBooking(manageToken.trim(), {
                new_time_slot_id: manageSlotId,
            });
            setManageBooking(response.data);
            setManageSuccess('Booking updated successfully.');
            loadEvent();
        } catch (err) {
            setManageError(err.response?.data?.detail || 'Failed to update booking.');
        } finally {
            setManageLoading(false);
        }
    };

    const handleCancelBooking = async () => {
        if (!manageToken) return;
        setManageLoading(true);
        setManageError(null);
        setManageSuccess(null);

        try {
            await bookingAPI.cancelBooking(manageToken.trim());
            setManageBooking(null);
            setManageSuccess('Booking canceled.');
            loadEvent();
        } catch (err) {
            setManageError(err.response?.data?.detail || 'Failed to cancel booking.');
        } finally {
            setManageLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="flex justify-center items-center min-h-[400px]">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="max-w-4xl mx-auto">
                <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-800">
                    {error}
                </div>
                <button
                    onClick={() => navigate('/')}
                    className="mt-4 text-indigo-600 hover:text-indigo-800"
                >
                    ← Back to events
                </button>
            </div>
        );
    }

    if (!event) {
        return (
            <div className="max-w-4xl mx-auto text-center">
                <p className="text-gray-500">Event not found.</p>
                <button
                    onClick={() => navigate('/')}
                    className="mt-4 text-indigo-600 hover:text-indigo-800"
                >
                    ← Back to events
                </button>
            </div>
        );
    }

    const totalCapacity = sortedSlots.reduce((sum, slot) => sum + slot.max_capacity, 0);
    const availableSpots = sortedSlots.reduce((sum, slot) => sum + slot.available_spots, 0);

    return (
        <div className="max-w-4xl mx-auto">
            <button
                onClick={() => navigate('/')}
                className="mb-6 text-indigo-600 hover:text-indigo-800 flex items-center"
            >
                <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7"/>
                </svg>
                Back to events
            </button>

            <div className="bg-white rounded-lg shadow-lg overflow-hidden">
                <div className="bg-gradient-to-r from-indigo-600 to-purple-600 px-8 py-12">
                    <h1 className="text-4xl font-bold text-white mb-4">{event.name}</h1>
                    <p className="text-indigo-100 text-lg">{event.description}</p>
                </div>

                <div className="p-8 space-y-10">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                        <div className="space-y-4">
                            <div className="flex items-start">
                                <svg className="w-6 h-6 mr-3 text-indigo-600 flex-shrink-0 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                                          d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                                </svg>
                                <div>
                                    <p className="text-sm text-gray-500">Date</p>
                                    <p className="text-lg font-medium text-gray-900">
                                        {new Date(event.event_date).toLocaleDateString('en-US', {
                                            weekday: 'long',
                                            year: 'numeric',
                                            month: 'long',
                                            day: 'numeric',
                                        })}
                                    </p>
                                </div>
                            </div>
                        </div>

                        <div className="space-y-4">
                            <div className="flex items-start">
                                <svg className="w-6 h-6 mr-3 text-indigo-600 flex-shrink-0 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                                          d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>
                                </svg>
                                <div>
                                    <p className="text-sm text-gray-500">Availability</p>
                                    <p className="text-lg font-medium text-gray-900">
                                        {availableSpots} / {totalCapacity} spots available
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div>
                        <h2 className="text-2xl font-semibold text-gray-900 mb-4">Time Slots</h2>
                        <div className="space-y-3">
                            {sortedSlots.map((slot) => (
                                <div
                                    key={slot.id}
                                    className="flex flex-col md:flex-row md:items-center md:justify-between border border-gray-200 rounded-lg p-4"
                                >
                                    <div>
                                        <p className="text-lg font-medium text-gray-900">
                                            {slot.start_time.slice(0, 5)}–{slot.end_time.slice(0, 5)}
                                        </p>
                                        <p className="text-sm text-gray-500">
                                            {slot.available_spots} / {slot.max_capacity} available
                                        </p>
                                    </div>
                                    <button
                                        onClick={() => handleStartBooking(slot.id)}
                                        disabled={slot.available_spots === 0}
                                        className="mt-3 md:mt-0 px-5 py-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-300 text-white font-semibold rounded-lg transition-colors duration-200"
                                    >
                                        {slot.available_spots === 0 ? 'Fully booked' : 'Book this slot'}
                                    </button>
                                </div>
                            ))}
                        </div>

                        {sortedSlots.length === 0 && (
                            <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 text-gray-600">
                                No time slots have been published for this event yet.
                            </div>
                        )}

                        {showBookingForm && (
                            <BookingForm
                                timeSlots={sortedSlots}
                                defaultSlotId={selectedSlotId}
                                onSuccess={handleBookingSuccess}
                                onCancel={() => setShowBookingForm(false)}
                            />
                        )}
                    </div>

                    <div className="border-t border-gray-200 pt-8">
                        <h2 className="text-2xl font-semibold text-gray-900 mb-4">Manage Booking</h2>
                        <form onSubmit={handleLoadBooking} className="flex flex-col md:flex-row md:items-end gap-3">
                            <div className="flex-1">
                                <label htmlFor="manage_token" className="block text-sm font-medium text-gray-700 mb-1">
                                    Magic Code
                                </label>
                                <input
                                    id="manage_token"
                                    type="text"
                                    value={manageToken}
                                    onChange={(e) => setManageToken(e.target.value)}
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                                    placeholder="Paste your magic code"
                                />
                            </div>
                            <button
                                type="submit"
                                disabled={manageLoading || !manageToken.trim()}
                                className="px-6 py-2 bg-gray-900 text-white font-semibold rounded-lg hover:bg-gray-800 disabled:bg-gray-400"
                            >
                                {manageLoading ? 'Loading...' : 'Load booking'}
                            </button>
                        </form>

                        {manageError && (
                            <div className="mt-3 bg-red-50 border border-red-200 rounded-lg p-3 text-red-800 text-sm">
                                {manageError}
                            </div>
                        )}

                        {manageSuccess && (
                            <div className="mt-3 bg-green-50 border border-green-200 rounded-lg p-3 text-green-800 text-sm">
                                {manageSuccess}
                            </div>
                        )}

                        {manageBooking && (
                            <div className="mt-4 bg-gray-50 border border-gray-200 rounded-lg p-4 space-y-4">
                                <div>
                                    <p className="text-sm text-gray-500">Current booking</p>
                                    <p className="text-lg font-medium text-gray-900">{manageBooking.attendee_name}</p>
                                    <p className="text-sm text-gray-500">Seats: {manageBooking.number_of_seats}</p>
                                </div>

                                <div>
                                    <label htmlFor="manage_slot" className="block text-sm font-medium text-gray-700 mb-1">
                                        Change to new slot
                                    </label>
                                    <select
                                        id="manage_slot"
                                        value={manageSlotId}
                                        onChange={(e) => setManageSlotId(e.target.value)}
                                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                                    >
                                        {sortedSlots.map((slot) => (
                                            <option key={slot.id} value={slot.id} disabled={slot.available_spots === 0}>
                                                {slot.start_time.slice(0, 5)}–{slot.end_time.slice(0, 5)} · {slot.available_spots}/{slot.max_capacity} available
                                            </option>
                                        ))}
                                    </select>
                                </div>

                                <div className="flex flex-col md:flex-row gap-3">
                                    <button
                                        type="button"
                                        onClick={handleUpdateBooking}
                                        disabled={manageLoading}
                                        className="flex-1 px-6 py-2 bg-indigo-600 text-white font-semibold rounded-lg hover:bg-indigo-700 disabled:bg-indigo-300"
                                    >
                                        Update booking
                                    </button>
                                    <button
                                        type="button"
                                        onClick={handleCancelBooking}
                                        disabled={manageLoading}
                                        className="flex-1 px-6 py-2 bg-red-100 text-red-700 font-semibold rounded-lg hover:bg-red-200 disabled:bg-red-50"
                                    >
                                        Cancel booking
                                    </button>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
