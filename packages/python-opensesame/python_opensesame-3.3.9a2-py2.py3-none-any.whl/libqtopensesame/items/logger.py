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
from libopensesame.logger import logger as logger_runtime
from libqtopensesame.items.qtplugin import qtplugin
from libqtopensesame.widgets.logger_widget import logger_widget
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'logger', category=u'item')

class logger(logger_runtime, qtplugin):

	"""
	desc:
		GUI controls for the logger item.
	"""

	description = _(u'Logs experimental data')
	help_url = u'manual/logging'
	lazy_init = True

	def __init__(self, name, experiment, string=None):

		"""See item."""

		logger_runtime.__init__(self, name, experiment, string)
		qtplugin.__init__(self)

	def init_edit_widget(self):

		"""See qtitem."""

		super(logger, self).init_edit_widget(stretch=False)
		self.logger_widget = logger_widget(self)
		self.add_widget(self.logger_widget)
		self.auto_add_widget(self.logger_widget.ui.checkbox_auto_log,
			u'auto_log')

	def edit_widget(self):

		"""See qtitem."""

		super(logger, self).edit_widget()
		for item in self.experiment.items.values():
			if item.item_type == self.item_type and item is not self:
				self.extension_manager.fire(u'notify',
					message=_(u'You have multiple unlinked loggers. This can lead to messy log files.'),
					category=u'warning')
				break
		self.logger_widget.update()

	def apply_edit_changes(self):

		"""See qtitem."""

		super(logger, self).apply_edit_changes()
		self.logger_widget.update()
