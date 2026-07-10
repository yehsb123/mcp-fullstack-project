# DB 연결 설정 (SQLAlchemy 엔진, 세션)
# 1주차에 구현


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base   # declarative_base 추가
from app.core.config import settings #config에서 만든 settings 가져옴
from sqlalchemy.orm import sessionmaker 

#엔진 생성
engine=create_engine(settings.DATABASE_URL)

# SessionLocal 팩토리
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #세션 필요하면 SessionLocal()하면 세션 하나씩 뽑혀나옴

Base = declarative_base() 

#get_db 의존성 함수
def get_db():
    db = SessionLocal()      # 세션 하나 받아서 db에 담음 
    try:
        yield db             # 세션 빌려줌 (필요한 데서 씀)
    finally:
        db.close()           # 다 쓰면 세션 끊음 (항시)