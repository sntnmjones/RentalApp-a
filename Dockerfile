# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.10

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

RUN apt update && \
    # Install postgres packages
    apt install -y libpq-dev gcc

# create root directory for our project in the container
RUN mkdir /rental_app

# Set the working directory to /rental_app
WORKDIR /rental_app

# Copy the current directory contents into the container at /rental_app
ADD . /rental_app/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Collects the static files into STATIC_ROOT.
RUN python3 manage.py collectstatic --noinput