from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import requests
from requests.exceptions import RequestException
from datetime import datetime
import time
from typing import List

app = FastAPI(title="Flexible Health Monitoring Service")

TIMEOUT_SECONDS = 3

# In-memory store
SERVICES: dict[str, str] = {}


# ----------- MODELS -----------

class SingleServiceInput(BaseModel):
    name: str
    url: HttpUrl


class BulkServiceInput(BaseModel):
    services: List[SingleServiceInput]


# ----------- HEALTH CHECK -----------

def check_service(name: str, url: str):
    start_time = time.time()

    try:
        response = requests.get(url, timeout=TIMEOUT_SECONDS)
        elapsed_ms = int((time.time() - start_time) * 1000)

        return {
            "service": name,
            "url": url,
            "status": "up" if response.status_code == 200 else "down",
            "http_status": response.status_code,
            "response_time_ms": elapsed_ms,
            "checked_at": datetime.utcnow().isoformat() + "Z"
        }

    except RequestException as e:
        elapsed_ms = int((time.time() - start_time) * 1000)

        return {
            "service": name,
            "url": url,
            "status": "down",
            "http_status": None,
            "response_time_ms": elapsed_ms,
            "error": str(e),
            "checked_at": datetime.utcnow().isoformat() + "Z"
        }


# ----------- REGISTRATION ENDPOINTS -----------

@app.post("/service")
def add_single_service(service: SingleServiceInput):
    if service.name in SERVICES:
        raise HTTPException(status_code=400, detail="Service name already exists")

    SERVICES[service.name] = service.url

    return {
        "message": "Service added",
        "total_services": len(SERVICES)
    }


@app.post("/services/bulk")
def add_multiple_services(payload: BulkServiceInput):
    if len(payload.services) < 2:
        raise HTTPException(
            status_code=400,
            detail="Bulk endpoint requires at least 2 services"
        )

    for service in payload.services:
        if service.name in SERVICES:
            raise HTTPException(
                status_code=400,
                detail=f"Service '{service.name}' already exists"
            )

    for service in payload.services:
        SERVICES[service.name] = service.url

    return {
        "message": "Services added successfully",
        "added_count": len(payload.services),
        "total_services": len(SERVICES)
    }


# ----------- HEALTH ENDPOINT -----------

@app.get("/health")
def health_check():
    if not SERVICES:
        raise HTTPException(status_code=400, detail="No services registered")

    results = []
    system_status = "healthy"

    for name, url in SERVICES.items():
        result = check_service(name, url)
        results.append(result)

        if result["status"] == "down":
            system_status = "unhealthy"

    return {
        "system_status": system_status,
        "service_count": len(SERVICES),
        "services": results
    }
