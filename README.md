
## Capital Time API

This API returns the current local time and UTC offset for selected capital cities. 

## What It Does

You send a **capital city name** to the API, and it gives you:

- The current **local time**
- The **UTC offset**


### How to Use

**Endpoint:**  
`GET http://34.69.20.158:5000/api/time?city=London`

**Headers:**  
To access the API, you need to include this token in your request header:

`Authorization: Bearer supersecrettoken123`

**Response:**
```json
{
  "city": "London",
  "local_time": "2025-04-22 20:40:32",
  "UTC_offset": "+01:00"
}
