#!/usr/bin/bash
# This file has to be executable, run : chmod +x generation_db.sh
# Call this script with command : ./generation_db.sh <db_name> <username> <password>


DB_NAME=$1
USER_DB=$2
PWD=$3

echo "Creating user $USER_DB..."
psql -U "postgres" -v user_db=$USER_DB -v pwd_db=$PWD -f create_user.psql

echo "Creating database $DB_NAME..."
psql -U "postgres" -v owner=$USER_DB -v db_name=$DB_NAME -f create_db.psql

echo "Creating tables..."
cd tables
for file in *.psql; do
    echo "Creating table $file..."
    psql -U $USER_DB -d $DB_NAME -f $file
done

echo ""
echo "Terminated."
echo "To check the database, run :"
echo "psql -U <username> -d <dbname>"