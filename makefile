local_clean: remove_images remove_containers
	@echo "done"

local_build:
	docker-compose -f docker-compose.local.yml up
	# @$(MAKE) migrate

local_rebuild:
	docker-compose -f docker-compose.local.yml up --build

local_debug:
	docker-compose -f docker-compose.debug.yml up

local_setup:
	docker-compose exec web python manage.py makemigrations
	docker-compose exec web python manage.py migrate
	python local/setup_local.py

local_down:
	docker-compose -f docker-compose.local.yml down || echo "no containers up"
	docker-compose -f docker-compose.debug.yml down || echo "no containers up"

remove_images: local_down
	docker rmi -f `docker images -aq` || echo "no images present"

remove_containers: remove_images
	docker rm `docker ps -aq` || echo "no containers present"