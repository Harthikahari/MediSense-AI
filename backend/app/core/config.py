"""
Configuration management for MediSense-AI.
Loads settings from environment variables with validation.
"""

from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field, validator


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    ENV: str = Field(default="development", description="Environment: development, staging, production")
    HOST: str = Field(default="0.0.0.0", description="Host to bind")
    PORT: int = Field(default=8000, description="Port to bind")
    DEBUG: bool = Field(default=True, description="Debug mode")

    # Database
    DATABASE_URL: str = Field(
        default="postgresql://medisense:medipass@db:5432/medisense_db",
        description="PostgreSQL connection URL"
    )
    POSTGRES_USER: str = Field(default="medisense")
    POSTGRES_PASSWORD: str = Field(default="medipass")
    POSTGRES_DB: str = Field(default="medisense_db")
    POSTGRES_HOST: str = Field(default="db")
    POSTGRES_PORT: int = Field(default=5432)

    # Redis / Celery
    REDIS_URL: str = Field(default="redis://redis:6379/0")
    CELERY_BROKER_URL: str = Field(default="redis://redis:6379/0")
    CELERY_RESULT_BACKEND: str = Field(default="redis://redis:6379/0")

    # MCP & LLM
    MCP_MODE: str = Field(default="mock", description="MCP mode: mock or anthropic")
    ANTHROPIC_API_KEY: Optional[str] = Field(default=None, description="Anthropic API key")
    MCP_HOST: str = Field(default="http://mcp:8001")
    MCP_TIMEOUT: int = Field(default=30, description="MCP request timeout in seconds")

    # Vector Database (Chroma)
    CHROMA_PERSIST_DIR: str = Field(default="/data/chroma")
    CHROMA_HOST: str = Field(default="localhost")
    CHROMA_PORT: int = Field(default=8001)
    EMBEDDING_MODEL: str = Field(default="sentence-transformers/all-MiniLM-L6-v2")
    EMBEDDING_DIMENSION: int = Field(default=384)

    # Payment Gateway
    PAYMENT_SDK_KEY: str = Field(default="test_payment_key_sandbox")
    PAYMENT_MODE: str = Field(default="sandbox", description="Payment mode: sandbox or live")
    PAYMENT_WEBHOOK_SECRET: str = Field(default="webhook_secret")

    # Email / SMS
    SMTP_HOST: str = Field(default="smtp.example.com")
    SMTP_PORT: int = Field(default=587)
    SMTP_USER: str = Field(default="notifications@medisense.ai")
    SMTP_PASSWORD: str = Field(default="")
    SMTP_FROM_EMAIL: str = Field(default="noreply@medisense.ai")
    SMTP_USE_TLS: bool = Field(default=True)

    SMS_PROVIDER: str = Field(default="twilio")
    TWILIO_ACCOUNT_SID: Optional[str] = Field(default=None)
    TWILIO_AUTH_TOKEN: Optional[str] = Field(default=None)
    TWILIO_PHONE_NUMBER: Optional[str] = Field(default=None)

    # Security & Authentication
    JWT_SECRET: str = Field(default="very_secret_jwt_key")
    JWT_ALGORITHM: str = Field(default="HS256")
    JWT_EXPIRATION_MINUTES: int = Field(default=60)
    SECRET_KEY: str = Field(default="app_secret_key")

    # CORS
    CORS_ORIGINS: str = Field(default="http://localhost:3000,http://localhost:8000")

    @validator("CORS_ORIGINS", pre=True)
    def parse_cors_origins(cls, v):
        """Parse CORS origins from comma-separated string to list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    # Guardrails
    GUARDRAILS_ENABLED: bool = Field(default=True)
    GUARDRAILS_POLICY_FILE: str = Field(default="/app/config/guardrail_policies.yaml")
    PHI_REDACTION_ENABLED: bool = Field(default=True)

    # ONNX Model
    ONNX_MODEL_PATH: str = Field(default="/app/models/symptom_classifier.onnx")
    ONNX_THREADS: int = Field(default=4)
    ONNX_DEVICE: str = Field(default="cpu")

    # OCR
    TESSERACT_CMD: str = Field(default="/usr/bin/tesseract")
    OCR_LANGUAGE: str = Field(default="eng")

    # Audit & Logging
    LOG_LEVEL: str = Field(default="INFO")
    AUDIT_ENABLED: bool = Field(default=True)
    AUDIT_LOG_PATH: str = Field(default="/var/log/medisense/audit.log")

    # RAGAS Evaluation
    RAGAS_EVAL_DATASET: str = Field(default="/app/ragas/testset.jsonl")
    RAGAS_CONFIG: str = Field(default="/app/ragas/ragas_config.yaml")

    # RLHF
    RLHF_ENABLED: bool = Field(default=False)
    RLHF_DATA_PATH: str = Field(default="/app/rlhf/data")
    RLHF_REWARD_MODEL_PATH: str = Field(default="/app/rlhf/models/reward_model")

    # Performance & Rate Limiting
    MAX_WORKERS: int = Field(default=4)
    RATE_LIMIT_PER_MINUTE: int = Field(default=60)
    AGENT_TIMEOUT_SECONDS: int = Field(default=120)
    MAX_CONCURRENT_AGENTS: int = Field(default=10)

    # Feature Flags
    FEATURE_IMAGE_ANALYSIS: bool = Field(default=True)
    FEATURE_PRESCRIPTION_GEN: bool = Field(default=True)
    FEATURE_PAYMENT_INTEGRATION: bool = Field(default=True)
    FEATURE_RLHF_FEEDBACK: bool = Field(default=False)

    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings."""
    return settings
