# Webtoon Crawling

### 1. 각 웹페이지별 스크랩 코드 완성하기
- [x] naver
- [x] kakao
- [x] lezhin
- [x] toptoon

### 2. 각 스크랩 코드 모듈화 하기
+ 작가(creator)도 스크랩해오기 기능 추가
  + 총 컬럼: 수집날짜, 요일, 순위, 웹툰제목, 웹툰작가, 웹툰링크, 썸넬링크
- [ ] kakao: 성인작품 스크랩하기 어려운 문제 발생
- [x] naver
- [x] lezhin
- [x] toptoon
- [x] toomics
- [ ] ridi: 주간 순위 없어 생략

실행 명령어
```
python scrap_webtoon.py -d <도메인명>
python scrap_webtoon.py -d naver
```