"""Application settings and configuration."""

import os
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
INPUTS_DIR = DATA_DIR / "inputs"
OUTPUTS_DIR = DATA_DIR / "outputs"
HISTORY_DIR = DATA_DIR / "history"


class Settings(BaseModel):
    """Application settings with validation."""

    # API Configuration
    qubrid_api_key: str = Field(..., description="Qubrid API key")
    qubrid_base_url: str = Field(
        default="https://platform.qubrid.com/v1",
        description="Qubrid API base URL"
    )

    # Model Configuration
    model_name: str = Field(
        default="mistralai/Mistral-7B-Instruct-v0.3",
        description="Model identifier"
    )
    temperature_analysis: float = Field(
        default=0.3,
        ge=0.0,
        le=1.0,
        description="Temperature for analysis tasks"
    )
    temperature_generation: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Temperature for generation tasks"
    )
    max_tokens: int = Field(
        default=4096,
        ge=512,
        le=8192,
        description="Maximum tokens for responses"
    )

    # Workflow Configuration
    max_iterations: int = Field(
        default=3,
        ge=1,
        le=5,
        description="Maximum critique-draft iterations"
    )
    critique_threshold: float = Field(
        default=8.0,
        ge=0.0,
        le=10.0,
        description="Minimum score to approve resume"
    )

    # Retry Configuration
    max_retries: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Maximum API retry attempts"
    )
    retry_delay: float = Field(
        default=1.0,
        ge=0.1,
        le=10.0,
        description="Initial retry delay in seconds"
    )

    @field_validator("qubrid_api_key")
    @classmethod
    def validate_api_key(cls, v: str) -> str:
        """Validate API key is not empty or placeholder."""
        if not v or v == "your_qubrid_api_key_here":
            raise ValueError(
                "QUBRID_API_KEY not set. Please add it to .env file."
            )
        return v

    class Config:
        """Pydantic configuration."""
        env_prefix = ""
        case_sensitive = False


def load_settings() -> Settings:
    """Load and validate settings from environment variables."""
    try:
        return Settings(
            qubrid_api_key=os.getenv("QUBRID_API_KEY", ""),
            qubrid_base_url=os.getenv(
                "QUBRID_BASE_URL",
                "https://platform.qubrid.com/v1"
            ),
            model_name=os.getenv(
                "MODEL_NAME",
                "mistralai/Mistral-7B-Instruct-v0.3"
            ),
            temperature_analysis=float(os.getenv("TEMPERATURE_ANALYSIS", "0.3")),
            temperature_generation=float(os.getenv("TEMPERATURE_GENERATION", "0.7")),
            max_iterations=int(os.getenv("MAX_ITERATIONS", "3")),
        )
    except Exception as e:
        raise RuntimeError(f"Failed to load settings: {e}")


# Create data directories if they don't exist
for directory in [INPUTS_DIR, OUTPUTS_DIR, HISTORY_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Global settings instance
settings = load_settings()
