build:
	docker build . -t coworking_booking_bot:latest

run:
	docker run --env-file .env coworking_booking_bot