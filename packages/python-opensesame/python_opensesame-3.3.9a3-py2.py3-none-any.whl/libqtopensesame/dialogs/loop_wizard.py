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
from libqtopensesame.misc.config import cfg
from libqtopensesame.dialogs.base_dialog import base_dialog
from datamatrix import DataMatrix, operations
from qdatamatrix import QDataMatrix
import pickle
from qtpy import QtWidgets

class loop_wizard(base_dialog):

	"""
	desc:
		The loop-wizard dialog
	"""

	def __init__(self, main_window):

		"""
		desc:
			Constructor.

		arguments:
			main_window:	The main window object.
		"""

		super(loop_wizard, self).__init__(main_window,
			ui=u'dialogs.loop_wizard_dialog')
		try:
			self._dm = pickle.loads(cfg.loop_wizard)
			assert(isinstance(self._dm, DataMatrix))
			assert(hasattr(self._dm._rowid, u'clone'))
		except:
			self._dm = DataMatrix(length=0)
		self._qdm = QDataMatrix(self._dm)
		self.ui.hbox_container.addWidget(self._qdm)
		self.ui.table_example.hide()

	def exec_(self):

		"""
		desc:
			Executes the dialog.

		returns:
			The dialog return status.
		"""

		retval = base_dialog.exec_(self)
		if retval == QtWidgets.QDialog.Rejected:
			return None
		self._dm = self._qdm.dm
		cfg.loop_wizard = pickle.dumps(self._dm)
		return operations.fullfactorial(self._dm)
