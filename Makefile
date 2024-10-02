l-build:
	# Build the Docker images and start the services in detached mode
	docker compose -f local-docker-compose.yml up --build -d

l-up:
	# Start the services defined in the Docker Compose file
	docker compose -f local-docker-compose.yml up 

l-stop:
	# Stop the running services without removing them
	docker compose -f local-docker-compose.yml stop

l-down:
	# Stop and remove all services and associated containers
	docker compose -f local-docker-compose.yml down

l-logs:
	# Display the logs for all running services
	docker compose -f local-docker-compose.yml logs

l-status:
	# Show the status of all running containers
	docker ps

web-shell:
	# Access the shell of the 'web' service container
	docker exec -it web bash

makemigrations:
	# Create new database migrations based on the current models
	docker exec web python manage.py makemigrations

migrate:
	# Apply database migrations
	docker exec web python manage.py migrate
	
createsuperuser:
	# Create a superuser for the Django application
	docker exec -it web python manage.py createsuperuser

backup:
	# Execute the backup script in the db container
	docker exec db backup.sh

backups:
	# Execute the backups script in the db container
	docker exec db backups.sh

restore:
	# Restore the database from the specified backup file
	# To use this target, specify the BACKUP_FILE variable like this:
	# make restore BACKUP_FILE=your_backup_file.sql.gz
	docker exec db restore.sh $(BACKUP_FILE)