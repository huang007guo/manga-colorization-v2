@echo off
:: 获得管理员权限
Net session >nul 2>&1 || mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0","","runas",1)(window.close)&&exit
:: 进入conda环境
CALL conda activate manga-colorization-v2
cd C:\job\codeing\my\python\manga-colorization-v2
C:
echo "python inference.py"
python inference.py -p "J:\down\from\1,J:\down\from\2" -g -o J:\down\colorization
pause