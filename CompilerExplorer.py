import sublime
import sublime_plugin
import os

class CompilerExplorerActivateCommand(sublime_plugin.TextCommand):
	def run(self, edit, **kwargs):
		self.currentFilePath = kwargs["file"]
		self.tmpFilePath = kwargs["tmpFilePath"]
		sublime.set_timeout_async(lambda: self.run_async())

	def run_async(self):
		currentFileName = os.path.splitext(os.path.basename(self.currentFilePath))[0]
		workingFolders = self.view.window().folders()
		files = []
		for folder in workingFolders:
			for r, d, f in os.walk(folder):
				for file in f:
					if file.endswith('.o'):
						if currentFileName in file:
							files.append(os.path.join(r, file))
		if not len(files):
			print("couldn't find *.o!!!")
			return
		# TODO:
		# If we have more than 1 file result prompt the user to select an obj file
		# elif len(files) > 1:
		# 	print("yeet")
		# 	objFile = None
		# else
		# tmpFilePath = os.path.join(workingFolders[0], "." + currentFileName + ".objdump")
		objFile = files[0]
		# TODO: wrap this in a linux 'watch' command, or try to run when objFile is updated
		cmd = "objdump -dCS {0} | c++filt > {1}".format(objFile, self.tmpFilePath)
		os.system(cmd)

class CompilerExplorerOpenCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.currentFilePath = self.view.window().active_view().file_name()
		# TODO: this is a shitty way to create a tmp file
		self.tmpFilePath = self.currentFilePath + ".objdump"
		compilerExplorerView = sublime.active_window().open_file(self.tmpFilePath)
		compilerExplorerView.set_read_only(True)
		compilerExplorerView.set_scratch(True)
		compilerExplorerView.set_name("Compiler Explorer - " + self.currentFilePath)
		compilerExplorerView.run_command(
			"compiler_explorer_activate",
			{
				"file": self.currentFilePath,
				"tmpFilePath": self.tmpFilePath
			}
			)