# We Use an official Python runtime as a parent image
FROM python:3.8.9

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /tradecore_social

# Set the working directory to /music_service
WORKDIR /tradecore_social

# Copy the current directory contents into the container at /music_service
ADD . /tradecore_social/

# Install any needed packages specified in requirements.txt
RUN pip install  --no-cache-dir -r requirements.txt
