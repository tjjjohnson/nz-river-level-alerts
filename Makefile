build-lambda:
	rm -rf build
	mkdir --parents build build/lib

	cp -r bin build/.
	pip3 install -r requirements.txt -t build

	curl -SL https://github.com/ManivannanMurugavel/selenium-python-aws-lambda/raw/master/lib/libORBit-2.so.0 > build/lib/libORBit-2.so.0
	curl -SL https://github.com/ManivannanMurugavel/selenium-python-aws-lambda/raw/master/lib/libgconf-2.so.4 > build/lib/libgconf-2.so.4


	# couldn't build everything from source so using this zip file that works in lambda
	curl -SL https://github.com/ManivannanMurugavel/selenium-python-aws-lambda/raw/master/lambda_function.zip > lambda_function.zip
	unzip -o lambda_function.zip -d build/
	rm lambda_function.zip

	cp -r src/* build/.
	cp example_alert_rules.yaml build/.
	
	rm -r build/pip build/*dist-info

	bash -c 'cd  build; zip -9qr nz-river-level-alerts.zip .'
	mv build/nz-river-level-alerts.zip .

	aws s3 cp nz-river-level-alerts.zip	 s3://river-level-alerts/

	rm -rf build

update-lambda: build-lambda
	aws lambda update-function-code --function-name river-level-alerts --s3-bucket river-level-alerts --s3-key nz-river-level-alerts.zip


