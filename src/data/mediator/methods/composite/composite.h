#ifndef _DATA_MEDIATOR_COMPOSITE_H_
#define _DATA_MEDIATOR_COMPOSITE_H_

#include "../../objects/metafile/metafile.h"
#include "../atomic/atomic.h"

#include <Python.h>

#ifdef __cplusplus
extern "C" {
#endif

	Ontology* aggregate_ontology(const char* id, size_t* size);

	PyObject* py_aggregate_ontology(PyObject* self, PyObject* args);

#ifdef __cplusplus
}
#endif

#endif 
