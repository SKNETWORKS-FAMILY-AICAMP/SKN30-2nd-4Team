import os
import sys

# 실행 방식과 관계없이 프로젝트 루트 경로가 sys.path에 확실히 잡히도록 강제 보정
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# web/app.py를 import 캐싱 없이 Streamlit 메인 실행기 상에서 프레시하게 직접 구동
app_path = os.path.join(ROOT_DIR, "web", "app.py")
with open(app_path, "r", encoding="utf-8") as f:
    code = compile(f.read(), app_path, "exec")
    exec(code, globals())
