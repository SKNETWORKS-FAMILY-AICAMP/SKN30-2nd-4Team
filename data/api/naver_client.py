import requests
from typing import Optional, List
from util import settings
from data.api.naver_dto import (
    NaverSearchTrendRequestDTO,
    NaverSearchTrendResponseDTO,
    KeywordGroupDTO
)

def get_naver_search_trend(
    start_date: str,
    end_date: str,
    time_unit: str,
    keyword_groups: List[KeywordGroupDTO],
    device: Optional[str] = None,
    gender: Optional[str] = None,
    ages: Optional[List[str]] = None
) -> Optional[NaverSearchTrendResponseDTO]:
    """
    네이버 통합 검색어 트렌드 API를 호출하여 검색 추이 데이터를 조회합니다.

    Args:
        start_date (str): 조회 기간 시작 날짜 (yyyy-mm-dd)
        end_date (str): 조회 기간 종료 날짜 (yyyy-mm-dd)
        time_unit (str): 구간 단위 (date, week, month)
        keyword_groups (List[KeywordGroupDTO]): 주제어 및 검색어 묶음 리스트
        device (str, optional): 검색 기기 조건 (pc, mo)
        gender (str, optional): 검색 사용자 성별 조건 (m, f)
        ages (List[str], optional): 검색 사용자 연령대 조건 (1 ~ 11)

    Returns:
        Optional[NaverSearchTrendResponseDTO]: API 응답 데이터 DTO, 실패 시 None
    """
    url = f"{settings.NAVER_API_URL}/datalab/search"
    
    headers = {
        "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": settings.NAVER_CLIENT_SECRET,
        "Content-Type": "application/json"
    }

    # Request DTO 생성 후 직렬화용 dictionary로 변환
    request_data = NaverSearchTrendRequestDTO(
        startDate=start_date,
        endDate=end_date,
        timeUnit=time_unit,
        keywordGroups=keyword_groups,
        device=device,
        gender=gender,
        ages=ages
    )
    
    # Pydantic v1, v2 호환성을 모두 만족하도록 처리
    try:
        body = request_data.model_dump(exclude_none=True)
    except AttributeError:
        body = request_data.dict(exclude_none=True)

    response = None
    try:
        response = requests.post(url, headers=headers, json=body)
        
        # HTTP 에러 핸들링
        response.raise_for_status()
        
        data = response.json()
        return NaverSearchTrendResponseDTO(**data)
        
    except requests.exceptions.HTTPError as e:
        status_code = response.status_code if response is not None else "Unknown"
        response_text = response.text if response is not None else "No Response Body"
        print(f"네이버 API HTTP 오류 발생 (상태 코드: {status_code}): {e}")
        print(f"응답 내용: {response_text}")
        raise
    except requests.exceptions.RequestException as e:
        print(f"네이버 API 호출 중 네트워크 오류 발생: {e}")
        raise
    except Exception as e:
        print(f"응답 처리 또는 DTO 변환 중 오류 발생: {e}")
        raise
