# git 기본설정

[Git 최초 설정](https://git-scm.com/book/ko/v2/%EC%8B%9C%EC%9E%91%ED%95%98%EA%B8%B0-Git-%EC%B5%9C%EC%B4%88-%EC%84%A4%EC%A0%95)

```
git config --global user.name "John Doe"
git config --global user.email johndoe@example.com
git config --global core.editor vim
```
# gitignore

**Github Python gitignore**  
<https://github.com/github/gitignore/blob/master/Python.gitignore>

**Pycharm gitignore**  
<https://github.com/github/gitignore/blob/master/Global/JetBrains.gitignore>

- mysite-project
	- django_app
		- app1
		- app2
		- app3

---

# Linux vim설정

```
sudo apt-get update
sudo apt-get install vim
vim ~/.vimrc
```

아래내용 입력

```
set number            " 줄 번호 표시
set tabstop=4         " tab을 4칸으로
set ignorecase      " 검색시 대소문자 구별하지 않음
set hlsearch         " 검색시 하이라이트
set fileencodings=utf-8,euc-kr    " 파일인코딩 형식
set bs=indent,eol,start    " backspace 키 사용
set ruler              " 상태표시줄 커서 위치 표시
set title               " 제목 표시
set showmatch    " 매칭되는 괄호 표시
set nowrap         " 자동 줄바꿈 해제
set wmnu           " tab 자동완성시 가능한 목록 표시

syntax on        " 문법 하이라이트
```