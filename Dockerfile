# Start with a python base image
# Take your pick from https://hub.docker.com/_/python
FROM python:3.11-slim

# Set /flask-app as the main application directory
WORKDIR /OCR

# Copy the requirements.txt file and required directories into docker image
COPY ./requirements.txt ./requirements.txt
COPY ./templates ./templates
COPY ./sample_pdf ./sample_pdf
COPY ./app_pdfplumber.py ./app_pdfplumber.py

# Add /src directory to PYTHONPATH, so that model.py Python module can be found
# To add multiple directories, delimit with colon e.g. /flask-app/src:/flask-app
ENV PYTHONPATH /OCR

# Install python package dependancies, without saving downloaded packages locally
RUN pip install -r requirements.txt --no-cache-dir

# Allow port 80 to be accessed (Flask app)
EXPOSE 80

# Start the Flask app using gunicorn
CMD ["gunicorn", "--bind=0.0.0.0:80", "app_pdfplumber:app"]