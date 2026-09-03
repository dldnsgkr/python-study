"""자유 실험장.

여기서는 뭘 해도 됩니다. 채점 대상이 아닙니다.
문서를 읽다가 "이거 진짜 그런가?" 싶을 때 바로 찍어 보는 곳입니다.

    ../study repl        # src/ 를 임포트한 상태의 REPL
    .venv/bin/python playground/scratch.py
"""

import dis

# 예: DRILL 00 의 2번 — 왜 바이트코드 길이가 다를까?
print("=== x + 1 ===")
dis.dis(lambda x: x + 1)

print("=== x.__add__(1) ===")
dis.dis(lambda x: x.__add__(1))
