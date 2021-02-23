`serial {"comm": "dep", "type": "set", "args" : {"mode": "start", "axe_y": 20}}`
serial {"comm": "dep", "type": "set", "args" : {"mode": "start", "axe_y": 20}}

`serial {"comm": "dep", "type": "set", "args" : {"mode": "start", "axe_y": -20}}`
serial {"comm": "dep", "type": "set", "args" : {"mode": "start", "axe_y": -20}}

`serial {"comm": "dep", "type": "set", "args" : {"mode": "stop"}}`
serial {"comm": "dep", "type": "set", "args" : {"mode": "stop"}}

`serial {"comm": "dep", "type": "set", "args" : {"pos_x": 700, "pos_y": -662.7}}`
serial {"comm": "pos", "type": "set", "args" : {"pos_x": 700, "pos_y": -600.7}}

`serial {"comm": "dep", "type": "set", "args" : {"mode": 0}}`

`serial {"comm": "dep", "type": "set", "args" : {"mode": 0}}`

`serial {"comm": "dep", "type": "set", "args" : {"mode": 0}}`

cable moteur2:670 moteur3:600


{"comm": "cal", "type": "set", "args" : {"mode":"cable","long":570,"id":0}}
{"comm": "cal", "type": "set", "args" : {"mode":"cable","long":750,"id":1}}
{"comm": "pos", "type": "get", "args" : {"mode":"cable","long":750,"id":1}}
{"comm": "pos", "type": "set", "args" : {"pos_x": 500, "pos_y": -500}}