#!/bin/bash

# 기본 설정
IS_DOCKER=false
CONTAINER_NAME="my_mysql"
STEP=""

# 1. 인자 처리 (옵션 추가)
for arg in "$@"; do
    case $arg in
        --is_docker=*)
            IS_DOCKER="${arg#*=}"
            shift
            ;;
        --step=*)
            STEP="${arg#*=}"
            shift
            ;;
        *)
            ;;
    esac
done

# 2. .env 파일에서 환경 변수 로드
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo "❌ .env 파일을 찾을 수 없습니다."
    exit 1
fi

MIGRATE_DIR="./data/db/migrate"

# 3. 실행 대상 파일 결정
if [ -n "$STEP" ]; then
    # 특정 번호가 지정된 경우 해당 번호로 시작하는 파일만 선택
    FILES=$(ls $MIGRATE_DIR/$STEP.*.sql 2>/dev/null)
    if [ -z "$FILES" ]; then
        echo "❌ 지정한 단계($STEP)에 해당하는 SQL 파일을 찾을 수 없습니다."
        exit 1
    fi
    echo "🚀 마이그레이션을 시작합니다... (대상: $STEP번 파일, Docker: $IS_DOCKER)"
else
    # 지정되지 않은 경우 전체 파일 선택
    FILES=$(ls $MIGRATE_DIR/*.sql | sort)
    echo "🚀 마이그레이션을 시작합니다... (대상: 전체 파일, Docker: $IS_DOCKER)"
fi

# 4. SQL 파일 실행 루프
for sql_file in $FILES; do
    echo "📖 실행 중: $(basename $sql_file)..."
    
    if [ "$IS_DOCKER" = "true" ]; then
        # Docker 환경: 컨테이너 내부의 mysql 명령어 사용
        cat "$sql_file" | docker exec -i $CONTAINER_NAME mysql -u$DB_USER -p$DB_PASSWORD $DB_NAME
    else
        # 로컬 환경: 로컬 시스템의 mysql 명령어 사용
        MYSQL_PWD=$DB_PASSWORD mysql -h $DB_HOST -P ${DB_PORT:-3306} -u $DB_USER $DB_NAME < "$sql_file"
    fi
    
    if [ $? -eq 0 ]; then
        echo "✅ 완료: $(basename $sql_file)"
    else
        echo "❌ 오류 발생: $(basename $sql_file) 실행 중 중단되었습니다."
        exit 1
    fi
done

echo "🎉 모든 마이그레이션이 성공적으로 완료되었습니다!"