import paramiko
import logging

logger = logging.getLogger("devnet_ssh")
logger.setLevel(logging.ERROR)

class SSHConnect:
    """
    Class used to establish interactive SSH session
    """
    CISCO = 1
    HP = 2
    HUAWEI = 3
    IOSXR = 5
    SERVER = 99
    TIMEOUT_SEC = 10

    def __init__(self, host, user, pwd, os_type=CISCO, port=22):
        """ Initializes attributes and establishes connection to the device,

        Args:
            host (str): Hostname or IP address of the target device.
            user (str): Username to authenticate
            pwd (str): Password to authenticate
            os_type (int, optional): Vendor Type, used to select prompt. Defaults to CISCO.
            port (int, optional): Port used for SSH. Defaults to 22.
        """

        # ==================== PROMPT DEFINITION
        self.os_type = os_type
        self.host = host
        self.prompt = self._find_prompt()

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
                timeout=self.TIMEOUT_SEC,
                banner_timeout=self.TIMEOUT_SEC,
                auth_timeout=self.TIMEOUT_SEC
            )
            if self.is_connected():
                self.channel = self.ssh.invoke_shell()
                self._clear_banner()

                # === DISABLE SCROLLING
                if self.os_type == self.HUAWEI:
                    self.send_command("screen-length 0 temp")
                elif self.os_type == self.HP:
                    self.send_command("screen-length disable")
                else:
                    self.send_command("terminal length 0")
        except Exception as e:
            logger.error(f"[PYNET-SSH]: {self.host} - {e}")
            raise

    def __del__(self):
        self.ssh.close()

    def _clear_banner(self):
        """
        Clears the banner MOTD/banner login
        """
        buff = ""
        while not buff.endswith(self.prompt):
            resp = self.channel.recv(9999).decode("utf-8").strip()  # === Banner received
            buff += resp

    def _find_prompt(self):
        """
        Selects the apropiate prompt for the connection

        Returns:
            str: Prompt used for the connection.
        """
        switcher = {1: "#", 2: ">", 3: ">", 4:"#"}
        return switcher.get(self.os_type, "#")
    
    def _read_char(self):
        """
        Reads whatever is on the channel, clears the device prompt and returns device console as a list

        Returns:
            list: List with device output
        """
        buffer = ""
        eol = ""
        clear_console = []

        while not (eol.strip().endswith(self.prompt) and not eol.strip().endswith(" #")):
            resp = self.channel.recv(9999).decode("utf-8")  # === Line is received
            if len(resp) > 0:
                buffer += resp
            eol += resp

        buffer = buffer.replace("\r", "")
        console = buffer.split("\n")
        
        for line in console:
            line = line.strip()
            if line!="":
                clear_console.append(line)

        clear_console.pop(0)        # === Delete first line, usually command sent
        if len(clear_console) > 0:  # === Delete last line (device prompt)
            clear_console.pop()

        return clear_console

    def disconnect(self):
        """
        Closes the connection
        """
        self.ssh.close()

    def is_connected(self):
        """
        Checks if SSH session is active

        Returns:
            boolean: SSH session active or disconnected
        """
        if self.ssh.get_transport() is not None:
            return self.ssh.get_transport().is_active()
        return False

    def send_command(self, cmd):
        """
        Sends a command line to the device and returns its output.

        Args:
            cmd (str): Command line

        Returns:
            list: List with output as string
        """
        buffer = []
        if self.os_type == self.HUAWEI or self.os_type == self.HP:
            if cmd == "system":
                self.prompt = "]"
            elif cmd == "return":
                self.prompt = ">"

        cmd = cmd.strip()
        self.channel.send(cmd + "\n")
        try:
            buffer = self._read_char()
        except Exception as e:
            logger.error(f"[PYNET-SSH]: Couldn't send {cmd} to {self.host} - {e}" % (self.host, cmd, e))
            pass    # === Rarely the device wouldn't answer to the cmd, prevent main program from crashing
        return buffer
