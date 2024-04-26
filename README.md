# Private GPT

Based on https://github.com/imartinez/privateGPT.git primordial branch

## The image

1. Build the container with the `Dockerfile`

## The container

1. Create a directory for your `source_documents` and adjust the `docker-compose.yaml` file to point to it
2. Do the same for the `db` directory
3. Set the `MODEL` environment to the Ollama model you are using
4. Set the `OLLAMA_BASE_URL` environment variable to point to the Ollama server you want to use

## Ollama

1. Make sure it is listening on the correct ip address by setting the system environment variable `OLLAMA_HOST` to `0.0.0.0`, or the ip address you want to use. This will require a restart of Ollama `launchctl setenv OLLAMA_HOST "0.0.0.0"` on the mac

## Done

1. Start the container
2. Get it to import the files in `source_documents` by running `docker exec -it privategpt_local-private_gpt-1 python ingest.py`, you will only need to run this when the source documents are updated
3. Make queries with `docker exec -it privategpt_local-private_gpt-1 python privateGPT.py`
