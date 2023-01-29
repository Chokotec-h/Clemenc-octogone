pyinstaller --onefile --windowed --icon="DATA/Images/logo.ico" main.py
pyinstaller main.spec
mkdir "dist/Clémenc'octogonne"
mv dist/* "dist/Clémenc'octogonne"
cp -r DATA "dist/Clémenc'octogonne"
