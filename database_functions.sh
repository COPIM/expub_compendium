#!/bin/bash
# @name: database_functions.sh
# @creation_date: 2022-11-02
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: Runs database functions for the ExPub Compendium
# @acknowledgements:
# https://www.redhat.com/sysadmin/arguments-options-bash-scripts

############################################################
# subprograms                                              #
############################################################
License()
{
  echo 'Copyright 2022 Simon Bowie <ad7588@coventry.ac.uk>'
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
   echo "This script performs database functions for the ExPub Compendium"
   echo
   echo "Syntax: database_functions.sh [-l|h|e|i|c|v|d]"
   echo "options:"
   echo "l     Print the MIT License notification."
   echo "h     Print this Help."
   echo "e     Export whole database."
   echo "i     Import whole database."
   echo "c     Export single table as tab-delimited txt."
   echo "v     Import tab-delimited txt file to table."
   echo "d     Drop table."
   echo
}

Export()
{
  docker exec -it $CONTAINER mysqldump --single-transaction -u $USERNAME -p$PASSWORD $DATABASE > $EXPORT_DIRECTORY/$EXPORT_SQL_FILENAME`date +"%Y%m%d"`.sql
}

Import()
{
  docker exec -i $CONTAINER mysql -u $USERNAME -p$PASSWORD $DATABASE < $IMPORT_SQL_FILE
}

Table_export()
{
  docker exec -it $CONTAINER bash -c "mysql -u $USERNAME -p$PASSWORD $DATABASE --batch -e 'SELECT * FROM $TABLE'" > $EXPORT_TXT_DIRECTORY/$EXPORT_TXT_FILENAME.txt
}

Table_import()
{
  docker cp $IMPORT_TXT_FILE $CONTAINER:/tmp/import_file

  docker exec -i $CONTAINER bash -c "mysql -u $USERNAME -p$PASSWORD $DATABASE -e 'LOAD DATA LOCAL INFILE '\''/tmp/import_file'\'' REPLACE INTO TABLE $TABLE FIELDS TERMINATED BY '\''\t'\'' LINES TERMINATED BY '\''\n'\'' IGNORE 1 ROWS;'"
}

Drop_table()
{
  docker exec -i $CONTAINER bash -c "mysql -u $USERNAME -p$PASSWORD $DATABASE -e 'DROP TABLE IF EXISTS $TABLE;'"
}
############################################################
############################################################
# main program                                             #
############################################################
############################################################

# set variables
CONTAINER=mariadb
DATABASE=toolkit
USERNAME=xxxxxxxx
PASSWORD=xxxxxxxx
EXPORT_DIRECTORY="./db_exports"
EXPORT_SQL_FILENAME=toolkit_db_
EXPORT_TXT_FILENAME=$2`date +"%Y%m%d"`

# error message for no flags
if (( $# == 0 )); then
    Help
    exit 1
fi

# get the options
while getopts ":hleicvd" flag; do
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
      \?) # Invalid option
        Help
        exit;;
   esac
done
