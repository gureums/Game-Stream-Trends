# Git Guidelines

## Branch 전략
- **`main`**: 항상 배포 가능한 상태 유지
- **`develop`**: 기능 개발 및 테스트가 이루어지는 브랜치
- **`feature/기능이름`**: 새로운 기능 개발 시 `develop` 브랜치에서 분기
  
## Merge 전략
1. `feature/기능이름` 브랜치에서 기능을 개발한 후, **`develop`** 브랜치로 merge
2. `develop` 브랜치에서 기능을 충분히 테스트 후, **`main`** 브랜치로 merge하여 배포
3. main 브랜치로의 merge는 Pull Request을 통해 이루어짐
4. PR 리뷰 후, 코드가 승인되면 merge

## 커밋 메시지 규칙
- **`feat:`** 새로운 기능 추가
- **`fix:`** 버그 수정
- **`docs:`** 문서 수정
- **`style:`** 코드 스타일 관련 변경 (공백, 세미콜론 등)
- **`refactor:`** 코드 리팩토링
- **`test:`** 테스트 추가/수정

### 예시 커밋 메시지:
- `feat: add API data collection script`
- `fix: resolve issue with data processing pipeline`