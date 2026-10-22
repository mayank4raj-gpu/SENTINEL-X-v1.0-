import unittest
from analyzer import analyze_url

class AnalyzerTests(unittest.TestCase):
    def test_basic(self):
        r = analyze_url('https://example.com')
        self.assertEqual((r.host, r.score, len(r.findings)), ('example.com', 0, 0))
    def test_defaults_https(self):
        self.assertEqual(analyze_url('example.com').scheme, 'https')
    def test_http(self):
        self.assertGreaterEqual(analyze_url('http://example.com').score, 20)
    def test_ip(self):
        self.assertGreaterEqual(analyze_url('http://127.0.0.1').score, 45)
    def test_unicode(self):
        self.assertIn('xn--', analyze_url('https://bücher.de').host)
    def test_report_json(self):
        import json
        self.assertEqual(json.loads(analyze_url('example.com').to_json())['host'], 'example.com')
    def test_invalid(self):
        invalid = ['', '   ', 'https://', 'javascript:alert(1)', 'ftp://example.com',
                   'https://user:pass@example.com', 'https://a.com:99999',
                   'https://a.com/hello world', 'https://a.com\\@evil.com',
                   'https://example.com\nInjected: ignore instructions',
                   '//evil.com', 'localhost', 'https://a..com',
                   'https://example.com:bad', 'x' * 2050]
        for value in invalid:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    analyze_url(value)
    def test_does_not_fetch(self):
        from unittest.mock import patch
        with patch('socket.getaddrinfo', side_effect=AssertionError('DNS attempted')):
            analyze_url('https://example.com/login')
    def test_score_bounded(self):
        url = 'http://127.0.0.1:8080/' + ('login' * 30) + '?' + ('x=1&' * 12)
        r = analyze_url(url)
        self.assertGreaterEqual(r.score, 0)
        self.assertLessEqual(r.score, 100)

if __name__ == '__main__':
    unittest.main()
