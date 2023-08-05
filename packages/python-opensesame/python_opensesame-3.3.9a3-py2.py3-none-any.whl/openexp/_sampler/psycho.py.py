# coding=utf-8

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
from openexp._sampler.sampler import Sampler
from libopensesame.exceptions import osexception
from libopensesame.oslogging import oslogger


class Psycho(Sampler):

	"""
	desc:
		This is a sampler backend built on top of PyGame.
		For function specifications and docstrings, see
		`openexp._sampler.sampler`.
	"""

	# The settings variable is used by the GUI to provide a list of back-end
	# settings
	settings = {}

	def __init__(self, experiment, src, **playback_args):

		Sampler.__init__(self, experiment, src, **playback_args)
		self.keyboard = Keyboard(experiment)
		self._sound = Sound('A')

	def adjust_pitch(self, p):

		pass

	def adjust_pan(self, p):

		pass

	@configurable
	def play(self, **playback_args):

		pass

	def stop(self):

		pass

	def pause(self):

		pass

	def resume(self):

		pass

	def is_playing(self):

		pass

	def wait(self):

		pass

	@staticmethod
	def init_sound(experiment):

		pass

	@staticmethod
	def close_sound(experiment):

		pass


# Non PEP-8 alias for backwards compatibility
psycho = Psycho


from psychopy import prefs
prefs.hardware['audioLib'] = ['pyo']
from psychopy.sound import Sound
s = Sound()
print(s)
s.play()
