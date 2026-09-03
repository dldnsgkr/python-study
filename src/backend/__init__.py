"""트랙 B · 백엔드 — pydantic · FastAPI · SQLAlchemy 2.0 · 운영.

  b1_pydantic.py    B1  타입 힌트를 런타임 계약으로
  b2_fastapi.py     B2  타입이 곧 API 스펙
  b3_sqlalchemy.py  B3  선언적 모델 · N+1 · 락 · 리포지터리
  b4_ops.py         B4  구조화 로깅 · trace_id · graceful shutdown

먼저 의존성을 설치하세요:  uv sync --group backend
채점:                      ./study backend
"""
