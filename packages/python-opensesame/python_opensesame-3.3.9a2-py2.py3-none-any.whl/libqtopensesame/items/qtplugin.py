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
import os
from libopensesame import plugins
from libopensesame.oslogging import oslogger
from qtpy import QtGui, QtCore, QtWidgets
from libqtopensesame.items import qtitem
from libqtopensesame.widgets import color_edit
from libopensesame import misc
from libopensesame.oslogging import oslogger
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'qtplugin', category=u'core')


class qtplugin(qtitem.qtitem):

	"""Provides basic functionality for plugin GUIs"""

	def __init__(self, plugin_file=None):

		"""
		desc:
			Constructor.

		arguments:
			plugin_file:	The location of the plugin script file.
		"""

		if plugin_file is not None:
			# The __file__ variable is generally a str, which will cause unicode
			# errors. Therefore, convert this here if necessary.
			plugin_file = safe_decode(plugin_file,
				enc=misc.filesystem_encoding())
			# These lines makes sure that the icons and help file are recognized
			# by OpenSesame.
			self.plugin_folder = os.path.dirname(plugin_file)
			for ext in [u'.html', u'.md']:
				basename = self.item_type + ext
				path = os.path.join(self.plugin_folder, basename)
				if os.path.exists(path):
					self.experiment.resources[basename] = path
			# Install a translation file if there is one. Most plugins have
			# their translations as part of the OpenSesame main translations.
			# However, separate plugins can bring their own translation.
			translation_file = os.path.join(self.plugin_folder, u'resources',
				u'locale', u'%s.qm' % self.main_window._locale)
			if os.path.exists(translation_file):
				translator = QtCore.QTranslator()
				translator.load(translation_file)
				QtCore.QCoreApplication.installTranslator(translator)
			self.init_item_icon()
		else:
			self.qicon = None
		self.lock = False
		qtitem.qtitem.__init__(self)

	def init_item_icon(self):

		icon = plugins.plugin_property(self.item_type, u'icon', default=None)
		if icon is not None:
			self.qicon = self.theme.qicon(icon)
			return
		icon16 = os.path.join(
			self.plugin_folder, u'%s.png' % self.item_type)
		icon32 = os.path.join(
			self.plugin_folder, u'%s_large.png' % self.item_type)
		self.experiment.resources[u'%s.png' % self.item_type] = icon16
		self.experiment.resources[u'%s_large.png' % self.item_type] = icon32
		self.qicon = QtGui.QIcon()
		self.qicon.addFile(icon16, QtCore.QSize(16,16))
		self.qicon.addFile(icon32, QtCore.QSize(32,32))

	def item_icon(self):

		"""
		returns:
			desc:	The name of the item icon.
			type:	unicode
		"""

		if self.qicon is not None:
			return self.qicon
		return self.item_type

	def edit_widget(self):

		"""
		desc:
			Updates the GUI controls.
		"""
		
		qtitem.qtitem.edit_widget(self)
		self.auto_edit_widget()

	def add_control(self, label, widget, tooltip=None, min_width=200,
		info=None):

		"""
		desc:
			Adds a generic control QWidget.

		arguments:
			label:	A text label.
			widget:	A QWidget.

		keywords:
			tooltip:	A tooltip text.
			min_width:	A minimum width for the widget.
			info:		Additional info, to be presented to the right of the
						control.
		"""

		if tooltip is not None:
			try:
				widget.setToolTip(tooltip)
			except:
				pass
		if isinstance(min_width, int):
			widget.setMinimumWidth(min_width)
		row = self.edit_grid.rowCount()
		label = QtWidgets.QLabel(label)
		label.setAlignment(self.edit_grid.labelAlignment())
		if info is None:
			self.edit_grid.insertRow(row, label, widget)
		else:
			hbox = QtWidgets.QHBoxLayout()
			hbox.setContentsMargins(0,0,0,0)
			hbox.setSpacing(12)
			hbox.addWidget(widget)
			info = QtWidgets.QLabel(info)
			info.setObjectName(u'control-info')
			hbox.addWidget(info)
			container = QtWidgets.QWidget()
			container.setLayout(hbox)
			self.edit_grid.insertRow(row, label, container)
		self.set_focus_widget(widget)

	def add_line_edit_control(self, var, label, validator=None, **kwdict):

		"""
		desc:
			Adds a QLineEdit control that is linked to a variable.

		arguments:
			var:	The associated variable.
			label:	The label text.

		keywords:
			validator:	A validator object.

		keyword-dict:
			kwdict:		A keyword dict to be passed on to add_control().

		returns:
			A QLineEdit widget.
		"""

		edit = QtWidgets.QLineEdit()
		edit.editingFinished.connect(self.apply_edit_changes)
		edit.textEdited.connect(self.set_dirty)
		edit.setMinimumWidth(200)
		if validator is not None:
			edit.setValidator(validator)
		self.add_control(label, edit, **kwdict)
		if var is not None:
			self.auto_line_edit[var] = edit
		return edit

	def add_checkbox_control(self, var, label, **kwdict):

		"""
		desc:
			Adds a QCheckBox control that is linked to a variable.

		arguments:
			var:	The associated variable.
			label:	The label text.

		keyword-dict:
			kwdict:		A keyword dict to be passed on to add_control().

		returns:
			A QCheckBox widget.
		"""

		checkbox = QtWidgets.QCheckBox(label)
		checkbox.clicked.connect(self.apply_edit_changes)
		self.add_control(u'', checkbox, **kwdict)
		if var is not None:
			self.auto_checkbox[var] = checkbox
		return checkbox

	def add_color_edit_control(self, var, label, **kwdict):

		"""
		desc:
			Adds a color_edit control.

		arguments:
			var:	The associated variable.
			label:	The label text.

		keyword-dict:
			kwdict:		A keyword dict to be passed on to add_control().

		returns:
			A color_edit widget.
		"""

		edit = color_edit.color_edit(self.main_window)
		edit.setMinimumWidth(200)
		edit.initialize(self.experiment)
		edit.textEdited.connect(self.apply_edit_changes)
		self.add_control(label, edit, **kwdict)
		if var is not None:
			self.auto_line_edit[var] = edit
		return edit

	def add_combobox_control(self, var, label, options, **kwdict):

		"""
		desc:
			Adds a QComboBox control that is linked to a variable.

		arguments:
			var:		The associated variable.
			label:		The label text.
			options:	A list of options.

		keyword-dict:
			kwdict:		A keyword dict to be passed on to add_control().

		returns:
			A QComboBox widget.
		"""

		combobox = QtWidgets.QComboBox()
		combobox.setMinimumWidth(200)
		for o in options:
			combobox.addItem(o)
		combobox.activated.connect(self.apply_edit_changes)
		self.add_control(label, combobox, **kwdict)
		if var is not None:
			self.auto_combobox[var] = combobox
		return combobox

	def add_doublespinbox_control(self, *args, **kwdict):

		"""
		desc:
			Adds a QDoubleSpinBox. See _add_spinbox_control().
		"""

		return self._add_spinbox_control(QtWidgets.QDoubleSpinBox, *args,
			**kwdict)

	def add_spinbox_control(self, *args, **kwdict):

		"""
		desc:
			Adds a QSpinBox. See _add_spinbox_control().
		"""

		return self._add_spinbox_control(QtWidgets.QSpinBox, *args, **kwdict)

	def _add_spinbox_control(self, cls, var, label, min_val, max_val,
		prefix=u'', suffix=u'', **kwdict):

		"""
		desc:
			Adds a QSpinBox or QDoubleSpinBox control that is linked to a
			variable.

		arguments:
			var:		The associated variable.
			label:		The label text.
			min_val:	A minimum value.
			max_val:	A maximum value.

		Keyword arguments:
			prefix:		A prefix text.
			suffix:		A suffix text.

		keyword-dict:
			kwdict:		A keyword dict to be passed on to add_control().

		returns:
			A QSpinBox widget.
		"""

		spinbox = cls()
		spinbox.setMinimum(min_val)
		spinbox.setMaximum(max_val)
		spinbox.editingFinished.connect(self.apply_edit_changes)
		spinbox.valueChanged.connect(self.set_dirty)
		spinbox.setMinimumWidth(200)
		if prefix != u'':
			spinbox.setPrefix(prefix)
		if suffix != u'':
			spinbox.setSuffix(suffix)
		self.add_control(label, spinbox, **kwdict)
		if var is not None:
			self.auto_spinbox[var] = spinbox
		return spinbox

	def add_slider_control(self, var, label, min_val, max_val, left_label=u'',
		right_label=u'', **kwdict):

		"""
		Adds a QSlider control that is linked to a variable.

		arguments:
			var:		The associated variable.
			label:		The label text.
			min_val:	A minimum value.
			max_val:	A maximum value.

		Keyword arguments:
			left_label:		A label for the left side.
			right_label:	A label for the right side.

		keyword-dict:
			kwdict:		A keyword dict to be passed on to add_control().

		returns:
			A QSlider widget.
		"""

		slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
		slider.setFocusPolicy(QtCore.Qt.NoFocus)
		slider.setGeometry(30, 40, 100, 30)
		slider.setRange(min_val, max_val)
		slider.setSingleStep(1000)
		#Take care of layout
		layout = QtWidgets.QHBoxLayout()
		layout.setMargin(0)
		layout.setSpacing(5)
		if left_label:
			llabel = QtWidgets.QLabel()
			llabel.setText(left_label)
			layout.addWidget(llabel)
		layout.addWidget(slider)
		if right_label:
			rlabel = QtWidgets.QLabel()
			rlabel.setText(right_label)
			layout.addWidget(rlabel)
		slider.sliderMoved.connect(self.apply_edit_changes)
		if var is not None:
			self.auto_slider[var] = slider
		widget = QtWidgets.QWidget()
		widget.setLayout(layout)
		self.add_control(label, widget, **kwdict)
		return slider

	def add_filepool_control(self, var, label, **kwdict):

		"""
		desc:
			Adds a control to select a file from the file pool, and is linked to
			a variable.

		arguments:
			var:		The associated variable.
			label:		The label text.

		keywords:
			click_func:	A custom function to be called when a file is selected.
						If no click_func is specified, file selection will be
						handled automatically. (default=None)

		keyword-dict:
			kwdict:		A keyword dict to be passed on to add_control().

		returns:
			A pool_select widget that contains the path of the selected file.
		"""

		from libqtopensesame._input.pool_select import pool_select
		edit = pool_select(self.main_window)
		edit.editingFinished.connect(self.apply_edit_changes)
		if var is not None:
			self.auto_line_edit[var] = edit
		self.add_control(label, edit, **kwdict)
		return edit

	def add_editor_control(self, var, label, syntax=False):

		"""
		Adds an editor that is linked to a variable.

		arguments:
			var:		The associated variable.
			label:		The label text.

		keywords:
			syntax:		A boolean indicating whether Python syntax highlighting
						should be activated.

		returns:
			An editor widget.
		"""

		if syntax:
			from pyqode_extras.widgets import PythonCodeEdit as CodeEdit
		else:
			from pyqode_extras.widgets import TextCodeEdit as CodeEdit
		editor = CodeEdit(self.main_window)
		editor.focusOutEvent = self._editor_focus_out
		if var is not None:
			self.auto_editor[var] = editor
		# This is a horrible hack to avoid the situation in which newly created
		# editors are closed on the open_experiment event, which should only
		# close editors linked to the old experiment. This only affects editors
		# that bypass the lazy-init system, and for these editors the close()
		# function should be bypassed exactly once.
		if not self.lazy_init:
			def ignore_close_once(editor):
				def inner():
					oslogger.debug(
						'ignoring close() once for {}'.format(editor)
					)
					editor.close = orig_close
				orig_close = editor.close
				return inner	
			editor.close = ignore_close_once(editor)
		self.edit_vbox.addWidget(editor)
		self.set_focus_widget(editor)
		self.extension_manager.fire(u'register_editor', editor=editor)
		return editor

	def _editor_focus_out(self, event):

		self.apply_edit_changes()

	def add_text(self, msg):

		"""
		desc:
			Adds a non-interactive QLabel for description purposes.

		arguments:
			msg:	A text message.

		returns:
			A QLabel.
		"""

		label = QtWidgets.QLabel(msg)
		label.setWordWrap(True)
		label.setOpenExternalLinks(True)
		self.edit_vbox.addWidget(label)
		return label

	def add_widget(self, w):

		"""
		desc:
			Adds a QWidget to the controls.

		arguments:
			w:
				desc:	A widget.
				type:	QWidget

		returns:
			desc:		The widget.
			type:		QWidget
		"""

		self.edit_vbox.addWidget(w)
		return w

	def add_stretch(self):

		"""
		desc:
			Pads empty space below the controls.
		"""

		self.edit_vbox.addStretch()

	def get_ready(self):

		"""
		desc:
			Applies pending script changes.

		returns:
			True if changes have been made, False otherwise.
		"""

		for var, editor in self.auto_editor.items():
			if editor.dirty:
				oslogger.debug(u'applying pending editor changes')
				self.apply_edit_changes()
				return True
		return qtitem.qtitem.get_ready(self)


QtPlugin = qtplugin
