Root 老大 權限最大 

切到 root 
```
sudo su
```
或者 
```
sudo -i
```

--- 

安裝 git
```
apt get git
```

使用git 安裝mininet
```
get clone git://github.com/miniet/miniet
mininet/util/install.sh -a 
```

建立 mininet 最基本的虛擬拓樸
```
mn
```

---

鏈結訊息
```
net
```
節點訊息
```
dump
```

---

`h1 ping 1個封包給 h2`

```
h1 ping -c 1 h2
```

或者

使用 mininet 叫出兩個host的terminal

```
xterm h1 h2
```

在 h2 輸入

```
ifconfig
```

在 h1 輸入

```
ping 10.0.0.2
```

在 mininet 輸入

```
sudo wireshark
```

此時 可以用wireshark監控封包傳送








