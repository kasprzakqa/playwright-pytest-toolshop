"""Environment-driven configuration. Same suite runs against the Docker app or the live demo."""

import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL: str = os.getenv("BASE_URL", "https://practicesoftwaretesting.com")
API_BASE_URL: str = os.getenv("API_BASE_URL", "https://api.practicesoftwaretesting.com")

# Published demo accounts, documented by the application for testing, not secrets.
CUSTOMER_EMAIL: str = os.getenv("CUSTOMER_EMAIL", "customer@practicesoftwaretesting.com")
CUSTOMER_PASSWORD: str = os.getenv("CUSTOMER_PASSWORD", "welcome01")
