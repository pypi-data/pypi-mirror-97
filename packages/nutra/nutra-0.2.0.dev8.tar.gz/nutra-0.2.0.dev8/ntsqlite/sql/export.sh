#!/bin/bash -e

cd "$(dirname "$0")"

table_cmd="sqlite3 nt.sqlite '.tables'"
tables=`sqlite3 nt.sqlite '.tables'`

for t in $tables
do
    export_cmd="SELECT * FROM $t"
    echo $export_cmd
    export_cmd="sqlite3 -csv nt.sqlite "\"$export_cmd\"""
    bash -exec "$export_cmd" > "data/$t.csv"
done
