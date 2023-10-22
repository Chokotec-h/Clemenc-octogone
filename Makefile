OS := $(shell uname)

main:
	pyinstaller --onefile --windowed --icon="DATA/Images/logo.ico" main.py
	pyinstaller main.spec
	mkdir "dist/Clémenc'octogonne"
	mv dist/main "dist/Clémenc'octogonne"
	cp -r DATA "dist/Clémenc'octogonne"
ifeq ($(OS), Darwin) # Copy data in the MacOS App file
	cp -r "dist/Clémenc'octogonne/DATA" "dist/main.app/Contents/MacOS/DATA"
endif

clean:
	rm -r build
	rm -r dist


