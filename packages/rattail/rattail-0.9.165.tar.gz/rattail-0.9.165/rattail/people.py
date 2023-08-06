# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2021 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
People Handler
"""

from __future__ import unicode_literals, absolute_import

from rattail.util import load_object
from rattail.app import GenericHandler


class PeopleHandler(GenericHandler):
    """
    Base class and default implementation for people handlers.
    """

    def normalize_full_name(self, first, last, **kwargs):
        from rattail.db.util import normalize_full_name
        return normalize_full_name(first, last)

    def update_names(self, person, **kwargs):
        """
        Update name(s) for the given person.

        :param person: Reference to a ``Person`` record.
        :param first: First name for the person.
        :param middle: Middle name for the person.
        :param last: Last name for the person.
        :param full: Full (display) name for the person.
        """
        if 'first' in kwargs:
            person.first_name = kwargs['first']

        if 'middle' in kwargs:
            person.middle_name = kwargs['middle']

        if 'last' in kwargs:
            person.last_name = kwargs['last']

        if 'full' in kwargs:
            if kwargs['full']:
                person.display_name = kwargs['full']
            else:
                person.display_name = self.normalize_full_name(
                    person.first_name, person.last_name)
        elif 'first' in kwargs and 'last' in kwargs:
            person.display_name = self.normalize_full_name(
                person.first_name, person.last_name)


def get_people_handler(config, **kwargs):
    """
    Create and return the configured :class:`PeopleHandler` instance.
    """
    spec = config.get('rattail', 'people.handler')
    if spec:
        factory = load_object(spec)
    else:
        factory = PeopleHandler
    return factory(config, **kwargs)
