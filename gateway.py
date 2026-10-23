import socket, struct, smtplib, time
from aiosmtpd.controller import Controller

def scan(data):
    s = socket.create_connection(("clamav", 3310))
    s.sendall(b"zINSTREAM\0")
    for i in range(0, len(data), 8192):
        c = data[i:i+8192]
        s.sendall(struct.pack("!I", len(c)) + c)
    s.sendall(struct.pack("!I", 0))
    r = s.recv(4096).decode().strip("\0\n ")
    s.close()
    return r

class Handler:
    async def handle_DATA(self, server, session, env):
        r = scan(env.content)
        print("CLAMAV RESULT:", r, flush=True)
        if "FOUND" in r:
            return "554 Message rejected: " + r
        with smtplib.SMTP("mailpit", 1025) as m:
            m.sendmail(env.mail_from, env.rcpt_tos, env.content)
        return "250 OK delivered"

Controller(Handler(), hostname="0.0.0.0", port=2525).start()
print("Gateway ready", flush=True)
while True:
    time.sleep(3600)