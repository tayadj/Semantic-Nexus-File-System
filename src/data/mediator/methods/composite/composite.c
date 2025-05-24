#include "composite.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>



Ontology* aggregate_ontology(const char* id, size_t* size) {

	PyObject* os_module = PyImport_ImportModule("os");
	if (!os_module) {
		PyErr_Print();
		return NULL;
	}

	PyObject* listdir_func = PyObject_GetAttrString(os_module, "listdir");
	if (!listdir_func || !PyCallable_Check(listdir_func)) {
		PyErr_Print();
		Py_DECREF(os_module);
		return NULL;
	}

	PyObject* py_id = PyUnicode_FromString(id);
	if (!py_id) {
		PyErr_Print();
		Py_DECREF(listdir_func);
		Py_DECREF(os_module);
		return NULL;
	}

	PyObject* file_list = PyObject_CallFunctionObjArgs(listdir_func, py_id, NULL);
	if (!file_list) {
		PyErr_Print();
		Py_DECREF(py_id);
		Py_DECREF(listdir_func);
		Py_DECREF(os_module);
		return NULL;
	}

	if (!PyList_Check(file_list)) {
		Py_DECREF(file_list);
		Py_DECREF(py_id);
		Py_DECREF(listdir_func);
		Py_DECREF(os_module);
		return NULL;
	}

	size_t capacity = 128;
	size_t total_size = 0;
	Ontology* aggregated_ontology = malloc(capacity * sizeof(Ontology));
	if (!aggregated_ontology) {
		Py_DECREF(file_list);
		Py_DECREF(py_id);
		Py_DECREF(listdir_func);
		Py_DECREF(os_module);
		return NULL;
	}
	
    Py_ssize_t num_files = PyList_Size(file_list);
    for (Py_ssize_t i = 0; i < num_files; ++i) {
        PyObject* py_filename = PyList_GetItem(file_list, i);
        const char* filename = PyUnicode_AsUTF8(py_filename);

        if (!filename || strcmp(filename, ".") == 0 || strcmp(filename, "..") == 0) {
            continue;
        }            

        char file_id[2048];
        snprintf(file_id, sizeof(file_id), "%s/%s", id, filename);
        Metafile* metafile = read_file(file_id);
        if (!metafile) {
            continue;
        }
            
        for (size_t j = 0; j < metafile->ontology_size; j++) {

            if (total_size >= capacity) {
                capacity *= 2;
                Ontology* temp = realloc(aggregated_ontology, capacity * sizeof(Ontology));
                if (!temp) {
					for (size_t k = 0; k < total_size; k++) {
						Ontology_free(&aggregated_ontology[k]);
					}
                    free(aggregated_ontology);
                    Metafile_free(metafile);
                    Py_DECREF(file_list);
                    Py_DECREF(py_id);
                    Py_DECREF(listdir_func);
                    Py_DECREF(os_module);
                    return NULL;
                }
				aggregated_ontology = temp;
            }

			aggregated_ontology[total_size].head = metafile->ontology[j].head ? strdup(metafile->ontology[j].head) : NULL;
			aggregated_ontology[total_size].relation = metafile->ontology[j].relation ? strdup(metafile->ontology[j].relation) : NULL;
			aggregated_ontology[total_size].tail = metafile->ontology[j].tail ? strdup(metafile->ontology[j].tail) : NULL;
            ++total_size;
        }

        Metafile_free(metafile);
    }

	if (total_size == 0) {
		free(aggregated_ontology);
		aggregated_ontology = NULL;
	} else {
		Ontology* shrunk_ontology = realloc(aggregated_ontology, total_size * sizeof(Ontology));
		if (shrunk_ontology) {
			aggregated_ontology = shrunk_ontology;
		}
	}

	*size = total_size;

	Py_DECREF(file_list);
	Py_DECREF(py_id);
	Py_DECREF(listdir_func);
	Py_DECREF(os_module);

	return aggregated_ontology;

}

PyObject* py_aggregate_ontology(PyObject* self, PyObject* args) {

    const char* id;
    if (!PyArg_ParseTuple(args, "s", &id)) {
        return NULL;
    }

    size_t size = 0;
    Ontology* aggregated_ontology = aggregate_ontology(id, &size);
    if (!aggregated_ontology) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to aggregate ontology");
        return NULL;
    }

    PyObject* py_list = PyList_New(size);
    if (!py_list) {
        for (size_t i = 0; i < size; ++i) {
            Ontology_free(&aggregated_ontology[i]);
        }
        free(aggregated_ontology);
        return NULL;
    }

    for (size_t i = 0; i < size; i++) {
        PyObject* dict = Py_BuildValue(
            "{s:s, s:s, s:s}",
            "head", aggregated_ontology[i].head ? aggregated_ontology[i].head : "",
            "relation", aggregated_ontology[i].relation ? aggregated_ontology[i].relation : "",
            "tail", aggregated_ontology[i].tail ? aggregated_ontology[i].tail : ""
        );
        if (!dict) {
            Py_DECREF(py_list);
            for (size_t j = i; j < size; ++j) {
                Ontology_free(&aggregated_ontology[j]);
            }
            free(aggregated_ontology);
            return NULL;
        }
        PyList_SET_ITEM(py_list, i, dict);
    }

    for (size_t i = 0; i < size; ++i) {
        Ontology_free(&aggregated_ontology[i]);
    }
    free(aggregated_ontology);

    return py_list;
}
