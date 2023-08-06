from unittest import TestCase

from cloudshell.cm.customscript.domain.script_configuration import ScriptConfigurationParser
from mock import Mock


class TestScriptConfiguration(TestCase):

    def setUp(self):
        self.api = Mock()
        self.parser = ScriptConfigurationParser(self.api)

    def test_cannot_parse_json_with_not_numeric_timeout(self):
        json = '{"timeoutMinutes":"str"}'
        with self.assertRaises(SyntaxError) as context:
            self.parser.json_to_object(json)
        self.assertIn('Node "timeoutMinutes" must be numeric type.', context.exception.message)

    def test_cannot_parse_json_with_negative_numeric_timeout(self):
        json = '{"timeoutMinutes":-123}'
        with self.assertRaises(SyntaxError) as context:
            self.parser.json_to_object(json)
        self.assertIn('Node "timeoutMinutes" must be greater/equal to zero.', context.exception.message)

    def test_cannot_parse_json_without_repository_details(self):
        json = '{}'
        with self.assertRaises(SyntaxError) as context:
            self.parser.json_to_object(json)
        self.assertIn('Missing "repositoryDetails" node.', context.exception.message)

    def test_cannot_parse_json_without_repository_url(self):
        json = '{"repositoryDetails":{}}'
        with self.assertRaises(SyntaxError) as context:
            self.parser.json_to_object(json)
        self.assertIn('Missing/Empty "repositoryDetails.url" node.', context.exception.message)

    def test_cannot_parse_json_with_an_empty_repository_url(self):
        json = '{"repositoryDetails":{"url":""}}'
        with self.assertRaises(SyntaxError) as context:
            self.parser.json_to_object(json)
        self.assertIn('Missing/Empty "repositoryDetails.url" node.', context.exception.message)

    def test_cannot_parse_json_without_hosts_detalis(self):
        json = '{"repositoryDetails":{"url":"someurl"}}'
        with self.assertRaises(SyntaxError) as context:
            self.parser.json_to_object(json)
        self.assertIn('Missing/Empty "hostsDetails" node.', context.exception.message)

    def test_cannot_parse_json_with_empty_host_detalis(self):
        json = '{"repositoryDetails":{"url":"someurl"},"hostsDetails":[]}'
        with self.assertRaises(SyntaxError) as context:
            self.parser.json_to_object(json)
        self.assertIn('Missing/Empty "hostsDetails" node.', context.exception.message)

    def test_cannot_parse_json_with_multiple_hosts_detalis(self):
        json = '{"repositoryDetails":{"url":"someurl"},"hostsDetails":[{},{}]}'
        with self.assertRaises(SyntaxError) as context:
            self.parser.json_to_object(json)
        self.assertIn('Node "hostsDetails" must contain only one item.', context.exception.message)

    def test_cannot_parse_json_with_host_without_an_ip(self):
        json = '{"repositoryDetails":{"url":"someurl"},"hostsDetails":[{"someNode":""}]}'
        with self.assertRaises(SyntaxError) as context:
            self.parser.json_to_object(json)
        self.assertIn('Missing/Empty "hostsDetails[0].ip" node.', context.exception.message)

    def test_cannot_parse_json_with_host_with_an_empty_ip(self):
        json = '{"repositoryDetails":{"url":"someurl"},"hostsDetails":[{"ip":""}]}'
        with self.assertRaises(SyntaxError) as context:
            self.parser.json_to_object(json)
        self.assertIn('Missing/Empty "hostsDetails[0].ip" node.', context.exception.message)

    def test_cannot_parse_json_with_host_without_an_connection_method(self):
        json = '{"repositoryDetails":{"url":"someurl"},"hostsDetails":[{"ip":"x.x.x.x"}]}'
        with self.assertRaises(SyntaxError) as context:
            self.parser.json_to_object(json)
        self.assertIn('Missing/Empty "hostsDetails[0].connectionMethod" node.', context.exception.message)

    def test_cannot_parse_json_with_host_with_an_empty_connection_method(self):
        json = '{"repositoryDetails":{"url":"someurl"},"hostsDetails":[{"ip":"x.x.x.x", "connectionMethod":""}]}'
        with self.assertRaises(SyntaxError) as context:
            self.parser.json_to_object(json)
        self.assertIn('Missing/Empty "hostsDetails[0].connectionMethod" node.', context.exception.message)

    def test_sanity(self):
        def wrapIt(x):
            m = Mock()
            m.Value = 'decrypted-' + x
            return m
        self.api.DecryptPassword.side_effect = lambda x: wrapIt(x)
        json = """
{
    "timeoutMinutes": 12.3,
    "repositoryDetails" : {
        "url": "B",
        "username": "C",
        "password": "D"
    },
    "hostsDetails": [{
        "ip": "E",
        "username": "F",
        "password": "G",
        "accessKey": "H",
        "connectionMethod": "IiIiI",
        "parameters": [{"name":"K11","value":"K12"}, {"name":"K21","value":"K22"}]
    }]
}"""
        conf = self.parser.json_to_object(json)
        self.assertEquals(12.3, conf.timeout_minutes)
        self.assertEquals("B", conf.script_repo.url)
        self.assertEquals("C", conf.script_repo.username)
        self.assertEquals("D", conf.script_repo.password)
        self.assertEquals("F", conf.host_conf.username)
        self.assertEquals("decrypted-G", conf.host_conf.password)
        self.assertEquals("decrypted-H", conf.host_conf.access_key)
        self.assertEquals("iiiii", conf.host_conf.connection_method)
        self.assertItemsEqual('K12', conf.host_conf.parameters['K11'])
        self.assertItemsEqual('K22', conf.host_conf.parameters['K21'])
        self.api.DecryptPassword.assert_any_call('G')
        self.api.DecryptPassword.assert_any_call('H')