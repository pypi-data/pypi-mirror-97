#
# Copyright (c) 2015-2019 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_mail.include module

This module is used for Pyramid integration
"""

from pyramid_mailer import IMailer, Mailer


__docformat__ = 'restructuredtext'


def include_package(config):
    """Pyramid package include"""

    # add translations
    config.add_translation_dirs('pyams_mail:locales')

    config.scan()

    settings = config.registry.settings
    mailers = settings.get('pyams_mail.mailers')
    if mailers:
        for prefix in mailers.split():
            config.registry.registerUtility(Mailer.from_settings(settings, prefix), IMailer,
                                            name=settings['{0}name'.format(prefix)])
