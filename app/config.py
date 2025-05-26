from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MYSQL_HOST: str = "mysql"
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "password"
    MYSQL_DB: str = "delivery"
    REDIS_URL: str = "redis://redis:6379"
    CBR_API_URL: str = "https://www.cbr-xml-daily.ru/daily_json.js"
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    TEST_DATABASE_URL: str = "mysql://root:password@localhost/test_db"

    MONGO_HOST: str = "mongodb"
    MONGO_USER: str = "root"
    MONGO_PASSWORD: str = "password"
    MONGO_DB: str = "delivery_logs"


settings = Settings()
