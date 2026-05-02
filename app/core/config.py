from pydantic_settings import BaseSettings

class Config(BaseSettings):
    app_name: str = "UrlShortener"
    debug: bool = False
    db_user: str = ""
    db_password: str = ""
    db_name: str = "urls.db"
    redis_host: str = "localhost"
    redis_port: int = 6379

    @property
    def db_url(self):
        return f"sqlite:///./{self.db_name}"
    
config = Config()
