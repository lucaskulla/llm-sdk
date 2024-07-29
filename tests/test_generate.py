import unittest
import requests
import requests_mock
from ollama.helpers import generate


class TestGenerateFunction(unittest.TestCase):
    @requests_mock.Mocker()
    def test_generate_success(self, mock):
        base_url = 'http://api.example.com'
        model = 'test_model'
        user_prompt = 'Hello, world!'

        # Mock response
        mock.post(f'{base_url}/api/generate', text='''{"response": "Hello, user!", "context": "some context", "done": false}
{"response": "", "context": "final context", "done": true}''')

        full_response, final_context = generate(base_url, model, user_prompt)

        self.assertEqual(full_response, 'Hello, user!')
        self.assertEqual(final_context, 'final context')

    @requests_mock.Mocker()
    def test_generate_error(self, mock):
        base_url = 'http://api.example.com'
        model = 'test_model'
        user_prompt = 'Hello, world!'

        # Mock error response
        mock.post(f'{base_url}/api/generate', status_code=500)

        full_response, final_context = generate(base_url, model, user_prompt)

        self.assertIsNone(full_response)
        self.assertIsNone(final_context)

    @requests_mock.Mocker()
    def test_generate_partial_stream(self, mock):
        base_url = 'http://api.example.com'
        model = 'test_model'
        user_prompt = 'Hello, world!'

        # Mock partial response
        mock.post(f'{base_url}/api/generate', text='''{"response": "Hello,", "context": "some context", "done": false}
{"response": " user!", "context": "final context", "done": true}''')

        full_response, final_context = generate(base_url, model, user_prompt)

        self.assertEqual(full_response, 'Hello, user!')
        self.assertEqual(final_context, 'final context')

    @requests_mock.Mocker()
    def test_generate_with_system_prompt(self, mock):
        base_url = 'http://api.example.com'
        model = 'test_model'
        user_prompt = 'Hello, world!'
        system_prompt = 'System prompt'

        mock.post(f'{base_url}/api/generate',
                  text='''{"response": "System response.", "context": "system context", "done": true}''')

        full_response, final_context = generate(base_url, model, user_prompt, system_prompt=system_prompt)

        self.assertEqual(full_response, 'System response.')
        self.assertEqual(final_context, 'system context')

    @requests_mock.Mocker()
    def test_generate_with_large_input(self, mock):
        base_url = 'http://api.example.com'
        model = 'test_model'
        user_prompt = 'Hello, world! ' * 1000  # Large input

        mock.post(f'{base_url}/api/generate',
                  text='''{"response": "Large response.", "context": "large context", "done": true}''')

        full_response, final_context = generate(base_url, model, user_prompt)

        self.assertEqual(full_response, 'Large response.')
        self.assertEqual(final_context, 'large context')

    @requests_mock.Mocker()
    def test_generate_with_special_characters(self, mock):
        base_url = 'http://api.example.com'
        model = 'test_model'
        user_prompt = 'Hello, world! @$%^&*()'

        mock.post(f'{base_url}/api/generate',
                  text='''{"response": "Special characters response.", "context": "special context", "done": true}''')

        full_response, final_context = generate(base_url, model, user_prompt)

        self.assertEqual(full_response, 'Special characters response.')
        self.assertEqual(final_context, 'special context')

    @requests_mock.Mocker()
    def test_generate_timeout(self, mock):
        base_url = 'http://api.example.com'
        model = 'test_model'
        user_prompt = 'Hello, world!'

        mock.post(f'{base_url}/api/generate', exc=requests.exceptions.Timeout)

        full_response, final_context = generate(base_url, model, user_prompt)

        self.assertIsNone(full_response)
        self.assertIsNone(final_context)

    @requests_mock.Mocker()
    def test_generate_network_error(self, mock):
        base_url = 'http://api.example.com'
        model = 'test_model'
        user_prompt = 'Hello, world!'

        mock.post(f'{base_url}/api/generate', exc=requests.exceptions.ConnectionError)

        full_response, final_context = generate(base_url, model, user_prompt)

        self.assertIsNone(full_response)
        self.assertIsNone(final_context)

    @requests_mock.Mocker()
    def test_generate_invalid_json_response(self, mock):
        base_url = 'http://api.example.com'
        model = 'test_model'
        user_prompt = 'Hello, world!'

        mock.post(f'{base_url}/api/generate', text='Invalid JSON')

        full_response, final_context = generate(base_url, model, user_prompt)

        self.assertIsNone(full_response)
        self.assertIsNone(final_context)


if __name__ == '__main__':
    unittest.main()
