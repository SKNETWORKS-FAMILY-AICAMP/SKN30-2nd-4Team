from pydantic import BaseModel, Field
from typing import List, Optional

class KeywordGroupDTO(BaseModel):
    """
    네이버 데이터랩 주제어 및 검색어 그룹 정보 DTO
    """
    groupName: str = Field(..., description="주제어 (검색어 묶음을 대표하는 이름)")
    keywords: List[str] = Field(..., description="주제어에 해당하는 검색어 목록 (최대 20개)")

class NaverSearchTrendRequestDTO(BaseModel):
    """
    네이버 통합 검색어 트렌드 API 요청 DTO
    """
    startDate: str = Field(..., description="조회 기간 시작 날짜 (yyyy-mm-dd)")
    endDate: str = Field(..., description="조회 기간 종료 날짜 (yyyy-mm-dd)")
    timeUnit: str = Field(..., description="구간 단위 (date: 일간, week: 주간, month: 월간)")
    keywordGroups: List[KeywordGroupDTO] = Field(..., description="주제어와 검색어 묶음 쌍의 배열 (최대 5개)")
    device: Optional[str] = Field(None, description="검색 환경 조건 (pc, mo)")
    gender: Optional[str] = Field(None, description="검색 사용자 성별 조건 (m: 남성, f: 여성)")
    ages: Optional[List[str]] = Field(None, description="검색 사용자 연령 조건 (1 ~ 11)")

class NaverSearchTrendDataDTO(BaseModel):
    """
    네이버 통합 검색어 트렌드 구간별 데이터 DTO
    """
    period: str = Field(..., description="구간별 시작 날짜 (yyyy-mm-dd)")
    ratio: float = Field(..., description="구간별 검색량의 상대적 비율 (0.00 ~ 100.00)")

class NaverSearchTrendResultDTO(BaseModel):
    """
    네이버 통합 검색어 트렌드 주제어별 결과 DTO
    """
    title: str = Field(..., description="주제어")
    keywords: List[str] = Field(..., description="주제어에 해당하는 검색어 목록")
    data: List[NaverSearchTrendDataDTO] = Field(..., description="구간별 데이터 목록")

class NaverSearchTrendResponseDTO(BaseModel):
    """
    네이버 통합 검색어 트렌드 API 전체 응답 DTO
    """
    startDate: str = Field(..., description="조회 기간 시작 날짜 (yyyy-mm-dd)")
    endDate: str = Field(..., description="조회 기간 종료 날짜 (yyyy-mm-dd)")
    timeUnit: str = Field(..., description="구간 단위 (date, week, month)")
    results: List[NaverSearchTrendResultDTO] = Field(..., description="주제어별 검색 추이 결과 리스트")
