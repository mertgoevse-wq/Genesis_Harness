import unittest
from security_intelligence.secret_scanner import SecurityIntelligence
class TestSecurityIntelligence(unittest.TestCase):
    def test_scan(self):
        si = SecurityIntelligence()
        res = si.scan_secrets_and_vulnerabilities()
        self.assertEqual(res["security_score"], 100)
if __name__ == "__main__":
    unittest.main()
