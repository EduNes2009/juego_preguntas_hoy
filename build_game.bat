@echo off
echo Limpiando rastros...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist main.spec del /q main.spec

echo Compilando juego...
python -m PyInstaller --noconfirm --onedir --windowed ^
--add-data "sounds;sounds" ^
--add-data "imagenes;imagenes" ^
--add-data "fonts;fonts" ^
--add-data "audio;audio" ^
--add-data "logic;logic" ^
--add-data "ui;ui" ^
--icon=Edu1.ico ^
main.py

echo.
echo ¡Proceso terminado! Revisá la carpeta 'dist/main'.
pause