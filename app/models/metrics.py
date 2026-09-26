from pydantic import BaseModel, Field


class ServiceMetrics(BaseModel):
    memory_usage_percent: float = Field(ge=0.0, le=100.0)
    cpu_usage_percent: float = Field(ge=0.0, le=100.0)
    latency_ms: float = Field(ge=0.0)