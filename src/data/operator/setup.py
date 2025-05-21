import setuptools
import os

module = setuptools.Extension(
	"operator",
	sources = [
		os.path.join("module", "module.c"),
		os.path.join("atomic", "create.c"),
		os.path.join("atomic", "read.c"),
	],
	include_dirs = ["atomic", "module"]
)

setuptools.setup(
	name = "operator",
	version = "1.0",
	description = "A semantic file system operator.",
	ext_modules = [module],
)
