import mysql.connector
from mysql.connector import Error
from util import settings

class DBManager:
    """
    MySQL 데이터베이스 연결 및 쿼리 실행을 관리하는 매니저 클래스입니다.
    팀원들은 이 클래스를 직접 인스턴스화하기보다 아래의 'db' 객체 사용을 권장합니다.
    """
    
    def __init__(self):
        self.config = settings.DB_CONFIG
        self.connection = None

    def connect(self):
        """데이터베이스 연결을 생성합니다. 이미 연결되어 있다면 기존 연결을 반환합니다."""
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connection = mysql.connector.connect(**self.config)
            return self.connection
        except Error as e:
            print(f"MySQL 연결 오류: {e}")
            raise

    def disconnect(self):
        """데이터베이스 연결을 안전하게 종료합니다."""
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def execute_query(self, query, params=None):
        """
        데이터 변경(INSERT, UPDATE, DELETE) 쿼리를 실행합니다.
        성공 시 True, 실패 시 False를 반환합니다.
        """
        conn = self.connect()
        if not conn:
            return False
            
        cursor = conn.cursor()
        try:
            cursor.execute(query, params or ())
            conn.commit()
            return True
        except Error as e:
            print(f"쿼리 실행 오류: {e}")
            conn.rollback()
            raise
        finally:
            cursor.close()

    def execute_many(self, query, params_list, chunk_size=1000):
        """
        다량의 데이터를 한 번에 INSERT/UPDATE할 때 사용합니다. (배치 쿼리)

        Args:
            query (str): 실행할 쿼리 템플릿.
                         예) "INSERT INTO ev_data (region, ev_count) VALUES (%s, %s)"
            params_list (list[tuple]): 각 행에 해당하는 파라미터 튜플의 리스트.
                         예) [('서울', 1000), ('경기', 2000), ...]
            chunk_size (int): 한 번에 처리할 행 수. 기본값 1000.
                              데이터가 매우 많을 경우 메모리 초과를 방지합니다.

        Returns:
            int: 성공적으로 삽입된 총 행 수. 실패 시 -1 반환.

        Example:
            rows = [('서울', 83868, 1396), ('경기', 102000, 2100)]
            query = "INSERT INTO ev_stats (region, ev_count, charger_count) VALUES (%s, %s, %s)"
            inserted = db.execute_many(query, rows)
            print(f"{inserted}건 삽입 완료")
        """
        conn = self.connect()
        if not conn:
            return -1

        cursor = conn.cursor()
        total_affected = 0
        try:
            # chunk_size 단위로 나누어 처리 (대용량 데이터 안정성 확보)
            for i in range(0, len(params_list), chunk_size):
                chunk = params_list[i:i + chunk_size]
                cursor.executemany(query, chunk)
                total_affected += cursor.rowcount
            conn.commit()
            return total_affected
        except Error as e:
            print(f"배치 쿼리 실행 오류: {e}")
            conn.rollback()
            raise
        finally:
            cursor.close()

    def fetch_all(self, query, params=None):
        """
        여러 줄의 데이터를 조회(SELECT)할 때 사용합니다.
        결과를 딕셔너리 리스트([{'col1': val1, ...}, ...]) 형태로 반환합니다.
        """
        conn = self.connect()
        if not conn:
            return []
            
        cursor = conn.cursor(dictionary=True) # 컬럼명을 키로 하는 딕셔너리 반환
        try:
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"데이터 조회 오류: {e}")
            raise
        finally:
            cursor.close()

    def fetch_one(self, query, params=None):
        """단일 행의 데이터를 조회할 때 사용합니다. 딕셔너리 하나를 반환합니다."""
        conn = self.connect()
        if not conn:
            return None
            
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            result = cursor.fetchone()
            return result
        except Error as e:
            print(f"데이터 단일 조회 오류: {e}")
            raise
        finally:
            cursor.close()

    # 'with' 문 사용을 위한 컨텍스트 매니저 지원
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

# =================================================================
# 팀원 공용 DB 객체 (Single Instance)
# 사용법: from config import db
# 1. users = db.fetch_all("SELECT * FROM users")
# 2. db.execute_query("UPDATE users SET name=%s WHERE id=%s", ('Kim', 1))
# =================================================================
db = DBManager()