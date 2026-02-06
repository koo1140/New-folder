# Skill: Fetch Weather Data Using Open-Meteo API

This skill teaches you how to fetch current weather data for any location using the **Open-Meteo API**. This API is free, doesn't require an API key, and provides structured JSON data.

---

## Steps to Fetch Weather Data

### 1. **Get Latitude and Longitude for a Location**
   - Use the `web_search` tool to find the latitude and longitude of a city (e.g., "latitude and longitude of Paris").
   - Alternatively, use a predefined list of coordinates for major cities (see below).

### 2. **Fetch Weather Data Using the Open-Meteo API**
   - Use the `execute_shell` tool to run a `curl` command to fetch weather data from the Open-Meteo API.
   - Example API request:
     ```bash
     curl "https://api.open-meteo.com/v1/forecast?latitude=40.7128&longitude=-74.0060&daily=temperature_2m_max,temperature_2m_min&timezone=America%2FNew_York"
     ```
   - Replace `latitude`, `longitude`, and `timezone` with the values for your location.

### 3. **Parse the JSON Response**
   - The API returns a JSON response with weather data.
   - Extract the following fields:
     - `daily.temperature_2m_max`: Maximum temperature for the day.
     - `daily.temperature_2m_min`: Minimum temperature for the day.
     - `timezone`: Timezone of the location.

### 4. **Present the Results**
   - Format the results in a user-friendly way. For example:
     ```
     Weather in New York (Timezone: America/New_York):
     - Maximum Temperature: 22°C
     - Minimum Temperature: 15°C
     ```

---

## Example Usage

### User Request:
```
User: "What's the weather like in New York?"
```

### Steps to Execute:
1. Use `web_search` to confirm the latitude and longitude of New York (e.g., 40.7128, -74.0060).
2. Use `execute_shell` to run the `curl` command:
   ```bash
   curl "https://api.open-meteo.com/v1/forecast?latitude=40.7128&longitude=-74.0060&daily=temperature_2m_max,temperature_2m_min&timezone=America%2FNew_York"
   ```
3. Parse the JSON response and extract the temperature data.
4. Present the results to the user:
   ```
   Weather in New York (Timezone: America/New_York):
   | Date       | Max Temperature | Min Temperature |
   |------------|-----------------|-----------------|
   | 2026-02-06 | -1.4°C          | -9.8°C          |
   | 2026-02-07 | -4.2°C          | -17.2°C         |
   ```

---

## Predefined Coordinates for Major Cities
| City       | Latitude | Longitude |
|------------|----------|-----------|
| New York   | 40.7128  | -74.0060  |
| London     | 51.5074  | -0.1278   |
| Tokyo      | 35.6762  | 139.6503  |
| Sydney     | -33.8688 | 151.2093  |
| Paris      | 48.8566  | 2.3522    |

---

## Notes
- If the `curl` command fails, check the internet connection or try again later.
- For more detailed weather data, you can add additional parameters to the API request (e.g., `hourly=temperature_2m`).
- The Open-Meteo API supports many other parameters. See the [Open-Meteo Documentation](https://open-meteo.com/en/docs) for more details.

---

## Tools Required
- `web_search` (to fetch latitude/longitude if not predefined)
- `execute_shell` (to run the `curl` command)