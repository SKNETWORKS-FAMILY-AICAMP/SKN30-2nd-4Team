from pydantic import BaseModel, Field
from typing import List, Optional

class DailyBoxOfficeDTO(BaseModel):
    """
    일별 박스오피스 리스트의 개별 영화 정보 DTO
    """
    rnum: int = Field(..., description="순번")
    """순번"""
    rank: int = Field(..., description="해당일자의 박스오피스 순위")
    """해당일자의 박스오피스 순위"""
    rankInten: int = Field(..., description="전일대비 순위의 증감분")
    """전일대비 순위의 증감분"""
    rankOldAndNew: str = Field(..., description="랭킹 신규진입 여부 (OLD/NEW)")
    """랭킹 신규진입 여부 (OLD/NEW)"""
    movieCd: str = Field(..., description="영화의 대표코드")
    """영화의 대표코드"""
    movieNm: str = Field(..., description="영화명(국문)")
    """영화명(국문)"""
    openDt: str = Field(..., description="영화의 개봉일")
    """영화의 개봉일"""
    salesAmt: int = Field(..., description="해당일의 매출액")
    """해당일의 매출액"""
    salesShare: float = Field(..., description="해당일자 매출총액 대비 해당 영화의 매출비율")
    """해당일자 매출총액 대비 해당 영화의 매출비율"""
    salesInten: int = Field(..., description="전일 대비 매출액 증감분")
    """전일 대비 매출액 증감분"""
    salesChange: float = Field(..., description="전일 대비 매출액 증감 비율")
    """전일 대비 매출액 증감 비율"""
    salesAcc: int = Field(..., description="누적매출액")
    """누적매출액"""
    audiCnt: int = Field(..., description="해당일의 관객수")
    """해당일의 관객수"""
    audiInten: int = Field(..., description="전일 대비 관객수 증감분")
    """전일 대비 관객수 증감분"""
    audiChange: float = Field(..., description="전일 대비 관객수 증감 비율")
    """전일 대비 관객수 증감 비율"""
    audiAcc: int = Field(..., description="누적관객수")
    """누적관객수"""
    scrnCnt: int = Field(..., description="해당일자에 상영한 스크린수")
    """해당일자에 상영한 스크린수"""
    showCnt: int = Field(..., description="해당일자에 상영된 횟수")
    """해당일자에 상영된 횟수"""

class BoxOfficeResultDTO(BaseModel):
    """
    박스오피스 결과 정보 DTO
    """
    boxofficeType: str = Field(..., description="박스오피스 종류")
    """박스오피스 종류"""
    showRange: str = Field(..., description="박스오피스 조회 일자")
    """박스오피스 조회 일자"""
    dailyBoxOfficeList: List[DailyBoxOfficeDTO] = Field(..., description="일별 박스오피스 리스트")
    """일별 박스오피스 리스트"""

class DailyBoxOfficeResponseDTO(BaseModel):
    """
    일별 박스오피스 API 전체 응답 DTO
    """
    boxOfficeResult: BoxOfficeResultDTO
    """박스오피스 결과 정보"""

class CommonCodeDTO(BaseModel):
    """
    공통코드 정보 DTO
    """
    fullCd: str = Field(..., description="해당 코드의 전체 코드")
    """해당 코드의 전체 코드"""
    korNm: str = Field(..., description="해당 코드의 국문명")
    """해당 코드의 국문명"""
    engNm: str = Field(..., description="해당 코드의 영문명")
    """해당 코드의 영문명"""

class CommonCodeResponseDTO(BaseModel):
    """
    공통코드 조회 API 전체 응답 DTO
    """
    codes: List[CommonCodeDTO] = Field(..., description="공통코드 리스트")
    """공통코드 리스트"""

class MovieListDirectorDTO(BaseModel):
    """
    영화목록 내 감독 정보 DTO
    """
    peopleNm: str = Field(..., description="영화감독명")
    """영화감독명"""

class MovieListCompanyDTO(BaseModel):
    """
    영화목록 내 제작사 정보 DTO
    """
    companyCd: str = Field(..., description="제작사 코드")
    """제작사 코드"""
    companyNm: str = Field(..., description="제작사명")
    """제작사명"""

