> ...

ubuntu默认不支持vlan模块，安装：

`apt-get install vlan`

实例：
```
vconfig add eth0 100此时eth0必须是up的状态
vconfig set_flag eth0.100 1 1
ifconfig eth0.100 192.168.2.1 255.255.255.0 up
```

```
vconfig Usage:
       add             [interface-name] [vlan_id]
       rem             [vlan-name]
       set_flag        [interface-name] [flag-num]       [0 | 1]
       set_egress_map  [vlan-name]      [skb_priority]   [vlan_qos]
       set_ingress_map [vlan-name]      [skb_priority]   [vlan_qos]
       set_name_type   [name-type]
```
* The [interface-name] is the name of the ethernet card that hoststhe VLAN you are talking about.
* The vlan_id is the identifier (0-4095) of the VLAN you are operating on.
* skb_priority is the priority in the socket buffer (sk_buff).
* vlan_qos is the 3 bit priority in the VLAN header
* name-type:  VLAN_PLUS_VID (vlan0005), VLAN_PLUS_VID_NO_PAD (vlan5), DEV_PLUS_VID (eth0.0005), DEV_PLUS_VID_NO_PAD (eth0.5)
* FLAGS:  1 REORDER_HDR  When this is set, the VLAN device will move the ethernet header around to make it look exactly like a real ethernet device.  This may help programs such as DHCPd which read the raw ethernet packet and make assumptions about the location of bytes.  If you don't need it, don't turn it on, because there will be at least a small performance degradation.  Default is OFF.
