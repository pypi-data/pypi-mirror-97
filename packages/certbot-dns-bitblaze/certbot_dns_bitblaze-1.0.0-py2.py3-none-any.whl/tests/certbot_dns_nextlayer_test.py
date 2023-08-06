import unittest

try:
    import mock
except ImportError:  # pragma: no cover
    from unittest import mock  # type: ignore

from certbot.compat import os
from certbot.plugins import dns_test_common, dns_test_common_lexicon
from certbot.tests import util as test_util
from requests.exceptions import HTTPError

TOKEN = "not42charslong"


class AuthenticatorTest(
    test_util.TempDirTestCase, dns_test_common_lexicon.BaseLexiconAuthenticatorTest
):
    def setUp(self):
        super(AuthenticatorTest, self).setUp()

        from certbot_dns_bitblaze.dns_bitblaze import Authenticator

        path = os.path.join(self.tempdir, "file.ini")
        dns_test_common.write({"bitblaze_token": TOKEN}, path)

        self.config = mock.MagicMock(
            bitblaze_credentials=path, bitblaze_propagation_seconds=0
        )  # don't wait during tests

        self.auth = Authenticator(self.config, "bitblaze")

        self.mock_client = mock.MagicMock()
        self.auth._get_bbdns_client = mock.MagicMock(return_value=self.mock_client)


class BitblazeLexiconClientTest(
    unittest.TestCase, dns_test_common_lexicon.BaseLexiconClientTest
):

    LOGIN_ERROR = HTTPError("401 Client Error: Unauthorized for url: ...")

    def setUp(self):
        from certbot_dns_bitblaze.dns_bitblaze import _BBDNSLexiconClient

        self.client = _BBDNSLexiconClient(TOKEN)

        self.provider_mock = mock.MagicMock()
        self.client.provider = self.provider_mock


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
