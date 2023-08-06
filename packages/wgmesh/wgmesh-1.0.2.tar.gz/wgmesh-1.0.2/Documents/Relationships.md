# Relationships

Singular:
 - local wg interface
 - BGP ASN

Shared with One:
 - ports: local:remote

Shared with All:
 - fd86:ea04:1115::1

### Port Alloction:

 Local port matches remote host port id.

 Remote port is my port id.

 Local ipv6 address is wg[x] index :port index.

###### Example:

Ep0

wg1: Ep0-Ep1
 - 6901
 - fd86:ea04:1115:0:1::/80

wg2: Ep0-Ep2
 - 6902
 - fd86:ea04:1115:0:2::/80


Ep1

wg0: Ep1-Ep0
 - 6900
 - fd86:ea04:1115:0:1::1/80

wg2: Ep1-Ep2
 - 6902
 - fd86:ea04:1115:1:2::1/80


Ep2

wg0: Ep2-Ep0
 - 6900
 - fd86:ea04:1115:0:2::2/80

wg1: Ep2-Ep1
 - 6901
 - fd86:ea04:1115:1:2::2/80

