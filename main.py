from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, HttpUrl
import requests
from requests.exceptions import RequestException

app = FastAPI()

class ServiceConfig(BaseModel):
    services: dict[str, HttpUrl]

SERVICES = {
    "github_api": "https://api.github.com",
    "httpbin_ok": "https://httpbin.org/status/200",
    "httpbin_fail": "https://httpbin.org/status/500"
}

def check_service(url):
    try:
        response = requests.get(url, timeout=3)
        return "healthy" if response.status_code == 200 else "unhealthy"
    except RequestException:
        return "unhealthy"

@app.post("/configure")
def configure_services(config: ServiceConfig):
    global SERVICES
    SERVICES = dict(config.services)
    return {"message": "Services updated successfully"}

@app.get("/health")
def health_check():
    results = {}
    unhealthy_count = 0

    for name, url in SERVICES.items():
        status = check_service(url)
        results[name] = status
        if status == "unhealthy":
            unhealthy_count += 1

    if unhealthy_count == 0:
        overall_status = "healthy"
    elif unhealthy_count < len(SERVICES):
        overall_status = "degraded"
    else:
        overall_status = "unhealthy"

    return JSONResponse(
        content={
            "status": overall_status,
            "services": results
        }
    )
