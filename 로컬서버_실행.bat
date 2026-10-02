@echo off
cd /d "%~dp0"
title 6차시 탈출 게임 - 로컬 서버

echo.
echo  ================================================
echo    6차시 탈출 게임(그림그래프) : 로컬 서버 (예비 방법)
echo  ================================================
echo.

where python >nul 2>nul
if errorlevel 1 goto TRYPY
python -c "pass" >nul 2>nul
if not errorlevel 1 goto RUNPY

:TRYPY
where py >nul 2>nul
if errorlevel 1 goto NOPY
py -c "pass" >nul 2>nul
if not errorlevel 1 goto RUNPY2

:NOPY
echo  [안내] 이 컴퓨터에서는 파이썬이 실행되지 않습니다.
echo.
echo         보통은 GitHub 주소(review-escape-6)로 접속하면 됩니다.
echo         그 주소도 안 되면, 이 폴더를 모둠 기기마다 복사해서
echo         index.html 을 더블클릭하세요.
echo.
pause
exit /b 1

:RUNPY
python server.py
goto ENDED

:RUNPY2
py server.py
goto ENDED

:ENDED
echo.
echo  서버가 종료되었습니다. 아무 키나 누르면 창이 닫힙니다.
pause >nul