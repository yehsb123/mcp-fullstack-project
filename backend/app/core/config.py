# 앱 설정 (환경변수 로딩)
# 1주차에 구현

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
      DATABASE_URL: str
      ANTHROPIC_API_KEY: str = ""

      model_config = {"env_file": ".env"}


settings = Settings()
