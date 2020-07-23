import paramiko
import logging

logger = logging.getLogger("pynet-ssh")
logger.setLevel(logging.ERROR)

CISCO = 1
HP = 2
HUAWEI = 3
IOSXR = 5
SERVER = 99

TIMEOUT_SEC = 10

class SSHConnect:
    prompt = ""
    ios_type = CISCO

    def __init__(self, host, pwd, ios_type=CISCO, port=22, user="automatico"):
        # ==================== PROMPT DEFINITION
        self.ios_type = ios_type
        self.host = host
        self.prompt = self.find_prompt(ios_type)

        # ==================== CONNECTION MANAGEMENT
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            self.ssh.connect(
                host,
                username=user,
                password=pwd,
                port=port,
                look_for_keys=False,
                allow_agent=False,
                timeout=TIMEOUT_SEC,
                banner_timeout=TIMEOUT_SEC,
                auth_timeout=TIMEOUT_SEC
            )
            if self.is_connected():
                self.channel = self.ssh.invoke_shell()
                self.clear_banner()

                # === DISABLE SCROLLING
                if self.ios_type == HUAWEI:
                    self.send_command("screen-length 0 temp")
                elif self.ios_type == HP:
                    self.send_command("screen-length disable")
                else:
                    self.send_command("terminal length 0")
        except Exception as e:
            logger.error(f"[PYNET-SSH]: {self.host} - {e}")
            raise

    def find_prompt(self, ios_type):
        switcher = {1: "#", 2: ">", 3: ">", 4:"#"}
        return switcher.get(ios_type, "#")

    def clear_banner(self):
        buff = ""
        while not buff.endswith(self.prompt):
            resp = self.channel.recv(9999).decode("utf-8").strip()  # === Banner received
            buff += resp

    def __del__(self):
        self.ssh.close()

    def is_connected(self):
        if self.ssh.get_transport() is not None:
            return self.ssh.get_transport().is_active()
        return False

    def disconnect(self):
        self.ssh.close()

    def commit(self):
        self.send_command("commit")

    def read_char(self):
        buffer = ""
        eol = ""
        while not (eol.strip().endswith(self.prompt) and not eol.strip().endswith(" #")):
            resp = self.channel.recv(9999).decode("utf-8")  # === Line is received
            if len(resp) > 0:
                buffer += resp
            eol += resp

        buffer = buffer.replace("\r", "")
        console = buffer.split("\n")
        clear_console = []
        
        for line in console:
            line = line.strip()
            if line!="":
                clear_console.append(line)

        clear_console.pop(0)        # === Delete first line, usually command sent
        if len(clear_console) > 0:  # === Delete last line (device prompt)
            clear_console.pop()

        return clear_console

    def send_command(self, cmd):
        buffer = []
        if self.ios_type == HUAWEI or self.ios_type == HP:
            if cmd == "system":
                self.prompt = "]"
            elif cmd == "return":
                self.prompt = ">"

        cmd = cmd.strip()

        self.channel.send(cmd + "\n")
        try:
            buffer = self.read_char()
        except Exception as e:
            logger.error(f"[PYNET-SSH]: Couldn't send {cmd} to {self.host} - {e}" % (self.host, cmd, e))
            pass    # === Rarely the device wouldn't answer to the cmd, prevent main program from crashing
        return buffer
