# B4 · 운영 — 설정·로깅·배포

`12-factor · 구조화 로깅 · 컨테이너`

## 설정 계층

우선순위는 **CLI 인자 > 환경변수 > .env 파일 > 기본값**. 비밀값은 코드·이미지에 절대 넣지 않고 환경변수나 시크릿 매니저로 주입합니다. B1의 `BaseSettings`가 이 순서를 그대로 구현합니다.

*구조화 로깅*

```text
import logging, json, sys

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        payload.update(getattr(record, "extra_fields", {}))
        return json.dumps(payload, ensure_ascii=False)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JsonFormatter())
logging.basicConfig(level=logging.INFO, handlers=[handler])

logger.info("주문 생성", extra={"extra_fields": {"order_id": 1, "trace_id": tid}})
```

**💡 요청 추적**

요청마다 `trace_id`를 만들어 `contextvars.ContextVar`에 넣으면, 비동기 태스크 경계를 넘어도 같은 값이 따라갑니다(스레드로컬의 async 버전). 로그 필터에서 이 값을 자동으로 붙이면 요청 단위 추적이 완성됩니다.

*Dockerfile*

```docker
FROM python:3.12-slim AS base
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install --no-cache-dir uv && uv sync --frozen --no-dev

COPY src/ ./src/
USER 1000
CMD ["uv", "run", "uvicorn", "myapp.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

| 항목 | 권장 |
| --- | --- |
| 서버 | uvicorn (ASGI). 프로세스 관리가 필요하면 gunicorn + uvicorn 워커 |
| 워커 수 | CPU 바운드면 코어 수, I/O 바운드면 그보다 적게 + 비동기로 처리 |
| 헬스체크 | `/healthz`(프로세스 생존)와 `/readyz`(DB 연결 등) 분리 |
| 종료 | SIGTERM 수신 시 진행 중 요청을 마치고 종료(graceful shutdown) |
| 마이그레이션 | 앱 부팅이 아니라 **별도 잡**으로 실행 — 다중 인스턴스 경쟁 방지 |

### 🏋 DRILL B4 — 운영

1. JSON 로그 포매터에 `contextvars` 기반 `trace_id` 자동 주입을 붙이세요.
2. 미들웨어로 요청 처리 시간과 상태 코드를 남기고, 느린 요청(>1초)만 WARNING으로 기록하세요.
3. SIGTERM을 받으면 새 요청을 거부하고 진행 중 작업을 마치는 종료 로직을 구현해 `docker stop`으로 검증하세요.
4. 이미지를 멀티스테이지로 최적화해 최종 크기를 절반 이하로 줄여 보세요.
