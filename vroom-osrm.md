```
docker run -t -v "/mnt/c/work/vroom/osrm:/data" osrm/osrm-backend osrm-extract -p /opt/car.lua /data/us-northeast-latest.osm.pbf && /usr/local/bin/osrm-partition /data/us-northeast-latest.osm.pbf && /usr/local/bin/osrm-customize /data/us-northeast-latest.osm.pbf
```
```
version: "2.4"
services:
  vroom:
    network_mode: host
    image: vroomvrp/vroom-docker:v1.11.0
    container_name: vroom
    volumes:
      - ./conf/:/conf
    environment:
      - VROOM_ROUTER=osrm  # router to use, osrm, valhalla or ors
    depends_on:
      - osrm

  # EXAMPLE for OSRM, please consult the repo for details: https://hub.docker.com/r/osrm/osrm-backend/
  osrm:
    image: osrm/osrm-backend
    container_name: osrm
    restart: always
    ports:
      - 5000:5000
    volumes:
      - ./osrm:/data
    command: "osrm-routed --max-matching-size 1000 --max-table-size 1000 --max-viaroute-size 1000 --algorithm mld /data/us-northeast-latest.osrm"

```
```
docker-compose -f vroom-osrm.yml up
```
