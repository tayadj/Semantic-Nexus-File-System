import setuptools
import os

module = setuptools.Extension(
	"mediator",
	sources = [
		os.path.join("module", "module.c"),
		os.path.join("methods", "atomic", "atomic.c"),
		os.path.join("methods", "composite", "composite.c"),
		os.path.join("objects", "metafile", "metafile.c")
	]
)

setuptools.setup(
	name = "mediator",
	version = "1.0",
	description = "A semantic file system mediator.",
	ext_modules = [module],
)
