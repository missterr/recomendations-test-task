FROM python:3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set up a workdir
RUN mkdir /recommendations
WORKDIR /recommendations

# Install dependencies
ADD requirements.txt /recommendations/
RUN pip install -r /recommendations/requirements.txt

ADD /recommendations/ /recommendations/