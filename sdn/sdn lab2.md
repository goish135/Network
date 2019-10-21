Ubuntu 版本 很重要

Ubuntu 版本 很重要

Ubuntu 版本 很重要

[VMware Player 虛擬機器安裝 Ubuntu 設定教學](https://www.kjnotes.com/linux/18)

[Mininet介紹與安裝 — on Ubuntu 16.04](https://ting-kuan.blog/2017/11/03/%e3%80%90mininet%e4%bb%8b%e7%b4%b9%e8%88%87%e5%ae%89%e8%a3%9d-on-ubuntu-16-04%e3%80%91/)

查看 Ubuntu 版本
```
lsb_release -a
```
![](https://i.imgur.com/xE3Ani4.png)

---
切到 root
```
sudo -i
sudo su
```
更新
```
apt-get update
```

升級
```
apt-get upgrade
```

重啟
```
reboot
```
---

clone mininet by git 
```
apt-get install git
cd /home/bbb # bbb 為帳戶名稱
git clone git://github.com/mininet/mininet
```
切到 mininet/util 目錄
利用 shell 檔案安裝mininet

```
cd mininet/util
./install.sh -a #安裝所有mininet套件
```
看到 Enjoy mininet 代表安裝完成

查看 mininet 版本
```
git tag
```
直接使用 預設版本的mininet
```
mn --version
```

---

測試 mininet 
```
mn --test pingall
```

---
[Ryu介紹與安裝（利用pip安裝） — on Ubuntu 16.04](https://ting-kuan.blog/2017/11/05/%e3%80%90ryu%e4%bb%8b%e7%b4%b9%e8%88%87%e5%ae%89%e8%a3%9d%ef%bc%88%e5%88%a9%e7%94%a8pip%e5%ae%89%e8%a3%9d%ef%bc%89-on-ubuntu-16-04%e3%80%91/)

安裝 python 的套件管理工具
```
apt-get install python-pip
apt-get install python-setuptools
```
安裝 ryu
```
pip install ryu
```

**執行Ryu**
```
ryu-manager
```
![](https://i.imgur.com/p83iYTY.png)

出現**loading app ryu.controller.ofp_handler instantiating app ryu.controller.ofp_handler of OFPHandler** 代表正確無誤

開啟兩個 terminal 
一個執行 Ryu 一個執行 Mininet
***Ryu***
```
ryu-manager --verbose --observe-links
```
Ryu 執行後，等mininet連接
***Mininet***
```
mn --topo-linear,2 --controller = remote
```

---

Ryu 的圖形化介面

尋找 ryu 的安裝路徑
```
pip show --files ryu
```

切到 ryu 的安裝路徑
```
cd /user/local/lib/python2.7/dist-packages
```

執行 Ryu ，可顯示圖形化介面(會顯示可連接網址)
```
ryu-manager --verbose --observe-links ryu/app/gui_topology/gui_topoplogy.py
```

瀏覽器輸入以下網址 即可開啟GUI
`http://0.0.0.0:8080` or `localhost:8080` or `127.0.0.1:8080`






