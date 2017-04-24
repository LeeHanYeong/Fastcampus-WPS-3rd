# 로그인/회원가입 구현

- member 애플리케이션 생성
- MyUser 모델 구현
	- AbstractUser를 상속
- POST요청을 받아서 회원을 만들어주는 View구현 (GET요청이 왔을때는 Form이 있는 Template을 보여줌)
	- username, password, nickname을 보내주는 Form이 있는 Template구현
	- 버튼눌러서 회원생성 (UserManager의 create_user) 테스트
- POST요청이 왔을 때 JSON으로 리턴해주는 View구현
	- request.POST의 데이터만 받아서 회원가입을 해주고 `json.dumps`함수를 사용해서 '잘 됐다'정도의 결과 또는 유저정보만 리턴
	- Postman에서 테스트
- DRF에서 구현
	- UserSerializer를 만듬 (ModelSerializer)
	- APIView를 상속받은 SignupAPIView클래스 구현
	- 구현한 클래스를 .as_view()로 urls.py에 등록
	- Postman에서 테스트