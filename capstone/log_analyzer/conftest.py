"""캡스톤 채점 대상 선택. STUDY_SOLUTIONS=1 이면 모범답안을 채점한다."""

import os
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE / "_solution" if os.environ.get("STUDY_SOLUTIONS") else HERE))
