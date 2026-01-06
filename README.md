---
# Health Check Service

This project is a **health monitoring service** built with **FastAPI**.
It allows users to dynamically register external service URLs and checks their availability and performance through a unified `/health` endpoint.

The service reports both **individual service health** and **overall system health**, making it suitable for basic platform monitoring use cases.
---

## Features

- Dynamic registration of service URLs
- Supports checking **one, two, three, or more services**
- Health checks include:

  - HTTP status code
  - Response time
  - Timestamp of last check

- Aggregated system health status
- Fault isolation (one failing service does not stop others from being checked)

---

## How It Works

- Users register services using the provided API endpoints
- The system sends HTTP requests to all registered URLs
- A service is considered **up** if it responds with HTTP `200`
- Any non-200 response, timeout, or exception marks the service as **down**
- If one or more services are down, the overall system status is marked **unhealthy**

---

## API Endpoints

### Register a Single Service

```
POST /service
```

Registers one URL for monitoring.

---

### Register Multiple Services

```
POST /services/bulk
```

Registers two or more URLs at once.

---

### Health Check

```
GET /health
```

Checks the health of all registered services and returns an aggregated response.

---

## Example Health Response

```json
{
  "system_status": "unhealthy",
  "service_count": 3,
  "services": [
    {
      "service": "github",
      "url": "https://api.github.com",
      "status": "up",
      "http_status": 200,
      "response_time_ms": 124,
      "checked_at": "2026-01-06T08:20:10Z"
    },
    {
      "service": "httpbin_ok",
      "url": "https://httpbin.org/status/200",
      "status": "up",
      "http_status": 200,
      "response_time_ms": 98,
      "checked_at": "2026-01-06T08:20:10Z"
    },
    {
      "service": "httpbin_fail",
      "url": "https://httpbin.org/status/503",
      "status": "down",
      "http_status": 503,
      "response_time_ms": 102,
      "checked_at": "2026-01-06T08:20:10Z"
    }
  ]
}
```

---

## Failure Handling

If a monitored service becomes unreachable, times out, or returns a non-200 response:

- The service is marked as **down**
- The overall system health changes to **unhealthy**
- Other services continue to be checked normally

This ensures accurate reporting and fault isolation.

---

## Technologies Used

- Python
- FastAPI
- Requests
- RESTful API design

---

## Source Code & Live Demo

- **GitHub Repository:**
  [https://github.com/Destifaith/health-check.git](https://github.com/Destifaith/health-check.git)

- **Live Deployment:**
  [https://health-check-dxku.onrender.com](https://health-check-dxku.onrender.com/docs)

---
