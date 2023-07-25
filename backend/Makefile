default:
	flask run

dev:
	export FLASK_APP=app
	export FLASK_ENV=development
	flask run --reload

pull-clamav:
	docker pull clamav/clamav

run-clamav:
	docker run -p 3310:3310 clamav/clamav

first-time-clamav: pull-clamav run-clamav
