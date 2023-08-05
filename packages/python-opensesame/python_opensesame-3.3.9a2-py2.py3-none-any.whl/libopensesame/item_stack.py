#-*- coding:utf-8 -*-

"""
This file is part of OpenSesame.

OpenSesame is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenSesame is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OpenSesame.  If not, see <http://www.gnu.org/licenses/>.
"""

from libopensesame.py3compat import *

class item_stack(object):

	"""
	desc:
		Keeps track of which item is currently active.
	"""

	def __init__(self):

		"""
		desc:
			Constructor.
		"""

		self.clear()

	def clear(self):

		"""
		desc:
			Clears the stack.
		"""

		self.l = []

	def push(self, item, phase):

		"""
		desc:
			Adds a new item to the stack.

		arguments:
			item:
				desc:	The item to add.
				type:	str
		"""

		self.l.append( (item, phase) )

	def pop(self):

		"""
		desc:
			Pops the last item from the stack.

		returns:
			desc:	The popped item.
			type:	str
		"""

		return self.l.pop()

	def __str__(self):

		return '.'.join(['%s[%s]' % i for i in self.l])

	def __unicode__(self):

		return u'.'.join([u'%s[%s]' % i for i in self.l])

# Create a single instance of the stack
item_stack_singleton = item_stack()
