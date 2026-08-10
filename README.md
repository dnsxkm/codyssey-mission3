# Codyssey Mission 3 — Mini NPU Simulator

MAC(Multiply-Accumulate) 연산으로 3×3~25×25 패턴을 판별하는 Python 콘솔 시뮬레이터.

## 실행 방법
실행 후 모드 선택: `1` 사용자 입력(3×3) / `2` data.json 분석

## 진행 상황
- [x] MAC 연산 + epsilon 판정
- [x] 모드 1: 입력 검증 → MAC → 판정 → 성능 측정
- [ ] 모드 2: data.json 로드 / 라벨 정규화 / PASS·FAIL
- [ ] 결과 리포트 (FAIL 원인 분석 + O(N²) 시간 복잡도)