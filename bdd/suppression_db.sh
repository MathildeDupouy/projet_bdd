#!/usr/bin/bash
# This file has to be executable, run : chmod +x suppression_db.sh
# Call this script with command : ./suppression_db.sh <db_name> <username> <password>


DB_NAME=$1
USER_DB=$2
PWD=$3

echo "Deleting tables..."
file='delete_tables.psql'
psql -U $USER_DB -d $DB_NAME -f $file

echo ""
echo "Terminated."
echo "To check the database, run :"
echo "psql -U <username> -d <dbname>"