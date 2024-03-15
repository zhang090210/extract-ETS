@echo off
pyinstaller -F -c main.py ^
    --distpath ./build ^
    --workpath ./build ^
    --clean ^
    -n ETS ^
    --add-binary "include/wkhtmltopdf.exe;include"