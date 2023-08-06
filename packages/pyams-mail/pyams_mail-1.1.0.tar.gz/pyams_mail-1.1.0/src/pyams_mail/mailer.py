#
# Copyright (c) 2008-2015 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_mailer.mailer module

This module provides a vocabulary of registered mailers utilities.
"""

from pyramid_mailer.interfaces import IMailer
from zope.componentvocabulary.vocabulary import UtilityVocabulary

from pyams_mail.interfaces import MAILERS_VOCABULARY_NAME
from pyams_utils.vocabulary import vocabulary_config


__docformat__ = 'restructuredtext'


@vocabulary_config(name=MAILERS_VOCABULARY_NAME)
class MailerVocabulary(UtilityVocabulary):
    """Mailer vocabulary"""

    interface = IMailer
    nameOnly = True
