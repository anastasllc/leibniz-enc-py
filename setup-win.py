from distutils.core import setup
import py2exe
 
setup(
	windows=['leibnizwx.py'],
	zipfile=None,
	redirect=True,
	filename=None,
	options={
	"py2exe": {	
		'bundle_files': "1"	
	}
	})
