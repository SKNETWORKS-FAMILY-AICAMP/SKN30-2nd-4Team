import requests
from datetime import date
from typing import Optional, Dict
from util import settings
from data.api.kobis_dto import (
    DailyBoxOfficeResponseDTO, CommonCodeResponseDTO, 
    MovieListResponseDTO, MovieInfoResponseDTO,
    CompanyListResponseDTO, CompanyInfoResponseDTO,
    PeopleListResponseDTO, PeopleInfoResponseDTO
)

def get_people_info(people_cd: str) -> Optional[PeopleInfoResponseDTO]:
    """
    영화인 상세정보를 조회합니다.

    Args:
        people_cd (str): 영화인 고유 코드

    Returns:
        Optional[PeopleInfoResponseDTO]: 조회 성공 시 DTO 객체, 실패 시 None
    """
    path = "/people/searchPeopleInfo.json"
    params = {
        "peopleCd": people_cd
    }

    data = _call_api(path, params)
    
    if data:
        try:
            return PeopleInfoResponseDTO(**data)
        except Exception as e:
            print(f"DTO 변환 중 오류 발생: {e}")
            return None
    return None

def get_people_list(people_nm: Optional[str] = None,
                    filmo_names: Optional[str] = None,
                    cur_page: str = "1",
                    item_per_page: str = "10") -> Optional[PeopleListResponseDTO]:
    """
    영화인 목록을 조회합니다.

    Args:
        people_nm (str, optional): 영화인명
        filmo_names (str, optional): 필모리스트(작품명)
        cur_page (str): 현재 페이지 (기본 1)
        item_per_page (str): 결과 개수 (기본 10)

    Returns:
        Optional[PeopleListResponseDTO]: 조회 성공 시 DTO 객체, 실패 시 None
    """
    path = "/people/searchPeopleList.json"
    params = {
        "curPage": cur_page,
        "itemPerPage": item_per_page
    }

    if people_nm: params["peopleNm"] = people_nm
    if filmo_names: params["filmoNames"] = filmo_names

    data = _call_api(path, params)
    
    if data:
        try:
            return PeopleListResponseDTO(**data)
        except Exception as e:
            print(f"DTO 변환 중 오류 발생: {e}")
            return None
    return None

def get_company_info(company_cd: str) -> Optional[CompanyInfoResponseDTO]:
    """
    영화사 상세정보를 조회합니다.

    Args:
        company_cd (str): 영화사 고유 코드

    Returns:
        Optional[CompanyInfoResponseDTO]: 조회 성공 시 DTO 객체, 실패 시 None
    """
    path = "/company/searchCompanyInfo.json"
    params = {
        "companyCd": company_cd
    }

    data = _call_api(path, params)
    
    if data:
        try:
            return CompanyInfoResponseDTO(**data)
        except Exception as e:
            print(f"DTO 변환 중 오류 발생: {e}")
            return None
    return None

def get_company_list(company_nm: Optional[str] = None,
                     ceo_nm: Optional[str] = None,
                     company_part_cd: Optional[str] = None,
                     cur_page: str = "1",
                     item_per_page: str = "10") -> Optional[CompanyListResponseDTO]:
    """
    영화사 목록을 조회합니다.

    Args:
        company_nm (str, optional): 영화사명
        ceo_nm (str, optional): 대표자명
        company_part_cd (str, optional): 영화사 분류코드
        cur_page (str): 현재 페이지 (기본 1)
        item_per_page (str): 결과 개수 (기본 10)

    Returns:
        Optional[CompanyListResponseDTO]: 조회 성공 시 DTO 객체, 실패 시 None
    """
    path = "/company/searchCompanyList.json"
    params = {
        "curPage": cur_page,
        "itemPerPage": item_per_page
    }

    if company_nm: params["companyNm"] = company_nm
    if ceo_nm: params["ceoNm"] = ceo_nm
    if company_part_cd: params["companyPartCd"] = company_part_cd

    data = _call_api(path, params)
    
    if data:
        try:
            return CompanyListResponseDTO(**data)
        except Exception as e:
            print(f"DTO 변환 중 오류 발생: {e}")
            return None
    return None

def get_movie_info(movie_cd: str) -> Optional[MovieInfoResponseDTO]:
    """
    영화 상세정보를 조회합니다.

    Args:
        movie_cd (str): 영화 고유 코드

    Returns:
        Optional[MovieInfoResponseDTO]: 조회 성공 시 DTO 객체, 실패 시 None
    """
    path = "/movie/searchMovieInfo.json"
    params = {
        "movieCd": movie_cd
    }

    data = _call_api(path, params)
    
    if data:
        try:
            return MovieInfoResponseDTO(**data)
        except Exception as e:
            print(f"DTO 변환 중 오류 발생: {e}")
            return None
    return None

