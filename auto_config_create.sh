rm -f my_auto_topo_conf
sudo rm -rf frrouting_cfg/ 
sudo rm -rf scripts/tmp/
mkdir frrouting_cfg/

cd scripts/
./script.py
cd tmp/routers/
chmod +x *_*
cd ../../../

cp scripts/tmp/my_auto_conf my_auto_topo_conf
cp -r scripts/tmp/routers/* frrouting_cfg/

sudo rm -rf scripts/tmp
