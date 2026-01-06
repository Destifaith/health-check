# Health Check Service

This is a simple health check service built with FastAPI.  
It monitors three external endpoints and exposes their status via `/health`.

## How it Works

- The service sends HTTP requests to each configured endpoint
- If an endpoint returns status code 200, it is considered healthy
- Any failure or exception marks the service as unhealthy

## Endpoint

GET /health

### Example Response

```json
{
  "status": "degraded",
  "services": {
    "github_api": "healthy",
    "httpbin_ok": "healthy",
    "httpbin_fail": "unhealthy"
  }
}
```
