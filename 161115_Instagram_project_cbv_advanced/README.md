# 인스타그램 서비스 설계

## 새로운 로그인 뷰

**FBV**  
def login_fbv(request) 로 작성해주세요

- views.py에 View작성
	- pass처리 후 form - urls - view를 미리 연결 한 후 나중에 로직을 작성하세요
	- request.method == 'GET'일 경우, context에 form을 포함하여 render
	- request.method == 'POST'일 경우, form의 validation후 Login처리
- forms.py에 LoginForm(forms.Form) 작성
	- username, password필드 가짐
- urls모듈 생성, views모듈을 하위요소로 둠
	- urls/views.py
- View와 urls연결
- Template작성
	- member/login.html에 작성

	
**CBV**  
class LoginFormView(FormView) 로  작성해주세요

## Git 협업을 위한 브랜치 관리

- 1명이 dev branch생성 후 push
	- git push origin dev
- 다른사람들은 dev branch를 추적
	- `git checkout --track origin/dev`
- dev branch로 checkout
	- `git checkout dev`
- dev branch를 기준으로 새 branch 생성
	- `git branch <new branch name>`
- 새 branch로 checkout
	- `git checkout <new branch name>`
		- 위 2명령어는 `git checkout -b <new branch name>`로 사용가능
- 새 branch에서 작업 완료 후, 저장소에 push
	- `git push origin <new branch name>`
- 해당 branch를 pull request처리
- pull request완료되면, 리모트에서 자신의 branch 삭제
	- `git push origin --delete <new branch name>`


## 다른사람의 branch 테스트

아래 명령어로 origin저장소의 변경점을 로컬에 적용

```
git fetch origin
```

이후

```
 git checkout --track origin/<new branch name>
```

## 협업을 위한 새로운 기능들

아래 기능을 각자 branch나눠서 만든 후, branch를 push 후 pull request생성

1. Signup
2. Photo delete
3. Logout

