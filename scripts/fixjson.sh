# Fix nonstandard JSON 
#   such as that prodcued by Chia CLI commands like "chia wallet get_transactions -v"
# (This script may fail on many unexpected situations such as embedded quotations.)

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
MODULE_DIR="${SCRIPT_DIR%/*}/modules"

cp $1.json $1.json.bak
sed -i -e "s/'/\"/g" -e "s/True/true/g" -e "s/False/false/g" -e "s/None/null/g" $1.json
python3 $MODULE_DIR/fix_json.py $1 > $1_.json
mv $1_.json $1.json