class MovieListDTO(BaseModel):
    """
    영화목록 정보 DTO
    """
    movieCd: str = Field(..., description="영화코드")
    """영화코드"""
    movieNm: str = Field(..., description="영화명(국문)")
    """영화명(국문)"""
    movieNmEn: str = Field(..., description="영화명(영문)")
    """영화명(영문)"""
    prdtYear: str = Field(..., description="제작연도")
    """제작연도"""
    openDt: str = Field(..., description="개봉일")
    """개봉일"""
    typeNm: str = Field(..., description="영화유형")
    """영화유형"""
    prdtStatNm: str = Field(..., description="제작상태")
    """제작상태"""
    nationAlt: str = Field(..., description="제작국가(전체)")
    """제작국가(전체)"""
    genreAlt: str = Field(..., description="영화장르(전체)")
    """영화장르(전체)"""
    repNationNm: str = Field(..., description="대표 제작국가명")
    """대표 제작국가명"""
    repGenreNm: str = Field(..., description="대표 장르명")
    """대표 장르명"""
    directors: List[MovieListDirectorDTO] = Field(..., description="영화감독 정보")
    """영화감독 정보"""
    companys: List[MovieListCompanyDTO] = Field(..., description="제작사 정보")
    """제작사 정보"""

class MovieListResultDTO(BaseModel):
    """
    영화목록 결과 정보 DTO
    """
    totCnt: int = Field(..., description="총 검색 결과 수")
    """총 검색 결과 수"""
    movieList: List[MovieListDTO] = Field(..., description="영화 목록")
    """영화 목록"""
    source: Optional[str] = Field(None, description="데이터 출처")
    """데이터 출처"""

class MovieListResponseDTO(BaseModel):
    """
    영화목록 조회 API 전체 응답 DTO
    """
    movieListResult: MovieListResultDTO = Field(..., description="영화목록 결과")
    """영화목록 결과"""

class MovieInfoNationDTO(BaseModel):
    """
    영화 상세정보 내 제작국가 DTO
    """
    nationNm: str = Field(..., description="제작국가명")
    """제작국가명"""

class MovieInfoGenreDTO(BaseModel):
    """
    영화 상세정보 내 장르 DTO
    """
    genreNm: str = Field(..., description="장르명")
    """장르명"""

class MovieInfoDirectorDTO(BaseModel):
    """
    영화 상세정보 내 감독 DTO
    """
    peopleNm: str = Field(..., description="감독명")
    """감독명"""
    peopleNmEn: Optional[str] = Field(None, description="감독명(영문)")
    """감독명(영문)"""

class MovieInfoActorDTO(BaseModel):
    """
    영화 상세정보 내 배우 DTO
    """
    peopleNm: str = Field(..., description="배우명")
    """배우명"""
    peopleNmEn: Optional[str] = Field(None, description="배우명(영문)")
    """배우명(영문)"""
    cast: str = Field(..., description="배역명")
    """배역명"""
    castEn: Optional[str] = Field(None, description="배역명(영문)")
    """배역명(영문)"""

class MovieInfoShowTypeDTO(BaseModel):
    """
    영화 상세정보 내 상영형태 DTO
    """
    showTypeGroupNm: str = Field(..., description="상영형태 그룹명")
    """상영형태 그룹명"""
    showTypeNm: str = Field(..., description="상영형태명")
    """상영형태명"""

class MovieInfoAuditDTO(BaseModel):
    """
    영화 상세정보 내 심의정보 DTO
    """
    auditNo: str = Field(..., description="심의번호")
    """심의번호"""
    watchGradeNm: str = Field(..., description="관람등급명")
    """관람등급명"""

class MovieInfoCompanyDTO(BaseModel):
    """
    영화 상세정보 내 참여 영화사 DTO
    """
    companyCd: str = Field(..., description="영화사 코드")
    """영화사 코드"""
    companyNm: str = Field(..., description="영화사명")
    """영화사명"""
    companyNmEn: Optional[str] = Field(None, description="영화사명(영문)")
    """영화사명(영문)"""
    companyPartNm: str = Field(..., description="참여 분야(제작사/배급사 등)")
    """참여 분야(제작사/배급사 등)"""

