default:
	flask run

dev:
	export FLASK_APP=app
	export FLASK_ENV=development
	flask run --reload

pull-clamav:
	sudo docker pull clamav/clamav

run-clamav:
	sudo docker run -d -p 3310:3310 clamav/clamav

first-time-clamav: pull-clamav run-clamav
