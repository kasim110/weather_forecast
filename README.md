# User Authentication and Weather History API

This project implements user authentication (register, login, and logout) and an API for retrieving historic weather data based on location (Latitude & Longitude) and the number of days in the past.

## API Endpoints

### User Authentication Endpoints

#### Register User
- Endpoint: `POST /users/user-register/`
- Description: Register a new user.
- Request Body:
    ```json
    {
        "first_name": "f_name",
        "last_name": "l_name",
        "mobile": "1234567",
        "email": "demo@gmail.com",
        "password": "password123"
    }
    ```
- Response: Returns the created user details.

#### Login User (Get Authentication Token)
- Endpoint: `POST /users/user-login/`
- Description: Log in an existing user and retrieve an authentication token.
- Request Body:
    ```json
    {
        "username": "existing_user",
        "password": "password123"
    }
    ```
- Response: Returns an authentication token for the logged-in user.

#### Logout User
- Endpoint: `POST /users/user-logout/`
- Description: Log out an authenticated user.
- Response: Returns a success message.

### Weather History API

#### Get Historic Weather Data
- Endpoint: `POST /users/get-history-weather-data/`
- Description: Retrieve historic weather data based on location (Latitude & Longitude) and the number of days in the past.
- Request Body:
    ```json
    {
        "latitude": 37.7749,
        "longitude": -122.4194,
        "num_days": 7
    }
    ```
- Response: Returns historic weather data for the specified location and time range.

## Project Structure

- `users/`: Django app for user authentication.
    - Include information about models, serializers, views, and URLs related to user authentication and about the `HistoricWeatherAPIView`.
- `weather_forecast/settings.py`: Django project settings.

## Running the Project

1. Install required packages: `pip install -r requirements.txt`
2. Apply migrations: `python manage.py migrate`
3. Start the development server: `python manage.py runserver`

## Usage

- Use API client tools like Postman or cURL to interact with the implemented endpoints.
- Register, log in, and log out users using the provided authentication endpoints.
- Retrieve historic weather data using the Weather History API.