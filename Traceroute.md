wiki 
>traceroute，現代Linux系統稱為tracepath，Windows系統稱為tracert，是一種電腦網路工具。它可顯示封包在IP網路經過的路由器的IP位址。

![](https://i.imgur.com/B1c7MU4.png)
![](https://i.imgur.com/7EP4t5t.png)

---

```shell
sudo traceroute –q 1 –I 8.8.8.8
```

Ref : [Linux 中 TRACEROUTE 使用浅析](https://belen.one/blog/2018/08/traceroute-command-in-linux/)
```shell
-d：使用Socket层级的排错功能；
-f<存活数值>：设置第一个检测数据包的存活数值TTL的大小；
-F：设置勿离断位；
-g<网关>：设置来源路由网关，最多可设置8个；
-i<网络界面>：使用指定的网络界面送出数据包；
-I：使用ICMP回应取代UDP资料信息；
-m<存活数值>：设置检测数据包的最大存活数值TTL的大小；
-n：直接使用IP地址而非主机名称；
-p<通信端口>：设置UDP传输协议的通信端口；
-r：忽略普通的Routing Table，直接将数据包送到远端主机上。
-s<来源地址>：设置本地主机送出数据包的IP地址；
-t<服务类型>：设置检测数据包的TOS数值；
-v：详细显示指令的执行过程；
-w<超时秒数>：设置等待远端主机回报的时间；
-x：开启或关闭数据包的正确性检验。
```

--- 

Question : 只有封包序號和 * 的回傳 在 VM Ubuntu 16 的環境 
但在 Windows ，是可以知道 各個經過的 Router Gateway 
![](https://i.imgur.com/laTATwZ.png)
原因 : ifconfig 為 虛擬 IP 192.168.x.x
VM 預設的網路 為 NAT 

---

[問題解析] 
![](https://i.imgur.com/q1LTDzu.png)

[NAT 架構]
![](https://i.imgur.com/I9EfBWS.jpg)
[Bridge 架構]
![](https://i.imgur.com/QfoFKSI.png)

[解決方法]
![](https://i.imgur.com/Ne8DBph.png)
在 Power Off 的情況下 ，Edit 網路設定
![](https://i.imgur.com/cFT6EEl.png)
重啟 再下 
```
sudo traceroute -q 1 -I 8.8.8.8
```
![](https://i.imgur.com/3JhMNHi.jpg)


---

[其他]
`apt intall traceroute`
sol : [Could not get lock/lib/dpkg/lock-fronted](https://askubuntu.com/questions/1109982/e-could-not-get-lock-var-lib-dpkg-lock-frontend-open-11-resource-temporari)

--- 

VM Bridge on Windows 

| Windows 家用版   |  Windows 專業版 |
| - | - |
| 使用 Wifi | 使用  乙太網路 |

如果家用版使用 乙太網路，VM 調 Bridge 會發生網路連不上的問題。
Ref : [How to fix Connection Problem with Bridged Networking in VMware](https://www.youtube.com/watch?v=H5WSjafQFZc&feature=youtu.be)
與 影片中不一樣的是 我沒有把 Bridge 的 Configuration 的 勾選項目 關掉，我是全勾。

![](https://i.imgur.com/1nIUAME.png)
![](https://i.imgur.com/biQOrT9.png)






