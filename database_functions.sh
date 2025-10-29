#!/bin/bash
# @name: database_functions.sh
# @creation_date: 2022-11-02
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <simonxix@simonxix.com>
# @purpose: Runs database functions for the Experimental Publishing Compendium
# @acknowledgements:
# https://www.redhat.com/sysadmin/arguments-options-bash-scripts
# https://askubuntu.com/questions/1389904/read-from-env-file-and-set-as-bash-variables

############################################################
# subprograms                                              #
############################################################

License()
{
  echo 'Copyright 2022-2025 Simon Bowie <simonxix@simonxix.com>'
  echo
  echo 'Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:'
  echo
  echo 'The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.'
  echo
  echo 'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.'
}

Help()
{
   # Display Help
   echo "This script performs database functions for the Experimental Publishing Compendium"
   echo
   echo "Syntax: database_functions.sh [-l|h|e|i|c|v|d|b]"
   echo "options:"
   echo "l     Print the MIT License notification."
   echo "h     Print this Help."
   echo "e     Export whole database."
   echo "i     Import whole database."
   echo "c     Export single table as tab-delimited txt."
   echo "v     Import tab-delimited txt file to table."
   echo "d     Drop table."
   echo "b     Backup database to remote storage."
   echo
}

Export()
{
  docker exec -i $DATABASE_CONTAINER mariadb-dump --single-transaction -u $DATABASE_USERNAME -p$DATABASE_PASSWORD $MYSQL_DATABASE > $EXPORT_DIRECTORY/$EXPORT_SQL_FILENAME`date +"%Y%m%d"`.sql
}

Import()
{
  docker exec -i $DATABASE_CONTAINER mariadb -u $DATABASE_USERNAME -p$DATABASE_PASSWORD $MYSQL_DATABASE < $IMPORT_SQL_FILE
}

Table_export()
{
  docker exec -i $DATABASE_CONTAINER bash -c "mariadb -u $DATABASE_USERNAME -p$DATABASE_PASSWORD $MYSQL_DATABASE --batch -e 'SELECT * FROM $TABLE'" > $EXPORT_TXT_DIRECTORY/$EXPORT_TXT_FILENAME.txt
}

Table_import()
{
  docker cp $IMPORT_TXT_FILE $DATABASE_CONTAINER:/tmp/import_file

  docker exec -i $DATABASE_CONTAINER bash -c "mariadb -u $DATABASE_USERNAME -p$DATABASE_PASSWORD $MYSQL_DATABASE -e 'LOAD DATA LOCAL INFILE '\''/tmp/import_file'\'' REPLACE INTO TABLE $TABLE FIELDS TERMINATED BY '\''\t'\'' LINES TERMINATED BY '\''\r'\'' IGNORE 1 ROWS;'"
}

Drop_table()
{
  docker exec -i $DATABASE_CONTAINER bash -c "mariadb -u $DATABASE_USERNAME -p$DATABASE_PASSWORD $MYSQL_DATABASE -e 'DROP TABLE IF EXISTS $TABLE;'"
}

Backup()
{
  docker exec -i $DATABASE_CONTAINER mariadb-dump --single-transaction -u $DATABASE_USERNAME -p$DATABASE_PASSWORD $MYSQL_DATABASE > $EXPORT_DIRECTORY/$BACKUP_SQL_FILENAME.sql

  scp $EXPORT_DIRECTORY/$BACKUP_SQL_FILENAME.sql $STORAGE_USERNAME@$STORAGE_SERVER:$STORAGE_DIRECTORY
}

############################################################
############################################################
# main program                                             #
############################################################
############################################################

# retrieve variables from .env file (see .env.template for template)
source .env.dev

# error message for no flags
if (( $# == 0 )); then
    Help
    exit 1
fi

# get the options
while getopts ":hleicvdb" flag; do
   case $flag in
      l) # display License
        License
        exit;;
      h) # display Help
        Help
        exit;;
      e) # export whole database
        Export
        exit;;
      i) # import database from file
        if [ -z "$2" ]
        then
          echo "-i requires a file as an argument"
          echo
          echo "Syntax: database_functions.sh -i [file]"
        else
          IMPORT_SQL_FILE=$2
          Import
          exit 1
        fi;;
      c) # export single table as tab-delimited txt
        if [ -z "$2" ]
        then
          echo "-c requires a table name as an argument"
          echo
          echo "Syntax: database_functions.sh -c [table name]"
        else
          TABLE=$2
          Table_export
          exit 1
        fi;;
      v) # import single tab-delimited txt to table
        if [ -z "$2" ] || [ -z "$3" ]
        then
          echo "-v requires a table name as an argument and the file to be imported"
          echo
          echo "Syntax: database_functions.sh -v [table name] [file]"
        else
          TABLE=$2
          IMPORT_TXT_FILE=$3
          Table_import
          exit 1
        fi;;
      d) # drop table
      if [ -z "$2" ]
      then
        echo "-d requires a table name as an argument"
        echo
        echo "Syntax: database_functions.sh -d [table name]"
      else
        TABLE=$2
        Drop_table
        exit 1
      fi;;
      b) # backup database to secure storage
        Backup
        exit;;
      \?) # invalid option
        Help
        exit;;
   esac
done
