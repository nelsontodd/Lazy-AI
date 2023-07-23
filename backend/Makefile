default:
	flask run

dev:
	export FLASK_APP=app
	export FLASK_ENV=development
	flask run --reload

clamav:
	docker pull clamav/clamav
	docker run -p 3310:3310 clamav/clamav
