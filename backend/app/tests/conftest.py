import os
os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("USE_MOCK_SCRAPERS", "true")
