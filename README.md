# 여따버려(Yeottabeolyeo. YTBL)
<hr>
광진구의 의류 수거함/폐전지, 형광등 수거함을 KakaoMap API를 통해 지도로 표시하고
SNS의 포스트기능들을 구현해본 웹 어플리케이션
<br>
DEMO : https://hovak.pythonanywhere.com/ 
  (현재 Pythonanywhere에 올라가있는 앱은 YTBL2로 게시판(board)기능을 제외한 버전)
  
<hr>

### 후기

```
  Django 입문하며 만들어본 첫번째 프로젝트로 완성도가 많이 떨어지지만
  기본적인 CRUD를 구현해보았고, 더 나아가 외부 API를 가져다 써본 좋은 경험이었다.
  이전에 Java를 공부할 때 느껴보지 못한 생산성에 많이 빠진거같다.
  추가로, 여러 기능(좋아요, Django-Ajax 통신)을 구현해보기 위해 찾아보고 적용해보며 Django와 좀 더 친해지게 된 계기가 되었다!
```

<hr>

### 여따버려 Project 기능 설명

<hr>

1. 지도 관련(ytbl)
      + KakaoMap API를 통한 지도 기능 구현      
      + 구청 홈페이지에서 수거함/폐전지, 형광등 수거함의 좌표값을 얻고
      + Geocoder-Xr를 통한 지번(도로명) 주소 -> 좌표값으로 변환한 Data(CSV)를 직접 DB에 Insert
      + 전체 / 의류 수거함 / 폐전지, 형광등 수거함으로 나누어 지도에 해당 카테고리의 좌표만 출력 가능
      
2. 계정 관련(account)
  
    + Custom User Model 적용
      + User 관련
        + Create
          - 계정 생성
        + Read
          - 계정 정보 출력
        + Update
          - 계정 정보 수정(비밀번호 변경)
        + Delete
          - 계정 삭제
        
3. 게시판 관련(board)
  
    + 게시판 기본 CRUD 구현
      + Create
        + 게시글 등록
      + Read
        + 게시글 목록 출력(List)
        + 게시글 상세 출력(Detail)
      + Update
        + 게시글 수정
      + Delete
        + 게시글 삭제
      
    + 이미지 CRUD 구현
      + board 객체 삭제시 참조된 이미지(서버에 저장된)도 함께 삭제
    
    + 댓글 구현
      + 댓글 CURD 및 대댓글(무한 계층 구조) 구현

4. 소셜 포스팅 관련(social)

    + 기존 게시판 CRUD와 유사하나 비동기 처리가 많음
      + Create
        + 목록(List)에서 바로 새로운 글을 작성할 수 있음
      + Read
        + 게시글 목록 출력(List)
        + 게시글 상세 출력(Detail)
      + Update
        + 게시글 좋아요 기능
        + 게시글 수정
      + Delete
        + 게시글 삭제
        
    + 이미지 CRUD 구현
      + social 객체 삭제시 참조된 이미지(서버에 저장된)도 함께 삭제
      
    + 댓글 구현
      + 댓글 CURD 및 대댓글(무한 계층 구조) 구현
    
