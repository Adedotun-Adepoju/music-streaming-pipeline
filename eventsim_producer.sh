#! /bin/bash
echo "here"
cd eventsim 

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
        --start-time "2016-08-01T00:00:00" \
        --end-time "2016-08-01T05:00:00" \
        --nusers 5000 \
        --growth-rate 0.25 \
        --userid 1 \
        --kafkaBrokerList localhost:9092 \
        --randomseed 1 \
        --continuous

echo "producing events..."