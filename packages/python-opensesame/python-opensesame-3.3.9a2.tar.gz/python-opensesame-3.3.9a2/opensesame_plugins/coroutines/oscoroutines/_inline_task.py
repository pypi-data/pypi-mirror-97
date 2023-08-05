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
from libopensesame.exceptions import osexception
from oscoroutines._base_task import base_task
import inspect

class inline_task(base_task):

	"""
	desc:
		A task controls the coroutine for a Python generator function.
	"""

	def __init__(self, coroutines, function_name, python_workspace, start_time,
		end_time):

		"""
		desc:
			Constructor.

		arguments:
			function_name:
				desc:	The name of a Python generator function.
				type:	str
			python_workspace:
				desc:	The python-workspace object.
				type:	python_workspace
		"""

		base_task.__init__(self, coroutines, start_time, end_time)
		self.function_name = function_name
		self.python_workspace = python_workspace

	def launch(self):

		"""See base_task."""

		if self.function_name not in self.python_workspace._globals:
			raise osexception(u'"%s" is not defined' % self.function_name)
		self.coroutine = self.python_workspace._globals[self.function_name]
		if not inspect.isgeneratorfunction(self.coroutine):
			raise osexception(
				u'"%s" is not a generator function' % self.function_name)
		self.coroutines.event('launching %s' % self.coroutine)
		self.coroutine = self.coroutine()
		self.coroutine.send(None)
