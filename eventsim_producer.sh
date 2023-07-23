#! /bin/bash
cd eventsim 

# Get current time 
current_time=$(date -u "+%Y-%m-%dT%H:%M:%S")

echo -e "\nStarting publish event at $current_time UTC" 

# Calculate time from 15 minutes ago
last_30_minutes=$(date -d '15 minutes ago' "+%Y-%m-%dT%H:%M:%S")

echo "Building docker image to generate events...."
sudo docker build -t eventsim .

echo "Running the container to generate events..."
sudo docker rm streaming_events
sudo docker run -itd \
    --network host \
    --name streaming_events \
    --memory="5.5g" \
    --memory-swap="7g" \
    eventsim \
        -c "examples/example-config.json" \
        --start-time $last_30_minutes \
        --end-time $current_time \
        --nusers 5000 \
        --growth-rate 0.25 \
        --userid 1 \
        --kafkaBrokerList localhost:9092 \
        --randomseed 1 \
        --continuous

echo "producing events..."

echo "done"
