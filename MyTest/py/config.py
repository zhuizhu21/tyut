# -*- coding: UTF-8 -*-
'''
定时任务，每天凌晨重启VPN
'''
import os
import time
os.system("docker stop $(docker ps -q)")
time.sleep(2)
os.system("docker run -it --rm  "
          " --privileged  "
          " --net fortinet "
          "--ip 172.20.0.2  "
          " -e VPNADDR=218.26.181.244:443 "
          "  -e VPNUSER=liuqian2028 "
          "  -e VPNPASS=132432532xiao "
          "  auchandirect/forticlient"
          )