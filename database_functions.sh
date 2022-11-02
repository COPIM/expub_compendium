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
   echo "Syntax: database_functions.sh [-l|h|e]"
   echo "options:"
   echo "l     Print the MIT License notification."
   echo "h     Print this Help."
   echo "e     Export."
   echo "i     Import."
   echo
}

Export()
{
  docker exec -it $CONTAINER mysqldump --single-transaction -u $USERNAME -p$PASSWORD $DATABASE > $EXPORT_FILENAME`date +"%Y%m%d"`.sql
}

Import()
{
  docker exec -i $CONTAINER mysql -u $USERNAME -p$PASSWORD $DATABASE < $DIRECTORY/$IMPORT_FILENAME
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
EXPORT_FILENAME=toolkit_db_
DIRECTORY="/Users/ad7588/Downloads"
IMPORT_FILENAME=toolkit_db.sql

# Get the options
while getopts ":hlimzaespxdw" option; do
   case $option in
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
      \?) # Invalid option
        echo "Error: Invalid option"
        exit;;
   esac
done
