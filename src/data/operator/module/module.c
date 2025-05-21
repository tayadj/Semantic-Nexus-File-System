#include "../atomic/atomic.h"
#include "../atomic/metafile.h"

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

static PyObject* py_read_file(PyObject* self, PyObject* args) {

	const char* id;

	if (!PyArg_ParseTuple(args, "s", &id)) {
		return NULL;
	}

	Metafile* metafile = read_file(id);
	if (metafile == NULL) {
		PyErr_SetString(PyExc_IOError, "Failed to read file.");
		return NULL;
	}

	PyObject* result = Py_BuildValue("ss", metafile->data, metafile->metadata);

	free(metafile->data);
	free(metafile->metadata);
	free(metafile);

	return result;

}

static PyObject* py_delete_file(PyObject* self, PyObject* args) {

	const char* id;

	if (!PyArg_ParseTuple(args, "s", &id)) {
		return NULL;
	}

	if (delete_file(id) != 0) {
		PyErr_SetString(PyExc_IOError, "Failed to delete file.");
		return NULL;
	}

	Py_RETURN_NONE;

}



static PyMethodDef operator_methods[] = {
	{"create_file", py_create_file, METH_VARARGS, "Create a file with given id, data and metadata."},
	{"read_file",   py_read_file,   METH_VARARGS, "Read file and return data and metadata as strings."},
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
	return PyModule_Create(&operator_module);
}