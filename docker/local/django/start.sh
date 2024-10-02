#!/bin/bash

# Function to print messages in green (success)
print_success() {
    echo -e "\e[32m$1\e[0m"  # 32 is the code for green text
}

# Function to print messages in yellow (warning)
print_warning() {
    echo -e "\e[33m$1\e[0m"  # 33 is the code for yellow text
}

# Function to print messages in red (error)
print_error() {
    echo -e "\e[31m$1\e[0m"  # 31 is the code for red text
}

# Function to create a superuser
create_superuser() {
    if [ ! -z "$DJANGO_SUPERUSER_PHONE" ] && [ ! -z "$DJANGO_SUPERUSER_USERNAME" ] && [ ! -z "$DJANGO_SUPERUSER_PASSWORD" ]; then
        echo "Creating superuser..."
        
        # Create the superuser
        python manage.py createsuperuser --noinput --phone "$DJANGO_SUPERUSER_PHONE" --username "${DJANGO_SUPERUSER_USERNAME}" &>/dev/null

        # Check if superuser creation was successful
        if [ $? -eq 0 ]; then
            print_success "Superuser created successfully."
        else
            print_error "Superuser creation failed. It may already exist."
        fi
    else
        print_warning "Superuser creation skipped. Please set DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_PHONE, and DJANGO_SUPERUSER_PASSWORD environment variables."
    fi
}

# Run migrations
echo "Making migrations..."
python manage.py makemigrations --noinput 


echo "Applying migrations..."
python manage.py migrate --noinput


# Create superuser
create_superuser

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput 

# Start the Django server
echo "Starting the Django server..."
python manage.py runserver 0.0.0.0:8000
