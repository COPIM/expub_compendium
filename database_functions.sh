#!/bin/bash
# @name: database_functions.sh
# @creation_date: 2022-11-02
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: Runs database functions for the ExPub Compendium
# @acknowledgements:
# https://www.redhat.com/sysadmin/arguments-options-bash-scripts

############################################################
# Subprograms                                              #
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
   echo "Syntax: database_functions.sh [-l|h|e|i|c]"
   echo "options:"
   echo "l     Print the MIT License notification."
   echo "h     Print this Help."
   echo "e     Export whole database."
   echo "i     Import whole database."
   echo "c     Export single table as CSV."
   echo "v     Import CSV file to table."
   echo
}

Export()
{
  docker exec -it $CONTAINER mysqldump --single-transaction -u $USERNAME -p$PASSWORD $DATABASE > $EXPORT_SQL_FILENAME`date +"%Y%m%d"`.sql
}

Import()
{
  docker exec -i $CONTAINER mysql -u $USERNAME -p$PASSWORD $DATABASE < $IMPORT_SQL_DIRECTORY/$IMPORT_SQL_FILENAME
}

CSV_table_export()
{
  docker exec -it $CONTAINER bash -c "mysql -u $USERNAME -p$PASSWORD $DATABASE --batch -e 'SELECT * FROM $TABLE'" > $EXPORT_CSV_DIRECTORY/$CSV_FILENAME.txt
}

CSV_table_import()
{
  docker cp $IMPORT_CSV_FILE $CONTAINER:/tmp/import_file

  docker exec -i $CONTAINER bash -c "mysql -u $USERNAME -p$PASSWORD $DATABASE -e 'LOAD DATA LOCAL INFILE '\''/tmp/import_file'\'' REPLACE INTO TABLE $TABLE FIELDS TERMINATED BY '\''\t'\'' LINES TERMINATED BY '\''\n'\'' IGNORE 1 ROWS;'"
}
############################################################
############################################################
# Main program                                             #
############################################################
############################################################

# Set variables
CONTAINER=mariadb
DATABASE=toolkit
USERNAME=xxxxxxxx
PASSWORD=xxxxxxxx
EXPORT_SQL_FILENAME=toolkit_db_
IMPORT_SQL_DIRECTORY="/Users/ad7588/Downloads"
IMPORT_SQL_FILENAME=toolkit_db.sql
EXPORT_CSV_DIRECTORY="./db_exports"
CSV_FILENAME=$2`date +"%Y%m%d"`

# error message for no flags
if (( $# == 0 )); then
    Help
    exit 1
fi

# Get the options
while getopts ":hleicv" flag; do
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
        Import
        exit;;
      c) # export single table as CSV
        TABLE=$2
        CSV_table_export
        exit;;
      v) # import single CSV to table
        TABLE=$2
        IMPORT_CSV_FILE=$3
        CSV_table_import
        exit;;
      \?) # Invalid option
        echo "Error: Invalid option"
        exit;;
   esac
done
