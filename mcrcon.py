import socket
from struct import pack,unpack
from select import select

class mcrcon:
    def connect(self): self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM); self.socket.connect(("192.168.1.84",25579)); self._send(3,"rconpswd")
    def __enter__(self): self.connect(); return self
    def __exit__(self,type,value,tb): self.disconnect()
    def disconnect(self):
        if self.socket is not None: self.socket.close(); self.socket = None
    def _read(self,length):
        data = b""
        while len(data) < length: data += self.socket.recv(length - len(data))
        return data
    def _send(self,out_type,out_data):
        out_payload = (pack("<ii",0,out_type)+out_data.encode("utf8")+b"\x00\x00")
        out_length = pack("<i",len(out_payload))
        self.socket.send(out_length+out_payload)
        in_data = ""
        while True:
            (in_length,) = unpack("<i",self._read(4))
            in_payload = self._read(in_length)
            in_id,in_type = unpack("<ii",in_payload[:8])
            in_data += in_payload[8:-2].decode("utf8")
            if len(select([self.socket],[],[],0)[0]) == 0: return in_data
    def run(self,command): return self._send(2,command)
async def mcrsend(commands,channel):
    resps,isresp = [],False
    with mcrcon() as mcr:
        for command in commands: resps.append(mcr.run(command))
    for i,resp in enumerate(resps): 
        if resp != "": isresp = True; await channel.send(f"Console response from {commands[i]}: {resp}")
    if not isresp: await channel.send("Your evil has occured")