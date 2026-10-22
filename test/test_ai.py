import os
import unittest
from unittest.mock import patch
from analyzer import analyze_url
from ai_agent import explain_with_strands

class AITests(unittest.TestCase):
    def test_disabled_by_default(self):
        with patch.dict(os.environ, {'ENABLE_AWS_AI':'0'}):
            with self.assertRaisesRegex(RuntimeError, 'disabled'):
                explain_with_strands(analyze_url('example.com'))
    def test_requires_model_id(self):
        with patch.dict(os.environ, {'ENABLE_AWS_AI':'1', 'BEDROCK_MODEL_ID':''}):
            with self.assertRaisesRegex(RuntimeError, 'BEDROCK_MODEL_ID'):
                explain_with_strands(analyze_url('example.com'))

if __name__ == '__main__':
    unittest.main()
