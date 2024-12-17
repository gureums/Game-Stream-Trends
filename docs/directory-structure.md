# Data Structure

- **.github/**: GitHub과 관련된 파일을 포함
  - **ISSUE_TEMPLATE/**: GitHub 이슈 생성을 위한 템플릿이 포함된 폴더
  - **workflows/**: 지속적인 통합 및 배포(CI/CD)를 위한 GitHub Actions 워크플로 파일들이 포함된 폴더

---
 
- **dags/**: Airflow의 DAG 파일들이 저장된 폴더. 워크플로의 스케줄링 및 실행을 정의

---
 
- **data/**: 로컬 환경에서 작업하는 동안 데이터를 처리하고 저장하는 곳 (raw data, processed data, ...)
  - **raw/**: API를 통해 수집된 raw data가 저장됨
  - **processed/**: processed data가 저장됨

---

- **scripts/**: 반복적인 작업을 수행하는 스크립트들이 위치하는 폴더 (데이터를 수집하거나 배치 작업을 자동화하는 스크립트가 포함)
  - **data_collection/**: API에서 원시 데이터를 수집하는 스크립트가 포함된 폴더
  - **data_processing/**: 수집된 데이터를 변환하거나 처리하는 스크립트가 포함된 폴더

---

- **src/**: 프로젝트의 핵심 애플리케이션 코드가 포함된 폴더 (서비스나 애플리케이션의 주된 동작을 담당)

---

- **docs/**: 프로젝트 문서 폴더로, 설정 가이드, API 문서 등 프로젝트와 관련된 문서가 포함된 폴더

---

- **terraform/**: AWS 리소스 프로비저닝 및 관리를 위한 인프라 코드(IaC)가 포함된 폴더