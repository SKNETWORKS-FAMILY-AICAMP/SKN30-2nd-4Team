# =================================================================
# 프로젝트 전역 설정 관리 모듈
# 팀원 필독: .env 파일에 DB 연결 정보를 반드시 설정해야 합니다.
# =================================================================

import os
from dotenv import load_dotenv
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Dict, Any

# 1. 프로젝트 루트 경로 설정 (프로젝트 어느 위치에서든 .env를 찾기 위함)
# Path(__file__)는 이 파일(config.py)의 위치를 의미합니다.
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / '.env'

# 2. .env 파일 로드 (DB_HOST, DB_USER 등의 환경변수 활성화)
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv() # 기본 .env 로드 시도

class AppSettings(BaseModel):
    """
    프로젝트 전역 설정을 속성 단위로 관리하는 DTO 클래스입니다.
    Pydantic을 사용하여 타입 검증 및 환경변수 매핑을 수행합니다.
    """
    # 1. KOBIS API 설정
    KOBIS_URL: str = Field(default=os.getenv('KOBIS_URL', 'http://www.kobis.or.kr/kobisopenapi/webservice/rest'))
    KOBIS_KEY: str | None = Field(default=os.getenv('KOBIS_KEY'))

    # 2. 데이터베이스 연결 설정
    DB_CONFIG: Dict[str, Any] = Field(default={
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME', 'film'),
        'connection_timeout': 10
    })

# 전역 설정 객체 생성 (싱글톤)
settings = AppSettings()