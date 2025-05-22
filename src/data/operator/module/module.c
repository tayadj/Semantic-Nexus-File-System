#include "../objects/metafile/metafile.h"
#include "../methods/atomic/atomic.h"

#include <Python.h>



static PyMethodDef operator_methods[] = {
	{"create_file", py_create_file, METH_VARARGS, "Create a file with given id and Metafile object."},
	{"read_file", py_read_file, METH_VARARGS, "Read a file with given id."},
	{"delete_file", py_delete_file, METH_VARARGS, "Delete a file with given id."},
	{NULL, NULL, 0, NULL}
};

static struct PyModuleDef operator_module = {
	PyModuleDef_HEAD_INIT,
	"operator",
	"A semantic file system operator.",
	-1,
	operator_methods
};

PyMODINIT_FUNC PyInit_operator(void) {

	PyObject* pyModule;

	if (PyType_Ready(&PyMetafileType) < 0) {
		return NULL;
	}
		
	pyModule = PyModule_Create(&operator_module);
	if (pyModule == NULL) {
		return NULL;
	}

	Py_INCREF(&PyMetafileType);
	if (PyModule_AddObject(pyModule, "Metafile", (PyObject*)&PyMetafileType) < 0) {
		Py_DECREF(&PyMetafileType);
		Py_DECREF(pyModule);
		return NULL;
	}

	return pyModule;
}