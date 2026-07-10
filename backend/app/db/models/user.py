from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"  # DB에 생길 표 이름

    id = Column(Integer, primary_key=True, index=True)      # 고유번호(PK)
    name = Column(String, nullable=False)                   # 이름 (필수)
    email = Column(String, unique=True, nullable=False)     # 이메일 (필수, 중복금지)
    department = Column(String)                             # 부서
    role = Column(String)                                   # 역할
    created_at = Column(DateTime, server_default=func.now())  # 생성시각 자동입력
