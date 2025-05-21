#include "../atomic/create.h"

#include <Python.h>



static PyObject* py_create_file(PyObject* self, PyObject* args) {

	const char* id;
	const char* data;
	const char* metadata;

	if (!PyArg_ParseTuple(args, "sss", &id, &data, &metadata)) {
		return NULL;
	}

	if (create_file(id, data, metadata) != 0) {
		PyErr_SetString(PyExc_IOError, "Failed to create file.");
		return NULL;
	}

	Py_RETURN_NONE;
}



static PyMethodDef operator_methods[] = {
	{"create_file", py_create_file, METH_VARARGS, "Create a file with given id, data and metadata."},
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
	return PyModule_Create(&operator_module);
}