class MovieInfoDTO(BaseModel):
    """
    영화 상세정보 DTO
    """
    movieCd: str = Field(..., description="영화코드")
    """영화코드"""
    movieNm: str = Field(..., description="영화명(국문)")
    """영화명(국문)"""
    movieNmEn: Optional[str] = Field(None, description="영화명(영문)")
    """영화명(영문)"""
    movieNmOg: Optional[str] = Field(None, description="영화명(원문)")
    """영화명(원문)"""
    showTm: str = Field(..., description="상영시간(분)")
    """상영시간(분)"""
    prdtYear: str = Field(..., description="제작연도")
    """제작연도"""
    openDt: str = Field(..., description="개봉연도")
    """개봉연도"""
    prdtStatNm: str = Field(..., description="제작상태")
    """제작상태"""
    typeNm: str = Field(..., description="영화유형")
    """영화유형"""
    nations: List[MovieInfoNationDTO] = Field(..., description="제작국가 정보")
    """제작국가 정보"""
    genres: List[MovieInfoGenreDTO] = Field(..., description="장르 정보")
    """장르 정보"""
    directors: List[MovieInfoDirectorDTO] = Field(..., description="감독 정보")
    """감독 정보"""
    actors: List[MovieInfoActorDTO] = Field(..., description="배우 정보")
    """배우 정보"""
    showTypes: List[MovieInfoShowTypeDTO] = Field(..., description="상영형태 정보")
    """상영형태 정보"""
    companys: List[MovieInfoCompanyDTO] = Field(..., description="참여 영화사 정보")
    """참여 영화사 정보"""
    audits: List[MovieInfoAuditDTO] = Field(..., description="심의 정보")
    """심의 정보"""

class MovieInfoResultDTO(BaseModel):
    """
    영화 상세정보 결과 정보 DTO
    """
    movieInfo: MovieInfoDTO = Field(..., description="영화 상세정보")
    """영화 상세정보"""
    source: Optional[str] = Field(None, description="데이터 출처")
    """데이터 출처"""

class MovieInfoResponseDTO(BaseModel):
    """
    영화 상세정보 조회 API 전체 응답 DTO
    """
    movieInfoResult: MovieInfoResultDTO = Field(..., description="영화 상세정보 결과")
    """영화 상세정보 결과"""

class CompanyListDTO(BaseModel):
    """
    영화사 목록 정보 DTO
    """
    companyCd: str = Field(..., description="영화사 코드")
    """영화사 코드"""
    companyNm: str = Field(..., description="영화사명")
    """영화사명"""
    companyNmEn: Optional[str] = Field(None, description="영화사명(영문)")
    """영화사명(영문)"""
    companyPartNames: str = Field(..., description="영화사 분류(제작사, 배급사 등)")
    """영화사 분류(제작사, 배급사 등)"""
    ceoNm: Optional[str] = Field(None, description="대표자명")
    """대표자명"""
    filmoNames: Optional[str] = Field(None, description="주요 필모그래피 리스트")
    """주요 필모그래피 리스트"""

class CompanyListResultDTO(BaseModel):
    """
    영화사 목록 결과 정보 DTO
    """
    totCnt: int = Field(..., description="총 검색 결과 수")
    """총 검색 결과 수"""
    companyList: List[CompanyListDTO] = Field(..., description="영화사 목록")
    """영화사 목록"""
    source: Optional[str] = Field(None, description="데이터 출처")
    """데이터 출처"""

class CompanyListResponseDTO(BaseModel):
    """
    영화사 목록 조회 API 전체 응답 DTO
    """
    companyListResult: CompanyListResultDTO = Field(..., description="영화사 목록 결과")
    """영화사 목록 결과"""

class CompanyInfoPartDTO(BaseModel):
    """
    영화사 상세정보 내 분류 정보 DTO
    """
    companyPartNm: str = Field(..., description="영화사 분류명")
    """영화사 분류명"""

class CompanyInfoFilmoDTO(BaseModel):
    """
    영화사 상세정보 내 필모그래피 정보 DTO
    """
    movieCd: str = Field(..., description="영화코드")
    """영화코드"""
    movieNm: str = Field(..., description="영화명")
    """영화명"""
    companyPartNm: str = Field(..., description="참여 분야")
    """참여 분야"""

