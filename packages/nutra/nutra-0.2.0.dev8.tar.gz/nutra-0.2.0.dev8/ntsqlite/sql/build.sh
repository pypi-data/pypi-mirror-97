#!/bin/bash -e

cd "$(dirname "$0")"

rm_cmd="rm -f nt.sqlite"
printf "\\n\e[1;31m${rm_cmd}\e[0m\\n\n"
$rm_cmd

pack_msg="==> Pack nt.sqlite"
printf "\\n\\x1b[32m${pack_msg}\x1b[0m\n\n"

# Create SQL file
pack_cmd="sqlite3 nt.sqlite \".read init.sql\""
# pack_cmd="sqlite3 nt.sqlite -init init.sql"
printf "\\n\e[1;31m${pack_cmd}\e[0m\\n"
bash -exec "$pack_cmd"
# sqlite3 nt.sqlite
