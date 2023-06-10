main:
	pyinstaller --onefile --windowed --icon="DATA/Images/logo.ico" main.py
	pyinstaller main.spec
	mkdir "dist/Clémenc'octogonne"
	mv dist/main "dist/Clémenc'octogonne"
	cp -r DATA "dist/Clémenc'octogonne"
	@echo "done!"

OSX:
	pyinstaller --onefile --windowed --icon="DATA/Images/logo.ico" main.py
	pyinstaller main.spec
	cp -r DATA "dist/main.app"
	@echo "done!"

clean:
	rm -r build
	rm -r dist


