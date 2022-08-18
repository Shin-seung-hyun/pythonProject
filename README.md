# pythonProject
WebCrawling

[ 영어 구두점 복원기 학습 데이터 생성을 위한 문장단위 분절 자동화 툴 개발 ]

오픈소스: xashru/punctuation-restoration 

프렌즈, 모던패밀리 전 시즌 활용하여 1차 학습 데이터 생성 완료


1. 일반 회화에 가까운 미드 스크립트 수집  
2. 특수문자 등 불필요한 요소 정제  
  a. quotation mark 삭제  
  b. 단어로 볼 수 있는 구조 내 '-' 삭제 (eg. week-end)  
  c. 문장 종결 ‘…'은 ‘.’로 치환, 문장 내 '…’은 space  
  d. It's 7:05 → 실제 시간을 뭐라고 읽는지 알아야겠지만 일단 저대로 둠  
  e. o'clock → 이대로 둠  
3. 토큰 단위로 분리 후 태크 부착(tag: O, PERIOD, COMMA, QUESTION)  
  \s -> \tO\n #어절 new line  
  \,\tO -> \tCOMMA #, replace  
  \.\tO -> \tPERIOD #. replace  
  \?\tO -> \tQUESTION #? replace  
  ‘s\tO -> \tO\n's\tO #'s 분리  
  're\tO -> \tO\n're\tO #'re 분리  
  'm\tO -> \tO\n'm\tO #'m 분리  
  'll\tO -> \tO\n'll\tO #'ll 분리  
  n't\tO -> \tO\nn't\tO # n’t 분리  
  미분리 토큰: 've, 'd …  
  
→ 총 107개 영문드라마 스크립트 raw 데이터 수집 후 정제하여 13만KB의 학습데이터 생성, 2천6백만개의 Tag부착 완료.