def get_movie_list(movie_nm: Optional[str] = None,
                   director_nm: Optional[str] = None,
                   open_start_dt: Optional[str] = None,
                   open_end_dt: Optional[str] = None,
                   prdt_start_year: Optional[str] = None,
                   prdt_end_year: Optional[str] = None,
                   rep_nation_cd: Optional[str] = None,
                   movie_type_cd: Optional[str] = None,
                   cur_page: str = "1",
                   item_per_page: str = "10") -> Optional[MovieListResponseDTO]:
    """
    영화 목록을 조회합니다.

    Args:
        movie_nm (str, optional): 영화명
        director_nm (str, optional): 감독명
        open_start_dt (str, optional): 개봉연도 시작 (YYYY)
        open_end_dt (str, optional): 개봉연도 종료 (YYYY)
        prdt_start_year (str, optional): 제작연도 시작 (YYYY)
        prdt_end_year (str, optional): 제작연도 종료 (YYYY)
        rep_nation_cd (str, optional): 국적코드
        movie_type_cd (str, optional): 영화유형코드
        cur_page (str): 현재 페이지 (기본 1)
        item_per_page (str): 결과 개수 (기본 10)

    Returns:
        Optional[MovieListResponseDTO]: 조회 성공 시 DTO 객체, 실패 시 None
    """
    path = "/movie/searchMovieList.json"
    params = {
        "curPage": cur_page,
        "itemPerPage": item_per_page
    }

    if movie_nm: params["movieNm"] = movie_nm
    if director_nm: params["directorNm"] = director_nm
    if open_start_dt: params["openStartDt"] = open_start_dt
    if open_end_dt: params["openEndDt"] = open_end_dt
    if prdt_start_year: params["prdtStartYear"] = prdt_start_year
    if prdt_end_year: params["prdtEndYear"] = prdt_end_year
    if rep_nation_cd: params["repNationCd"] = rep_nation_cd
    if movie_type_cd: params["movieTypeCd"] = movie_type_cd

    data = _call_api(path, params)
    
    if data:
        try:
            return MovieListResponseDTO(**data)
        except Exception as e:
            print(f"DTO 변환 중 오류 발생: {e}")
            return None
    return None

def get_common_codes(com_code: str) -> Optional[CommonCodeResponseDTO]:
    """
    공통코드 정보를 조회합니다. (지역 코드, 영화 형식 등)

    Args:
        com_code (str): 조회하고자 하는 상위 코드 (예: 지역코드 0105000000)

    Returns:
        Optional[CommonCodeResponseDTO]: 조회 성공 시 DTO 객체, 실패 시 None
    """
    path = "/code/searchCodeList.json"
    params = {
        "comCode": com_code
    }

    data = _call_api(path, params)
    
    if data:
        try:
            return CommonCodeResponseDTO(**data)
        except Exception as e:
            print(f"DTO 변환 중 오류 발생: {e}")
            return None
    return None

def get_daily_box_office(target_dt: date, 
                        item_per_page: str = "10", 
                        multi_movie_yn: Optional[str] = None, 
                        rep_nation_cd: Optional[str] = None, 
                        wide_area_cd: Optional[str] = None) -> Optional[DailyBoxOfficeResponseDTO]:
    """
    일일 박스오피스 정보를 조회합니다.

    Args:
        target_dt (date): 조회하고자 하는 날짜
        item_per_page (str): 결과 개수 (기본 10, 최대 10)
        multi_movie_yn (str, optional): 다양성 영화 여부 (Y: 다양성, N: 상업)
        rep_nation_cd (str, optional): 한국/외국 영화 구분 (K: 한국, F: 외국)
        wide_area_cd (str, optional): 상영지역별 코드

    Returns:
        Optional[DailyBoxOfficeResponseDTO]: 조회 성공 시 DTO 객체, 실패 시 None
    """
    path = "/boxoffice/searchDailyBoxOfficeList.json"
    
    # date 객체를 API 요청 형식(YYYYMMDD)으로 변환
    target_dt_str = target_dt.strftime('%Y%m%d')
    
    params = {
        "targetDt": target_dt_str,
        "itemPerPage": item_per_page
    }

    if multi_movie_yn:
        params["multiMovieYn"] = multi_movie_yn
    if rep_nation_cd:
        params["repNationCd"] = rep_nation_cd
    if wide_area_cd:
        params["wideAreaCd"] = wide_area_cd

    data = _call_api(path, params)
    
    if data:
        try:
            return DailyBoxOfficeResponseDTO(**data)
        except Exception as e:
            print(f"DTO 변환 중 오류 발생: {e}")
            return None
    return None


def _call_api(path: str, params: Dict) -> Optional[Dict]:
    """
    API를 호출하는 공통 함수입니다. 이 파일 내부에서만 사용합니다.

    Args:
        path (str): API 엔드포인트 경로 
        params (dict): 요청 파라미터 딕셔너리

    Returns:
        Optional[Dict]: 호출 성공 시 JSON 응답 데이터, 실패 시 None
    """
    # 1. URL 구성
    # URL이 '/'로 시작하지 않을 경우를 대비해 처리
    if not path.startswith('/'):
        path = '/' + path

    url = f"{settings.KOBIS_URL}{path}"

    # 2. 필수 기본 파라미터 추가
    # 서비스키는 .env에서 가져온 값을 사용하며, JSON 형식을 기본으로 요청합니다.
    api_params = params.copy()
    if 'key' not in api_params:
        api_params['key'] = settings.KOBIS_KEY

    try:
        # 3. API 호출
        response = requests.get(url, params=api_params)

        # 4. 응답 상태 확인
        response.raise_for_status()

        # 5. 데이터 반환
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"API 호출 중 오류 발생 (URL: {url}): {e}")
        return None
    except ValueError as e:
        print(f"JSON 파싱 오류: {e}")
        return None