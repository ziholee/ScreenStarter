@echo off
REM ===========================
REM ScreenStarter 빌드 스크립트
REM ===========================

REM 1. 가상환경 활성화 (있으면)
IF EXIST venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM 2. pyinstaller 설치 확인
pip show pyinstaller >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [INFO] pyinstaller 설치 중...
    pip install pyinstaller
)

REM 3. 이전 빌드 삭제
echo [INFO] 이전 빌드 파일 정리 중...
rmdir /S /Q build dist
del /Q ScreenStarter.spec

REM 4. 빌드 실행
echo [INFO] ScreenStarter.exe 빌드 시작...
pyinstaller --noconsole --onefile --icon=app.ico ScreenStarter.py

REM 5. 빌드 결과 확인
IF EXIST dist\ScreenStarter.exe (
    echo [SUCCESS] 빌드 완료: dist\ScreenStarter.exe
) ELSE (
    echo [ERROR] 빌드 실패
)

pause
