import subprocess
import time
import os
while True:
    result = str(subprocess.check_output('ps -ef | grep chromedriver', shell=True))
    if './chromedriver' in result:
        print("chromdriver is running...")
        time.sleep(100)
        continue
    else:
        os.system("nohup python3 poncle_stock.py > output.txt &")
        print("chromedriver open")
        time.sleep(1000)
        continue
