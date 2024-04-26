FROM --platform=amd64 python:3.10

# docker build -t private_gpt .

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY *.py .

##
# This will load the embedding for the embedding model
# and save them as part of the image so they will not
# need to be reloaded each time the container is run
##

RUN python privateGPT.py -E

CMD ["sleep", "infinity"]
