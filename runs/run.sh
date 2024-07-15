#!/usr/bin/env bash

IFS=$'\n'
for row in $(cat flights-to-scan.csv)
do
  origin_airport_name=$(echo $row | cut -d "," -f 1)
  origin_airport_code=$(echo $row | cut -d "," -f 2)
  destination_airport_name=$(echo $row | cut -d "," -f 3)
  destination_airport_code=$(echo $row | cut -d "," -f 4)
  departure_date=$(echo $row | cut -d "," -f 5)
  return_date=$(echo $row | cut -d "," -f 6)
  echo "Running for: $origin_airport_name $origin_airport_code $destination_airport_name $destination_airport_code $departure_date $return_date..."
  poetry -C ../yafs run yafs \
    --origin-airport $origin_airport_name $origin_airport_code \
    --destination-airport $destination_airport_name $destination_airport_code \
    --departure-date "$departure_date" \
    --return-date "$return_date"
  echo "Done."
done