class CompanyInfoDTO(BaseModel):
    """
    영화사 상세정보 DTO
    """
    companyCd: str = Field(..., description="영화사 코드")
    """영화사 코드"""
    companyNm: str = Field(..., description="영화사명(국문)")
    """영화사명(국문)"""
    companyNmEn: Optional[str] = Field(None, description="영화사명(영문)")
    """영화사명(영문)"""
    ceoNm: Optional[str] = Field(None, description="대표자명")
    """대표자명"""
    parts: List[CompanyInfoPartDTO] = Field(..., description="영화사 분류 정보")
    """영화사 분류 정보"""
    filmos: List[CompanyInfoFilmoDTO] = Field(..., description="참여 영화 필모그래피")
    """참여 영화 필모그래피"""

class CompanyInfoResultDTO(BaseModel):
    """
    영화사 상세정보 결과 정보 DTO
    """
    companyInfo: CompanyInfoDTO = Field(..., description="영화사 상세정보")
    """영화사 상세정보"""
    source: Optional[str] = Field(None, description="데이터 출처")
    """데이터 출처"""

class CompanyInfoResponseDTO(BaseModel):
    """
    영화사 상세정보 조회 API 전체 응답 DTO
    """
    companyInfoResult: CompanyInfoResultDTO = Field(..., description="영화사 상세정보 결과")
    """영화사 상세정보 결과"""

class PeopleListDTO(BaseModel):
    """
    영화인 목록 정보 DTO
    """
    peopleCd: str = Field(..., description="영화인 코드")
    """영화인 코드"""
    peopleNm: str = Field(..., description="영화인명")
    """영화인명"""
    peopleNmEn: Optional[str] = Field(None, description="영화인명(영문)")
    """영화인명(영문)"""
    repRoleNm: Optional[str] = Field(None, description="주 활동 분야")
    """주 활동 분야"""
    filmoNames: Optional[str] = Field(None, description="필모리스트")
    """필모리스트"""

class PeopleListResultDTO(BaseModel):
    """
    영화인 목록 결과 정보 DTO
    """
    totCnt: int = Field(..., description="총 검색 결과 수")
    """총 검색 결과 수"""
    peopleList: List[PeopleListDTO] = Field(..., description="영화인 목록")
    """영화인 목록"""
    source: Optional[str] = Field(None, description="데이터 출처")
    """데이터 출처"""

class PeopleListResponseDTO(BaseModel):
    """
    영화인 목록 조회 API 전체 응답 DTO
    """
    peopleListResult: PeopleListResultDTO = Field(..., description="영화인 목록 결과")
    """영화인 목록 결과"""

class PeopleInfoFilmoDTO(BaseModel):
    """
    영화인 상세정보 내 필모그래피 정보 DTO
    """
    movieCd: str = Field(..., description="참여 영화 코드")
    """참여 영화 코드"""
    movieNm: str = Field(..., description="참여 영화명")
    """참여 영화명"""
    moviePartNm: str = Field(..., description="참여 분야")
    """참여 분야"""

class PeopleInfoDTO(BaseModel):
    """
    영화인 상세정보 DTO
    """
    peopleCd: str = Field(..., description="영화인 코드")
    """영화인 코드"""
    peopleNm: str = Field(..., description="영화인명(국문)")
    """영화인명(국문)"""
    peopleNmEn: Optional[str] = Field(None, description="영화인명(영문)")
    """영화인명(영문)"""
    sex: Optional[str] = Field(None, description="성별")
    """성별"""
    repRoleNm: Optional[str] = Field(None, description="영화인 분류명")
    """영화인 분류명"""
    filmos: List[PeopleInfoFilmoDTO] = Field(..., description="참여 영화 필모그래피")
    """참여 영화 필모그래피"""
    homepages: List[str] = Field(default_factory=list, description="관련 URL")
    """관련 URL"""

class PeopleInfoResultDTO(BaseModel):
    """
    영화인 상세정보 결과 정보 DTO
    """
    peopleInfo: PeopleInfoDTO = Field(..., description="영화인 상세정보")
    """영화인 상세정보"""
    source: Optional[str] = Field(None, description="데이터 출처")
    """데이터 출처"""

class PeopleInfoResponseDTO(BaseModel):
    """
    영화인 상세정보 조회 API 전체 응답 DTO
    """
    peopleInfoResult: PeopleInfoResultDTO = Field(..., description="영화인 상세정보 결과")
    """영화인 상세정보 결과"""


