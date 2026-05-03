#!/usr/bin/env bash

OUTPUT="sql/load.sql"
> $OUTPUT  # reset file

for i in data/raw/*.csv
do
    TABLE=$(basename "$i" .csv)

    echo "COPY $TABLE FROM '/data/raw/$(basename $i)' WITH (FORMAT csv, HEADER true);" >> $OUTPUT
done