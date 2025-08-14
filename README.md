# Selenium 테스트 자동화 포트폴리오

**QA Engineer: 윤도현 (Dohyeon Yun)**

## 프로젝트 개요
Selenium + Pytest를 활용한 웹 UI 테스트 자동화 프레임워크  
Page Object Model 패턴 적용으로 유지보수성과 재사용성 확보

## 빠른 실행 방법

### Google Colab에서 실행
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Yundo37/automation-portfolio-Yundo/blob/main/Test%20Automation-Yundo.ipynb)

### 로컬 환경에서 실행
```bash
git clone https://github.com/Yundo37/automation-portfolio-Yundo.git
cd automation-portfolio-Yundo
pip install -r requirements.txt
pytest tests/ --html=reports/report.html --self-contained-html -v
```

## 주요 기능
- **E2E 테스트**: 전체 주문 프로세스 검증
- **폼 테스트**: 파라미터화된 데이터 검증 + 의도적 실패 케이스
- **자동 스크린샷**: 테스트 실패 시 자동 캡처
- **HTML 리포트**: 브라우저에서 확인 가능한 상세 결과

## 연락처
- **Email**: porore37@naver.com
- **Phone**: +82 10 5652 3436
