@echo off

pyinstaller PeYx2.spec
echo Build complete

.\dist\PeYx2\PeYx2.exe
echo Test complete

pause