@echo off
echo 正在安装依赖...
pip install -r requirements.txt

echo 正在打包程序...
pyinstaller --onefile --windowed --name "解析力检测工具" main.py

echo 打包完成！
pause