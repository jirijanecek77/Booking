# Event Booking API

A token-based event booking system built with FastAPI, SQLAlchemy, and Clean Architecture principles. Users can book time slots for events using only their name, receiving a unique token to manage their booking.

## Features

- ✅ Create events with multiple time slots
- ✅ Book time slots with minimal information (just name)
- ✅ Token-based booking management (no passwords)
- ✅ View, update, and cancel bookings using token
- ✅ Real-time capacity tracking
- ✅ Optional email for notifications
- ✅ Clean Architecture (Domain, Application, Infrastructure layers)
- ✅ Async SQLAlchemy with PostgreSQL
- ✅ FastAPI with automatic OpenAPI documentation
- ✅ Poetry for dependency management
- ✅ Alembic for database migrations

## Architecture

```
src/
├── domain/              # Business entities and repository interfaces
│   ├── entities/        # Event, TimeSlot, Booking
│   └── repositories/    # Abstract repository interfaces
├── application/         # Use cases (business logic)
│   └── use_cases/       # CreateBooking, UpdateBooking, etc.
├── infrastructure/      # External implementations
│   ├── database/        # SQLAlchemy models and repositories
│   └── api/            # FastAPI routes and schemas
└── main.py             # Application entry point
```

## Quick Start

### Using Docker (Recommended)

```bash
# Build and run (PostgreSQL + API)
docker-compose up

# The first time it runs, Alembic migrations will be applied automatically
# API will be available at http://localhost:8000
# PostgreSQL at localhost:5432
# Interactive docs at http://localhost:8000/docs
```

### Manual Setup

#### Prerequisites
- Python 3.11+
- Poetry
- PostgreSQL 16+

```bash
# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Copy environment file
cp .env.example .env

# Start PostgreSQL (or use Docker for just the database)
docker run -d \
  --name postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=event_booking \
  -p 5432:5432 \
  postgres:16-alpine

# Run database migrations
poetry run alembic upgrade head

# Run application
poetry run uvicorn src.main:app --reload

# API will be available at http://localhost:8000
```

## API Endpoints

### Events

- `POST /api/v1/events` - Create event with time slots
- `GET /api/v1/events` - List all events
- `GET /api/v1/events/{event_id}` - Get event details
- `GET /api/v1/events/{event_id}/slots` - Get available time slots

### Bookings

- `POST /api/v1/bookings` - Create a booking (returns token)
- `GET /api/v1/bookings/{token}` - Get booking details
- `PUT /api/v1/bookings/{token}` - Update booking (change time slot)
- `DELETE /api/v1/bookings/{token}` - Cancel booking

## Usage Examples

### 1. Create an Event

```bash
curl -X POST "http://localhost:8000/api/v1/events" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tech Conference 2024",
    "event_date": "2024-06-15",
    "description": "Annual tech conference",
    "time_slots": [
      {
        "start_time": "09:00:00",
        "end_time": "09:30:00",
        "max_capacity": 10
      },
      {
        "start_time": "09:30:00",
        "end_time": "10:00:00",
        "max_capacity": 10
      }
    ]
  }'
```

### 2. Create a Booking

```bash
curl -X POST "http://localhost:8000/api/v1/bookings" \
  -H "Content-Type: application/json" \
  -d '{
    "attendee_name": "John Doe",
    "time_slot_id": "your-time-slot-uuid",
    "email": "john@example.com"
  }'

# Response includes booking_token - SAVE THIS!
{
  "id": "...",
  "attendee_name": "John Doe",
  "time_slot_id": "...",
  "booking_token": "abc123xyz...",
  "email": "john@example.com",
  "created_at": "2024-01-01T10:00:00"
}
```

### 3. View Your Booking

```bash
curl "http://localhost:8000/api/v1/bookings/{your-token}"
```

### 4. Change Your Time Slot

```bash
curl -X PUT "http://localhost:8000/api/v1/bookings/{your-token}" \
  -H "Content-Type: application/json" \
  -d '{
    "new_time_slot_id": "new-time-slot-uuid"
  }'
```

### 5. Cancel Your Booking

```bash
curl -X DELETE "http://localhost:8000/api/v1/bookings/{your-token}"
```

## Interactive API Documentation

Visit `http://localhost:8000/docs` for Swagger UI documentation where you can test all endpoints interactively.

## Database

The application uses **PostgreSQL** with async SQLAlchemy and Alembic for migrations.

### Database Migrations

```bash
# Create a new migration
poetry run alembic revision --autogenerate -m "description"

# Apply migrations
poetry run alembic upgrade head

# Rollback last migration
poetry run alembic downgrade -1

# View migration history
poetry run alembic history
```

### Database Connection
Default connection string: `postgresql+asyncpg://postgres:postgres@localhost:5432/event_booking`

Update `DATABASE_URL` in `.env` to change database configuration.

## Security Considerations

- **Token Security**: Booking tokens are cryptographically secure (32-byte URL-safe)
- **Rate Limiting**: Consider adding rate limiting in production
- **CORS**: Update CORS origins in production
- **Token Storage**: Users must save their token - no recovery without it
- **Optional Contact**: Email/phone are optional but recommended for recovery

## Future Enhancements

- [ ] Email notifications (booking confirmation, reminders)
- [ ] SMS notifications
- [ ] QR code generation for bookings
- [ ] Calendar integration (iCal export)
- [ ] Admin dashboard
- [ ] Rate limiting
- [ ] Redis caching for high traffic
- [ ] Webhook notifications
- [ ] Multi-language support

## Development

```bash
# Install dev dependencies
poetry install

# Run tests
poetry run pytest

# Format code
poetry run black src/
poetry run isort src/

# Type checking
poetry run mypy src/

# Add a new dependency
poetry add package-name

# Add a dev dependency
poetry add --group dev package-name
```

## Project Structure

```
event-booking-app/
├── src/
│   ├── domain/                 # Business logic layer
│   │   ├── entities/          # Domain entities
│   │   └── repositories/      # Repository interfaces
│   ├── application/           # Application layer
│   │   └── use_cases/        # Business use cases
│   ├── infrastructure/        # Infrastructure layer
│   │   ├── database/         # Database implementation
│   │   └── api/              # API routes & schemas
│   └── main.py               # FastAPI app entry point
├── alembic/                   # Database migrations
│   ├── versions/             # Migration files
│   └── env.py                # Alembic configuration
├── pyproject.toml            # Poetry dependencies
├── alembic.ini               # Alembic config
├── docker-compose.yml        # Docker services
└── README.md
```

## License

MIT License
