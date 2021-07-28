from core.commands import _fs_implements
from fman.url import splitscheme, join, basename, relpath, normalize
from fman import DirectoryPaneCommand, show_prompt, _get_app_ctxt
from fman.fs import touch

def get_fs_scheme(pane):
	return splitscheme(pane.get_path())[0]


class CreateFile(DirectoryPaneCommand):
	aliases = ('New file', 'Create file')

	def __call__(self):
		file_under_cursor = self.pane.get_file_under_cursor()
		if file_under_cursor:
			default = basename(file_under_cursor)
		else:
			default = ''
		name, ok = show_prompt("New file", default)
		if ok and name:
			base_url = self.pane.get_path()
			# import ipdb; ipdb.set_trace()
			touch(join(base_url, name))
			self.set_cursor(base_url, name)

	def set_cursor(self, base_url, name):
		dir_url = join(base_url, name)
		effective_url = normalize(dir_url)
		select = relpath(effective_url, base_url).split('/')[0]
		if select != '..':
			try:
				self.pane.place_cursor_at(join(base_url, select))
			except ValueError as dir_disappeared:
				pass

	def is_visible(self):
		return True
