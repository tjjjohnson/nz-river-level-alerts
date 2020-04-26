build-lambda:
	mkdir --parents build

	#cp -r src build/.
	#cp -r bin build/.
	pip3 install -r requirements.txt -t lib

	#cd  build; zip -9qr build.zip .
	#cp build/build.zip .

	zip -9qr build/river_level_alerts_bin.zip bin/.
	zip -9qr build/river_level_alerts_lib.zip lib/.
	
	#rm -rf build

