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

"""PyAMS_mail.interfaces module

This module provides IPrincipalMailInfo, which can return email address(es) or any principal,
if the authentication plug-in provides this information.
"""

from zope.interface import Interface


MAILERS_VOCABULARY_NAME = 'pyams_mail.mailers'


class IPrincipalMailInfo(Interface):
    """Principal mail informations interfaces"""

    def get_addresses(self):
        """Get list of mail addresses matching adapted principal

        As adapted principal can be a group, result should be a list of
        tuples containing name and address of each group member.
        """
