# Fix nonstandard JSON 
#   such as that prodcued by Chia CLI commands like "chia wallet get_transactions -v"
# (This script may fail on many unexpected situations such as embedded quotations.)

cp $1.json $1.json.bak
sed -i -e "s/'/\"/g" -e "s/True/true/g" -e "s/False/false/g" -e "s/None/null/g" $1.json
python3 fix_json.py $1 > $1_.json
mv $1_.json $1.json
