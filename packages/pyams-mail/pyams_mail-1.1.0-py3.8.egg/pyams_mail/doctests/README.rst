==================
PyAMS_mail package
==================

Introduction
------------

This package is composed of a set of utility functions, usable into any Pyramid application.

    >>> from pyramid.testing import setUp, tearDown
    >>> config = setUp(hook_zca=True)

We will need a mailer utility afterwards to test this utility registration:

    >>> config.registry.settings['pyams_mail.mailers'] = 'pyams_smtp.'
    >>> config.registry.settings['pyams_smtp.name'] = 'PyAMS test mailer'
    >>> config.registry.settings['pyams_smtp.host'] = 'localhost'
    >>> config.registry.settings['pyams_smtp.port'] = 25

    >>> from cornice import includeme as include_cornice
    >>> include_cornice(config)
    >>> from pyams_utils import includeme as include_utils
    >>> include_utils(config)
    >>> from pyams_mail import includeme as include_mail
    >>> include_mail(config)


Text messages
-------------

A text message is a basic message which provides a unique version of the given text:

    >>> from pyams_mail.message import TextMessage
    >>> body = 'This is the message body.'
    >>> message = TextMessage(subject='Text message',
    ...                       fromaddr='testing@example.com',
    ...                       toaddr='john.doe@example.com',
    ...                       text=body)

    >>> message
    <pyramid_mailer.message.Message object at 0x...>
    >>> message.validate()

    >>> message.subject
    'Text message'
    >>> message.sender
    'testing@example.com'
    >>> message.recipients
    ('john.doe@example.com',)
    >>> message.body
    'This is the message body.'

It can then be converted to an email message which will be used by a mailer utility:

    >>> msg = message.to_message()
    >>> msg
    <email.mime.nonmultipart.MIMENonMultipart object at 0x...>
    >>> msg.is_multipart()
    False
    >>> msg.get_content_type()
    'text/plain'
    >>> sorted(msg.keys())
    ['Content-Disposition', 'Content-Transfer-Encoding', 'Content-Type', 'From', 'MIME-Version', 'Subject', 'To']
    >>> payload = msg.get_payload()
    >>> payload
    'This=20is=20the=20message=20body.'


HTML messages
-------------

An HTML message is a multipart MIME message which provides HTML and text versions of the same
test:

    >>> from pyams_mail.message import HTMLMessage
    >>> body = '<p>This is my message body</p>'
    >>> message = HTMLMessage(subject='Test message',
    ...                       fromaddr='testing@example.com',
    ...                       toaddr='john.doe@example.com',
    ...                       html=body)

    >>> message
    <pyramid_mailer.message.Message object at 0x...>
    >>> message.validate()

    >>> message.subject
    'Test message'
    >>> message.sender
    'testing@example.com'
    >>> message.recipients
    ('john.doe@example.com',)
    >>> message.html
    '<p>This is my message body</p>'
    >>> message.body
    'This is my message body\n'

It can then be converted to an email message which will be used by a mailer utility:

    >>> msg = message.to_message()
    >>> msg
    <email.mime.multipart.MIMEMultipart object at 0x...>
    >>> msg.is_multipart()
    True
    >>> msg.get_content_type()
    'multipart/alternative'
    >>> sorted(msg.keys())
    ['Content-Type', 'From', 'MIME-Version', 'Subject', 'To']
    >>> payload = msg.get_payload()
    >>> payload
    [<...MIMENonMultipart object at 0x...>, <...MIMENonMultipart object at 0x...>]

    >>> part = payload[0]
    >>> part.get_content_type()
    'text/plain'
    >>> part.get_payload(decode=True)
    b'This is my message body\n'
    >>> part.get_charset()
    us-ascii

    >>> part = payload[1]
    >>> part.get_content_type()
    'text/html'
    >>> part.get_payload(decode=True)
    b'<p>This is my message body</p>'
    >>> part.get_charset()
    us-ascii


Getting mailers
---------------

Mailers registration can be done from Pyramid configuration file, as shown at the beginning:

    >>> from pyramid_mailer.interfaces import IMailer
    >>> config.registry.getUtility(IMailer, name='PyAMS test mailer')
    <pyramid_mailer.mailer.Mailer object at 0x...>


Tests cleanup:

    >>> tearDown()
