rm -rf dump
unzip dump.zip
./clear_db.sh
mongorestore dump
rm -rf dump
