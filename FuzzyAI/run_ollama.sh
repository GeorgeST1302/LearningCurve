#!/bin/bash

# Set initial values
device=0
port=11434

# Loop 8 times
for i in {1..8}
do
  # Execute docker run command
  cid=$(docker run -d -e OLLAMA_ORIGINS=* --rm --gpus "device=$device" -v /root/.ollama:/root/.ollama -p $port:11434 ollama/ollama)

  # Increment device and port for the next iteration
  ((device++))
  ((port++))
done

docker exec -it $cid ollama pull mistral
docker exec -it $cid ollama pull llama2
docker exec -it $cid ollama pull llama3
docker exec -it $cid ollama pull phi3
docker exec -it $cid ollama pull llama2-uncensored

