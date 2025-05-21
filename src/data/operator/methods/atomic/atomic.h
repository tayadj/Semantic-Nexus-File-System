#ifndef _DATA_OPERATOR_ATOMIC_H_
#define _DATA_OPERATOR_ATOMIC_H_

#include "../../objects/metafile/metafile.h"

#include <Python.h>

#ifdef __cplusplus
extern "C" {
#endif

	// int create_file(const char* id, const Metafile* metafile);
	// Metafile* read_file(const char* id);
	// int delete_file(const char* id);

	int create_file(const char* id, const Metafile* metafile);

	PyObject* py_create_file(PyObject* self, PyObject* args);

#ifdef __cplusplus
}
#endif

#endif 
