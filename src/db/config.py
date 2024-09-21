from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str = "development"
    REDIS: str = "redis"
    REDIS_PORT: int = 6379    
    DATABASE_URL: str = "sqlite:///./test.db"
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    MAIL_USERNAME: str = "osamaahmed170395@gmail.com"
    MAIL_PASSWORD: str = "rkqshwadhiyfhwls"

    class Config:
        env_file = ".env"


settings = Settings()
