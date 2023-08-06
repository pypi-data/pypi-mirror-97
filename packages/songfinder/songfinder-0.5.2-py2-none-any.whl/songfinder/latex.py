# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import division

import os
import errno
import shutil
import codecs
#~ import subprocess
import random
import traceback
import logging

try:
	import tkinter as tk
except ImportError:
	import Tkinter as tk
try:
	from PyPDF2 import PdfFileReader
	HAVEPYPDF = True
except ImportError:
	HAVEPYPDF = False


import songfinder
from songfinder import messages as tkMessageBox
from songfinder import messages as tkFileDialog # pylint: disable=reimported
from songfinder import classPaths
from songfinder import fonctions as fonc
from songfinder import commandLine
from songfinder.elements import exports
from songfinder import exception
from songfinder import accords
from songfinder import classSettings as settings
from songfinder import guiHelper

class LatexParam(tk.Frame, object):
	def __init__(self, fenetre, chants_selection, papa, noCompile, screens=None, **kwargs):
		tk.Frame.__init__(self, fenetre, **kwargs)
		with guiHelper.SmoothWindowCreation(fenetre, screens=screens):
			self.grid()
			self.chants_selection = chants_selection
			self.papa = papa
			self.noCompile = noCompile
			self.settingName = 'SettingsLatex'

			self.deps = {'reorder':[('list', 'non')], \
						'alphabetic_list':[('affiche_liste', 'oui')], \
						'one_song_per_page':[('list', 'non')], \
						'transpose':[('chords', 'oui')], \
						'list':[('affiche_liste', 'oui')], \
						'sol_chords':[('chords', 'oui')], \
						'two_columns':[('affiche_liste', 'oui')], \
						'capo':[('chords', 'oui')], \
						'simple_chords':[('chords', 'oui')], \
						'keep_first':[('chords', 'oui')], \
						'keep_last':[('chords', 'oui'), ('keep_first', 'non')], \
						'diapo':[('reorder', 'non'), ('alphabetic_list', 'non'), \
								('one_song_per_page', 'non'), ('transpose', 'non'), \
								('list', 'non'), ('booklet', 'non'), \
								('two_columns', 'non'), ('capo', 'non'), \
								('simple_chords', 'non'), ('keep_first', 'non'), \
								('keep_last', 'non'), ('sol_chords', 'non'), \
								('one_chorus', 'non'), ('affiche_liste', 'non'), \
								('chords', 'non'), ('keep_first', 'non')], \
						}

			self.dictParam = {'Reordonner les chants pour remplir les pages.':'reorder', \
								'Sommaire alphabetic.':'alphabetic_list', \
								'Afficher un chant par page.':'one_song_per_page',\
								'Transposer les accords.':'transpose',\
								'Afficher les accords.':'chords',\
								'Liste des chants seule.':'list',\
								'Accords en français.':'sol_chords',\
								'Format carnet imprimable.':'booklet',\
								'Refaire les sauts de lignes.':'saut_lignes',\
								"Afficher qu'un seul refrain/pont par chants.":'one_chorus',\
								"Ignorer les diapos optionelles.":'ignore',\
								"Afficher le sommaire.":'affiche_liste',\
								"Afficher le sommaire sur deux collones.":'two_columns',\
								"Appliquer les capo.":'capo',\
								"Simplifier les accords (retire sus4, Maj6 etc.).":'simple_chords',\
								"Ne garder que le premier accord (Do/Mi -> Do).":'keep_first',\
								"Ne garder que le second accord (Do/Mi -> Mi).":'keep_last',\
								"Diaporama.":'diapo',\
								}
			self.dictValeurs = dict()
			self.dictButton = dict()
			self.pressed = None
			nb_boutton = len(self.dictParam)
			column_width = 5
			nb_row = (nb_boutton+1)//2
			for i, (param, item) in enumerate(self.dictParam.items()):
				var = tk.IntVar()
				button = tk.Checkbutton(self, text=param, variable=var, \
									# ~ command=self.save)
									command = lambda identifyer=item: self.save(identifyer))
				self.dictValeurs[param] = var
				self.dictButton[item] = button
				# ~ self.liste_buttons.append(button)
				column_num = i//nb_row * (column_width + 1)
				button.grid(row=i%nb_row, column=column_num, columnspan=column_width, sticky='w' )

			self.bouton_ok = tk.Button(self, text='OK', command=self.createFiles)
			self.bouton_ok.grid(row=nb_row, column=0, columnspan=column_width//2, sticky='w' )
			self.bouton_ok = tk.Button(self, text='Annuler', command=self.quit)
			self.bouton_ok.grid(row=nb_row, column=column_width//2, columnspan=column_width//2, sticky='w' )

			self.maj()

	def save(self, identifyer, event=0): # pylint: disable=unused-argument
		self.pressed = identifyer
		for param, valeur in self.dictValeurs.items():
			if valeur.get():
				str_valeur = 'oui'
			else:
				str_valeur = 'non'
			settings.LATEXSETTINGS.set('Export_Parameters', self.dictParam[param], str_valeur)
			if settings.LATEXSETTINGS.get('Export_Parameters', 'booklet') == 'oui' \
				and not HAVEPYPDF:
				settings.LATEXSETTINGS.set('Export_Parameters', 'booklet', 'non')
				tkMessageBox.showinfo('Info', 'pypdf2 is not installed, this fonctionality is not available. '
										'Run "pip install pypdf2" to install it.')

		self.maj()

	def maj(self):
		for param in self.dictParam.values():
			if settings.LATEXSETTINGS.get('Export_Parameters', param) == 'oui':
				self.dictButton[param].select()
			else:
				self.dictButton[param].deselect()

		if self.pressed:
			pressedValue = settings.LATEXSETTINGS.get('Export_Parameters', self.pressed)
			if pressedValue == 'oui':
				if self.pressed in self.deps:
					for condition in self.deps[self.pressed]:
						settings.LATEXSETTINGS.set('Export_Parameters', condition[0], condition[1])
						if condition[1] == 'oui':
							self.dictButton[condition[0]].select()
						else:
							self.dictButton[condition[0]].deselect()

			for param, conditions in self.deps.items():
				for condition in conditions:
					if condition[0] == self.pressed:
						if condition[1] != pressedValue:
							self.dictButton[param].deselect()
							settings.LATEXSETTINGS.set('Export_Parameters', param, condition[1])

	def createFiles(self):
		settings.LATEXSETTINGS.write()
		pdfFile = CreatePDF(self.chants_selection)
		pdfFile.writeFiles()
		close = 0
		if self.noCompile == 0:
			try:
				close = pdfFile.compileLatex()
			except exception.CommandLineError:
				tkMessageBox.showerror('Erreur', traceback.format_exc())
		if close == 0:
			self.quit()
		else:
			self.papa.liftLatexWindow()

	def quit(self):
		self.papa.closeLatexWindow()


class CreatePDF(object):
	def __init__(self, elements_selection):
		if settings.LATEXSETTINGS.get('Export_Parameters', 'diapo') == 'oui':
			self.__prefix = 'genBeamer'
			ClassType = exports.ExportBeamer
		else:
			self.__prefix = 'genCarnet'
			ClassType = exports.ExportLatex

		self.__listLatex = []
		for element in elements_selection:
			newlatex = ClassType(element)
			if newlatex.exportText:
				self.__listLatex.append(newlatex)

		if settings.LATEXSETTINGS.get('Export_Parameters', 'reorder') == 'oui':
			self.__listLatex = reorderLatex(self.__listLatex)

		self.__pdflatex = commandLine.MyCommand('pdflatex')

		self.__chemin = os.path.join(songfinder.__settingsPath__, 'latexTemplates')
		self.__songFolder = os.path.join(self.__chemin, 'songs')
		self.__songList = os.path.join(self.__chemin, 'listeChants.tex')
		self.__tableOfContent = os.path.join(self.__chemin, 'sommaire.tex')
		self.__bookletizer = os.path.join(self.__chemin, 'bookletizer.tex')
		self.__tmpName = os.path.join(self.__chemin, self.__prefix + '.pdf')

		self.__checkFiles()

	def __getTableOfContent(self):
		text = ''
		if settings.LATEXSETTINGS.get('Export_Parameters', 'affiche_liste') == 'oui':
			# Liste sommaire
			dicoTitres = {latexElem.title:str(self.__listLatex.index(latexElem)+1) \
							for latexElem in self.__listLatex}
			# Alphabetic
			if settings.LATEXSETTINGS.get('Export_Parameters', 'alphabetic_list') == 'oui':
				listTitres = sorted(dicoTitres.keys())
			else:
				listTitres = [latexElem.title for latexElem in self.__listLatex]

			text = '\\section*{Le Turf Auto}\n\\label{sommaire}\n'
			for title in listTitres:
				# Tonalite
				elem = self.__listLatex[ int(dicoTitres[title])-1 ]
				if settings.LATEXSETTINGS.get('Export_Parameters', 'chords') == 'oui':
					chord = accords.Accords(elem.key, \
											transposeNb=elem.transpose, \
											capo=elem.capo)
					key = chord.getChords()[0]
					if key != '':
						key = '~--~\\emph{%s}'%elem.escape(key)
				else:
					key = ''

				text = '%s\\contentsline{section}{%s%s \\dotfill}{%s}{section.%s}\n'\
							%(text, elem.escape(title), key, dicoTitres[title], dicoTitres[title])

			if settings.LATEXSETTINGS.get('Export_Parameters', 'two_columns') == 'oui':
				text = '\\begin{multicols}{2}\n%s\n\\end{multicols}'%text
		return text

	def __getSongList(self):
		text = '\\newcommand{\\songsPath}{%s}\n'%self.__songFolder.replace('\\', '/')
		if settings.LATEXSETTINGS.get('Export_Parameters', 'list') == 'non':
			for i, latexElem in enumerate(self.__listLatex):
				text = '%s\\input{\\songsPath/"%s"}\n'%(text, latexElem.nom)
				if (i+1)%99 == 0:
					text = '%s\\clearpage\n'%text
		text = text.replace('#', '\\#')
		return text

	def __getBookletizer(self):
		# Get number of pages of original pdf file
		with open(self.__tmpName,'rb') as fileIn:
			numPage = PdfFileReader(fileIn).getNumPages()
		numPage = (numPage//4 + 1) * 4
		# Write bookletizer tex file
		text = """\\documentclass[a4paper]{article}
\\usepackage{pdfpages}
\\begin{document}
\\includepdf[pages=-, nup=1x2, signature*=%s, landscape,
angle=180, delta=0 1cm]{%s}
\\end{document}"""%(numPage, self.__tmpName.replace('\\', '/'))
		return text

	def writeFiles(self):
		# List of song to import
		with codecs.open(self.__songList, 'w', encoding='utf-8') as out:
			out.write(self.__getSongList())
		# Songs
		if settings.LATEXSETTINGS.get('Export_Parameters', 'list') == 'non':
			for latexElem in self.__listLatex:
				fileName = os.path.join(self.__songFolder, latexElem.nom + '.tex')
				with codecs.open(fileName, 'w', encoding='utf-8') as out:
					out.write(latexElem.exportText)
		# Table of content
		with codecs.open(self.__tableOfContent, 'w', encoding='utf-8') as out:
			out.write(self.__getTableOfContent())

	def __checkFiles(self):
		try:
			os.makedirs(self.__chemin)
		except (OSError, IOError) as error:
			if error.errno == errno.EEXIST:
				pass
			else:
				raise
		try:
			os.makedirs(self.__songFolder)
		except (OSError, IOError) as error:
			if error.errno == errno.EEXIST:
				pass
			else:
				raise
		source = os.path.join(songfinder.__dataPath__, 'latexTemplates')
		for item in os.listdir(source):
			if os.path.isfile( os.path.join(source, item) ):
				sourceFile = os.path.join(source, item)
				currentFile = os.path.join(self.__chemin, item)
				if not os.path.isfile( currentFile ) \
					or os.stat(sourceFile).st_mtime > os.stat(currentFile).st_mtime:
					shutil.copy(sourceFile, currentFile)

	def __getOutFile(self):
		defaultName = 'turfAuto'
		defaultPath = classPaths.PATHS.pdf
		if settings.LATEXSETTINGS.get('Export_Parameters', 'reorder') == 'non' and \
			settings.LATEXSETTINGS.get('Export_Parameters', 'alphabetic_list') == 'non':
			defaultName = fonc.cree_nom_sortie()
		self.pdfName = tkFileDialog.asksaveasfilename(initialdir=defaultPath, \
										initialfile=defaultName, defaultextension=".pdf", \
										filetypes=(("pdf file", "*.pdf"),("All Files", "*.*") ))

	def compileLatex(self):
		self.__getOutFile()
		if not self.pdfName:
			return 1
		fileToCompile = os.path.join(self.__chemin, self.__prefix + '.tex')
		# Compile
		self.__pdflatex.checkCommand()
		os.chdir(self.__chemin)
		code, out, err = self.__pdflatex.run(options=['-interaction=nonstopmode', \
												fileToCompile])
		if code == 0:
			code, out, err = self.__pdflatex.run(options=['-interaction=nonstopmode', \
												fileToCompile])
		os.chdir(songfinder.__chemin_root__)
		if code != 0:
			tkMessageBox.showerror('Attention', 'Error while '
						'compiling latex files.\n Error %s:\n%s'%(str(code), err))
			return 1
		# Compile booklet
		if settings.LATEXSETTINGS.get('Export_Parameters', 'booklet') == 'oui':
			# Write bookletizer file
			with codecs.open(self.__bookletizer,'w', encoding='utf-8') as out:
				out.write(self.__getBookletizer())
			os.chdir(self.__chemin)
			code, out, err = self.__pdflatex.run(options=['-interaction=nonstopmode', \
												self.__bookletizer])
			os.chdir(songfinder.__chemin_root__)
			if code != 0:
				tkMessageBox.showerror('Attention', 'Error while '
							'compiling latex files.\n Error %s:\n%s'%(str(code), err))
			else:
				self.__tmpName = os.path.join(self.__chemin, 'bookletizer.pdf')

		# Move file to specified directory
		shutil.move(self.__tmpName, self.pdfName)
		logging.info('Succes creating pdf file')
		self.__cleanDir()
		self.__openFile()
		return 0

	def __openFile(self):
		if os.path.isfile(self.pdfName):
			if tkMessageBox.askyesno('Confirmation', 'Le fichier "%s" '
									'à été créé.\nVoulez-vous l\'ouvrire ?'\
									%self.pdfName.decode('utf-8')):
				commandLine.run_file(self.pdfName)

	def __cleanDir(self):
		listExt = ['.aux', '.idx', '.ilg', '.ind', '.log', '.out', '.toc', '.pdf', '.synctex.gz']
		for root, _, files in os.walk(self.__chemin):
			for fichier in files:
				fullName = os.path.join(root, fichier)
				if fonc.get_ext(fullName) in listExt:
					os.remove(fullName)

def reorderLatex(listLatex):
	# Suprimme les doublons, change le nombre de ligne des chant qui ont le meme
	dictNbLigne = dict()
	for i,elem in enumerate(listLatex):
		nbLigne = elem.nbLine
		if nbLigne in dictNbLigne:
			texte1 = elem.text
			texte2 = listLatex[dictNbLigne[nbLigne]].text
			if texte1 != texte2:
				dictNbLigne[nbLigne - random.randint(1,10**7)*10**(-7)] = i
		else:
			dictNbLigne[nbLigne] = i
	# change les titles identiques
	titles = []
	for elem in listLatex:
		title = elem.title
		if title in titles:
			logging.warning('Two elements have the same title "%s"'%title)
			title = title + '~'
			elem.title = title
		titles.append(title)
	sortedKeys = sorted(dictNbLigne.keys(), reverse=True)
	maxLine = 40
	suptitle = 4
	newKey = []
	nb = len(sortedKeys)
	inList = []
	for i,key in enumerate(sortedKeys):
		if key > maxLine:
			logging.warning('Song "%s" is to big to fit one page, size: %d, max size: %d'\
						%(listLatex[dictNbLigne[key]].title, key, maxLine))
		if i not in inList:
			newKey.append(key)
			inList.append(i)
			addSong(inList, newKey, sortedKeys, maxLine, suptitle, nb, key, i)

	newListe = [ listLatex[i] for i in [dictNbLigne[key] for key in newKey] ]
	return newListe

def addSong(inList, newKey, sortedKeys, maxLine, suptitle, nb, nbLine, i):
	# Add song to list accrding to size of song
	previous = -1
	maxLine  = maxLine-suptitle
	for j,key in enumerate(reversed(sortedKeys)):
		if nbLine + key > maxLine or i == nb-j-1:
			if previous != -1:
				if nb-j not in inList:
					newKey.append(previous)
					inList.append(nb-j)
					newNbLine = nbLine + previous
				else:
					newNbLine = nbLine
					maxLine  = maxLine+suptitle
				addSong(inList, newKey, sortedKeys, maxLine, suptitle, nb, newNbLine, nb-j)
			break
		previous = key
