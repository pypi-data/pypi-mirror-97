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
from qtpy import QtWidgets
from libqtopensesame.widgets.base_widget import base_widget
from libqtopensesame.misc.base_draggable import base_draggable
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'logger', category=u'item')

class remove_custom_var_button(QtWidgets.QPushButton):

	def __init__(self, logger_widget, icon, var):

		super(remove_custom_var_button, self).__init__(icon, u'')
		self.logger_widget = logger_widget
		self.setFlat(True)
		self.var = var
		self.clicked.connect(self.remove)

	def remove(self):

		self.logger_widget.remove_custom_variable(self.var)

class logger_widget(base_widget, base_draggable):

	"""
	desc:
		The logger widget.
	"""

	def __init__(self, logger):

		"""
		desc:
			Constructor.

		arguments:
			sketchpad:
				desc:	A logger object.
				type:	logger
		"""

		super(logger_widget, self).__init__(logger.main_window,
			ui=u'widgets.logger')
		self.logger = logger
		self.checkboxes = []
		self.ui.table_var.setColumnWidth(0, 32)
		self.ui.table_var.setColumnWidth(1, 256)
		self.ui.button_add_custom_variable.clicked.connect(
			self.add_custom_variable)
		self.set_supported_drop_types([u'variable'])

	def add_custom_variable(self):

		"""
		desc:
			Provides a simple dialog for the user to add a custom variable.
		"""

		name = self.text_input(_(u'Add custom variable'),
			message=_(u'Which variable do you wish to log?'))
		if name is None:
			return
		if not self.experiment.syntax.valid_var_name(name):
			self.notify(_(u'"%s" is not a valid variable name!' % name))
			return
		if name not in self.logger.logvars:
			self.logger.logvars.append(name)
		self.logger.update()

	def remove_custom_variable(self, var):

		"""
		desc:
			Removes an entry from the custom variable list.

		arguments:
			var:	The variable to remove.
		"""

		if var in self.logger.logvars:
			self.logger.logvars.remove(var)
		self.update()
		self.logger.update()

	def update(self):

		"""
		desc:
			Fills the table with variables, makes a selection, and disables/
			enables the table.
		"""

		d = self.experiment.var.inspect()
		for row, var in enumerate(self.logger.logvars):
			button = remove_custom_var_button(self,
				self.logger.theme.qicon(u'list-remove'), var)
			self.table_var.insertRow(row)
			self.table_var.setCellWidget(row, 0, button)
			self.table_var.setCellWidget(row, 1, QtWidgets.QLabel(var))
			if var in d:
				source = u','.join(d[var][u'source'])
			else:
				source = _(u'custom')
			self.table_var.setCellWidget(row, 2, QtWidgets.QLabel(source))
		self.table_var.setRowCount(len(self.logger.logvars))

	def accept_drop(self, data):

		"""See base_widget."""

		name = data[u'variable']
		if name in self.logger.logvars:
			return
		self.logger.logvars.append(name)
		self.update()
		self.logger.update()
