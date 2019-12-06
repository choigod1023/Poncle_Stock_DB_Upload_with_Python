#! /bin/bash
#check=`ps -ef | grep 프로세스명`
check =`ps -ef | grep chromedriver | wc | awk '{print$1}'`
echo $check
if [ $check -gt 1 ];
then
 exit 0
#echo "exit"
else
#echo "start"
 nohup python3 ./poncle_stock/poncle_stock.py > output.txt &
fi

