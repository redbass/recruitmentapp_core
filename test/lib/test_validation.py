from lib.validation import validate_email
from test import UnitTestCase


class TestEmailValidation(UnitTestCase):
    valid_emails = [
        'email@example.com',
        'firstname.lastname@example.com',
        'email@subdomain.example.com',
        'firstname+lastname@example.com',
        'email@123.123.123.123',
        'email@[123.123.123.123]',
        '"email"@example.com',
        '1234567890@example.com',
        'email@example-one.com',
        '_______@example.com',
        'email@example.name',
        'email@example.museum',
        'email@example.co.jp',
        'firstname-lastname@example.com',

        'much."more\\ unusual"@example.com',
        'very.unusual."@".unusual.com@example.com'
    ]
    invalid_emails = [
        'plainaddress',
        '#@%^%#$@#$@#.com',
        '@example.com',
        'email.example.com'
    ]

    def test_validate_email_with_valid_emails(self):
        for email in self.valid_emails:
            self.assertTrue(validate_email(email),
                            'The `{email}` is not valid'.format(email=email))

    def test_validate_email_with_invalid_emails(self):
        for email in self.invalid_emails:
            self.assertFalse(validate_email(email),
                             'The `{email}` is valid'.format(email=email))
