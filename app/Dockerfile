FROM python:3.12.2-bookworm

# set some environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./app/requirements.txt .
RUN pip install -r requirements.txt
COPY ./app/entrypoint.sh .
RUN chmod +x entrypoint.sh

# copy project
COPY ./app/src/ticmagicalline .

ENTRYPOINT [ "/entrypoint.sh" ]
