# Switching Hub

###### tags: `Ryu`

> Ref#1 : [本章將會用簡單的 Switching hub 安裝做為題材，說明 Ryu 如何安裝一個應用程式。](https://osrg.github.io/ryu-book/zh_tw/html/switching_hub.html#)
> Ref#2 : [初學者入門建議#9:學習利用 Controller 規劃轉送邏輯](https://github.com/YanHaoChen/Learning-SDN)
> Ref#3 : [控制規則](https://github.com/YanHaoChen/Learning-SDN/tree/master/Controller/Ryu/ControlFlow)


## :memo: 紀錄實作過程

### 環境

- VMware Workstation 15  Player
-  Ryu 4.34
-  Open vSwitch 2.9.5
-  Mininet 2.2.2

 

### 目的
==交換器(Switching Hub)部分功能==
- 學習連接到port的host之MAC位址，並記錄在MAC address table 中
- 對於已記錄於MAC address table的 MAC address，若收到送往該MAC address的封包，則轉送該封包到該port
- 對於未指定目標位址的封包(**還未記錄於MAC address table?**)，則進行Flooding


### 過程(指令+截圖)

```
sudo mn --topo single,3 --mac --switch ovsk --controller remote -x
```
**Step1 mininet:**

![](https://i.imgur.com/ImnI0DB.png)
![](https://i.imgur.com/cxshbos.png)

---

==Check s1==

```
ovs-vsctl show
ovs-dpctl show
```

![](https://i.imgur.com/PLNivfC.png)

---

**設定版本OpenFlow1.3&空白Flow Table** 
(**空白Flow Table no output ?**) 

```
ovs-vsctl set bridge s1 protocols=OpenFlow13
ovs-ofctl -O OpenFlow13 dump-flows s1
```
![](https://i.imgur.com/K9UtjZm.png)

---

**Step2 Ryu:**

執行交換器

```
ryu-manager --verbose ryu.app.simple_switch_13
```

![](https://i.imgur.com/Wv8U2tL.png)


確認 Table-miss Flow Entry 已經被加入
(**What is Table-miss Flow Entry?**)
![](https://i.imgur.com/loYmcNG.png)

在ping命令執行前，確認每一台host都可收到，執行`tcpdump`確認封包確實被接收

![](https://i.imgur.com/CrW8rla.png)
![](https://i.imgur.com/WUXWwrU.png)

host 1 ping host 2

```
mininet> h1 ping -c1 h2
```

![](https://i.imgur.com/okNYyJc.png)

```
ovs-ofctl -O OpenFlow13 dump-flows s1
```
圖片中的輸出`第三行` : Table-miss Flow Entry (優先權為0)
另外加入兩個優先權為1的Flow Entry
1. 目的 MAC address (dl_dst): host1，actions:forward h1
   Flow Entry 會被 match 2次(n_packets): ARP reply + ICMP echo reply
2. 目的 MAC address (dl_dst): host2，actions:forward h2
   Flow Entry 被 match 1次 : ARP request (broadcast)，透過 ICMP echo request 完成


![](https://i.imgur.com/ghSAjvZ.png)

---

==controller c0==

**[白底部分]**

第一個 Packet-In 由 host1 發送的 ARP request，因為透過廣播的方式所以沒有Flow Entry存在，所以發送Packet-Out。

第二個是從host2回覆的 ARP reply，目的MAC address為host1，因此前述 Flow Entry(1)被新增

第三個 host1 > host2 發送的 `ICMP echo request` 因此新增 Flow Entry(2)

[補充]
ping則是用ICMP的"Echo request"（類別代碼：8）和"Echo reply"（類別代碼：0）訊息來實現的

host 2 向 host 1 回覆的 ICMP echo reply 則會和 Flow Entry (1) 發生 match，故直接轉送封包至 host 1 而不需要發送 Packet-In。

![](https://i.imgur.com/GHJHAZk.png)

---
**h1**

*h1*

host 1 首先發送廣播 ARP request 封包，接著接收到 host 2 送來的 ARP reply 回覆。 接著 host 1 發送 ICMP echo request，host 2 則回覆 ICMP echo reply 。

*h2*

對於 host 2 則是接收 host 1 發送的 ARP request 封包，接著對 host 1 發送 ARP reply 回覆。 然後接收到 host 1 來的 ICMP echo request ，回覆 host 1 echo reply。

![](https://i.imgur.com/fW5V48q.png)

**h3**

對 host 3 而言，僅有一開始接收到 host 1 的廣播 ARP request ，未做其他動作。

---

- ryu/app/simple_switch_13.py：
```python=1
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet


class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install table-miss flow entry
        #
        # We specify NO BUFFER to max_len of the output action due to
        # OVS bug. At this moment, if we specify a lesser number, e.g.,
        # 128, OVS will send Packet-In with invalid buffer_id and
        # truncated packet data. In that case, we cannot output packets
        # correctly.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]

        mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                match=match, instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        dst = eth.dst
        src = eth.src

        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = in_port

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst)
            self.add_flow(datapath, 1, match, actions)

        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)
```


