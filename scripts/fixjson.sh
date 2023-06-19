# Fix nonstandard JSON 
#   such as that prodcued by Chia CLI commands like "chia wallet get_transactions -v"
# (This script may fail on many unexpected situations such as embedded quotations.)

# Find the modules directory
if [[ $SHELL == '/bin/bash' ]]; then
  SOURCE=${BASH_SOURCE[0]}
else
  SOURCE=$0
fi
while [ -L "$SOURCE" ]; do 
  DIR=$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )
  SOURCE=$(readlink "$SOURCE")
  [[ $SOURCE != /* ]] && SOURCE=$DIR/$SOURCE 
done
DIR=$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )
MODULE_DIR="${DIR%/*}/modules"

# Backup the original JSON file
cp $1.json $1.json.bak

# Fix single quotes, booleans, and nulls
sed -i -e "s/'/\"/g" -e "s/True/true/g" -e "s/False/false/g" -e "s/None/null/g" $1.json

# Convert undelimited series of json objects to a list
python3 $MODULE_DIR/fix_json.py $1 > $1_.json
mv $1_.json $1.json
