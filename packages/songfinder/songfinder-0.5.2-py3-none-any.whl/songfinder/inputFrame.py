# -*- coding: utf-8 -*-
from __future__ import unicode_literals
try:
	import tkinter as tk
except ImportError:
	import Tkinter as tk

def make_method(func, instance):
	return ( lambda *args, **kwargs: func(instance, *args, **kwargs) )

class entryField(tk.Frame, object):
	def __init__(self, parentFrame, width=None, text='', packing=tk.TOP, **kwargs):
		tk.Frame.__init__(self, parentFrame, **kwargs)

		self._text = tk.Label(self, text=text)
		self._input = tk.Entry(self, state=tk.NORMAL, width=width)

		self._text.pack(side=packing)
		self._input.pack(side=packing, fill=tk.X, expand=1)

		for name,_ in tk.Entry.__dict__.items():
			_method = make_method(tk.Entry.__dict__[name], self._input)
			setattr(self, name, _method)
		for name in set(tk.Label.__dict__.keys()) - set(tk.Entry.__dict__.keys()):
			_method = make_method(tk.Label.__dict__[name], self._text)
			setattr(self, name, _method)

	def bind(self, *args, **kwargs): # pylint: disable=arguments-differ
		self._input.bind(*args, **kwargs)

	def focus_set(self, *args, **kwargs): # pylint: disable=arguments-differ
		self._input.focus_set(*args, **kwargs)

class TextField(tk.Frame, object):
	def __init__(self, parentFrame, width=None, text='', packing=tk.TOP, state=tk.NORMAL, **kwargs):
		tk.Frame.__init__(self, parentFrame, **kwargs)

		self._text = tk.Label(self, text=text)
		self._input = tk.Text(self, width=width, height=1, state=state)

		self._text.pack(side=packing)
		self._input.pack(side=packing, fill=tk.X, expand=1)

		for name,_ in tk.Text.__dict__.items():
			_method = make_method(tk.Text.__dict__[name], self._input)
			setattr(self, name, _method)
		for name in set(tk.Label.__dict__.keys()) - set(tk.Text.__dict__.keys()):
			_method = make_method(tk.Label.__dict__[name], self._text)
			setattr(self, name, _method)

	def bind(self, *args, **kwargs): # pylint: disable=arguments-differ
		self._input.bind(*args, **kwargs)

	def focus_set(self, *args, **kwargs): # pylint: disable=arguments-differ
		self._input.focus_set(*args, **kwargs)

	@property
	def state(self):
		return self._input['state']

	@state.setter
	def state(self, value):
		self._input['state'] = value
