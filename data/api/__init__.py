"""
영화진흥위원회(KOBIS) API 클라이언트 패키지
이 패키지는 영화 관련 데이터를 조회하는 다양한 API 함수를 제공합니다.
"""

from data.api.kobis_client import (
    get_daily_box_office,  # 일일 박스오피스 조회
    get_common_codes,      # 지역/영화형태 등 공통코드 조회
    get_movie_list,        # 영화 목록 검색
    get_movie_info,        # 영화 상세 정보 조회
    get_company_list,      # 영화사 목록 검색
    get_company_info,      # 영화사 상세 정보 조회
    get_people_list,       # 영화인 목록 검색
    get_people_info        # 영화인 상세 정보 조회
)

# 외부에서 'from data.api import *' 등을 사용할 때 공개될 함수 목록
# ex: from data.api import get_movie_list, get_movie_info
__all__ = [
    "get_daily_box_office",  # 일일 박스오피스 조회
    "get_common_codes",      # 지역/영화형태 등 공통코드 조회
    "get_movie_list",        # 영화 목록 검색
    "get_movie_info",        # 영화 상세 정보 조회
    "get_company_list",      # 영화사 목록 검색
    "get_company_info",      # 영화사 상세 정보 조회
    "get_people_list",       # 영화인 목록 검색
    "get_people_info"        # 영화인 상세 정보 조회
]
