#include "metafile.h"



static void Metafile_free(Metafile* metafile) {

	if (!metafile) {
		return;
	} 

	if (metafile->text) {
		free(metafile->text);
	}

	if (metafile->image) {
		free(metafile->image);
	}

	if (metafile->audio) {
		free(metafile->audio);
	}

	if (metafile->video) {
		free(metafile->video);
	}

	if (metafile->ontology) {
		for (size_t i = 0; i < metafile->ontology_count; ++i) {
			if (metafile->ontology[i].head) {
				free(metafile->ontology[i].head);
			}
			if (metafile->ontology[i].relation) {
				free(metafile->ontology[i].relation);
			}
			if (metafile->ontology[i].tail) {
				free(metafile->ontology[i].tail);
			}
		}
		free(metafile->ontology);
	}

	free(metafile);

}

void PyMetafile_dealloc(PyMetafile* self) {

	if (self->metafile) {
		Metafile_free(self->metafile);
	}
	Py_TYPE(self)->tp_free((PyObject*)self);

}

PyObject* PyMetafile_new(PyTypeObject* type, PyObject* args, PyObject* kwargs) {

	PyMetafile* self = (PyMetafile*)type->tp_alloc(type, 0);

	if (self != NULL) {
		self->metafile = malloc(sizeof(Metafile));
		if (self->metafile == NULL) {
			Py_DECREF(self);
			PyErr_NoMemory();
			return NULL;
		}

		self->metafile->text = NULL;
		self->metafile->image = NULL;
		self->metafile->image_size = 0;
		self->metafile->audio = NULL;
		self->metafile->audio_size = 0;
		self->metafile->video = NULL;
		self->metafile->video_size = 0;
		self->metafile->ontology = NULL;
		self->metafile->ontology_count = 0;
	}

	return (PyObject*)self;

}

int PyMetafile_init(PyMetafile* self, PyObject* args, PyObject* kwargs) {

	static char* kwlist[] = { "text", "image", "audio", "video", "ontology", NULL };
	PyObject* py_text = NULL;
	PyObject* py_image = NULL;
	PyObject* py_audio = NULL;
	PyObject* py_video = NULL;
	PyObject* py_ontology = NULL;

	if (!PyArg_ParseTupleAndKeywords(
			args, kwargs, "|OOOOO", kwlist, 
			&py_text, &py_image, &py_audio, &py_video, &py_ontology
		)) {
		return -1;
	}

	if (py_text && py_text != Py_None) {
		if (!PyUnicode_Check(py_text)) {
			PyErr_SetString(PyExc_TypeError, "Text must be string-type.");
			return -1;
		}
		const char* temp = PyUnicode_AsUTF8(py_text);
		if (!temp) {
			return -1;
		}
		self->metafile->text = strdup(temp);
		if (!self->metafile->text) {
			PyErr_NoMemory();
			return -1;
		}
	} else {
		self->metafile->text = strdup("");
		if (!self->metafile->text) {
			PyErr_NoMemory();
			return -1;
		}
	}

	if (py_image && py_image != Py_None) {
		if (!PyBytes_Check(py_image)) {
			PyErr_SetString(PyExc_TypeError, "Image must be byte-type.");
			return -1;
		}
		char* buffer;
		Py_ssize_t size;
		if (PyBytes_AsStringAndSize(py_image, &buffer, &size) == -1) {
			return -1;
		}
		self->metafile->image = malloc(size);
		if (!self->metafile->image) {
			PyErr_NoMemory();
			return -1;
		}
		memcpy(self->metafile->image, buffer, size);
		self->metafile->image_size = (size_t)size;
	}

	if (py_audio && py_audio != Py_None) {
		if (!PyBytes_Check(py_audio)) {
			PyErr_SetString(PyExc_TypeError, "Audio must be byte-type.");
			return -1;
		}
		char* buffer;
		Py_ssize_t size;
		if (PyBytes_AsStringAndSize(py_audio, &buffer, &size) == -1) {
			return -1;
		}
		self->metafile->image = malloc(size);
		if (!self->metafile->image) {
			PyErr_NoMemory();
			return -1;
		}
		memcpy(self->metafile->image, buffer, size);
		self->metafile->image_size = (size_t)size;
	}

	if (py_video && py_video != Py_None) {
		if (!PyBytes_Check(py_video)) {
			PyErr_SetString(PyExc_TypeError, "Audio must be byte-type.");
			return -1;
		}
		char* buffer;
		Py_ssize_t size;
		if (PyBytes_AsStringAndSize(py_video, &buffer, &size) == -1) {
			return -1;
		}
		self->metafile->image = malloc(size);
		if (!self->metafile->image) {
			PyErr_NoMemory();
			return -1;
		}
		memcpy(self->metafile->image, buffer, size);
		self->metafile->image_size = (size_t)size;
	}

	if (py_ontology && py_ontology != Py_None) {
		if (!PyList_Check(py_ontology)) {
			PyErr_SetString(PyExc_TypeError, "Ontology must be list-type.");
			return -1;
		}
		Py_ssize_t list_size = PyList_Size(py_ontology);
		self->metafile->ontology = malloc(list_size * sizeof(*(self->metafile->ontology)));
		if (!self->metafile->ontology) {
			PyErr_NoMemory();
			return -1;
		}
		self->metafile->ontology_count = (size_t)list_size;
		for (Py_ssize_t i = 0; i < list_size; ++i) {
			PyObject* item = PyList_GetItem(py_ontology, i);
			if (!PyDict_Check(item)) {
				PyErr_SetString(PyExc_TypeError, "Ontology entity must be dict-type.");
				return -1;
			}
			PyObject* py_head = PyDict_GetItemString(item, "head");
			PyObject* py_relation = PyDict_GetItemString(item, "relation");
			PyObject* py_tail = PyDict_GetItemString(item, "tail");
			const char* head_str = (py_head && PyUnicode_Check(py_head)) ? PyUnicode_AsUTF8(py_head) : "";
			const char* relation_str = (py_relation && PyUnicode_Check(py_relation)) ? PyUnicode_AsUTF8(py_relation) : "";
			const char* tail_str = (py_tail && PyUnicode_Check(py_tail)) ? PyUnicode_AsUTF8(py_tail) : "";
			self->metafile->ontology[i].head = strdup(head_str);
			self->metafile->ontology[i].relation = strdup(relation_str);
			self->metafile->ontology[i].tail = strdup(tail_str);
			if (!self->metafile->ontology[i].head || !self->metafile->ontology[i].relation || !self->metafile->ontology[i].tail) {
				PyErr_NoMemory();
				return -1;
			}
		}
	}

	return 0;

}

PyObject* PyMetafile_get_text(PyMetafile* self, void* closure) {

	if (self->metafile->text) {
		return PyUnicode_FromString(self->metafile->text);
	}

	Py_RETURN_NONE;

}

PyObject* PyMetafile_get_image(PyMetafile* self, void* closure) {

	if (self->metafile->image && self->metafile->image_size > 0) {
		return PyBytes_FromStringAndSize((const char*)self->metafile->image, self->metafile->image_size);
	}
		
	Py_RETURN_NONE;

}



int PyMetafile_set_text(PyMetafile* self, PyObject* value, void* closure) {

	if (!value) {
		PyErr_SetString(PyExc_TypeError, "Cannot delete the text attribute.");
		return -1;
	}
	if (!PyUnicode_Check(value)) {
		PyErr_SetString(PyExc_TypeError, "Text must be string-type.");
		return -1;
	}

	const char* temp = PyUnicode_AsUTF8(value);
	if (!temp) {
		return -1;
	}

	char* _text = strdup(temp);
	if (!_text) {
		PyErr_NoMemory();
		return -1;
	}

	free(self->metafile->text);

	self->metafile->text = _text;

	return 0;

}


int PyMetafile_set_image(PyMetafile* self, PyObject* value, void* closure) {

	if (!value) {
		PyErr_SetString(PyExc_TypeError, "Cannot delete the image attribute.");
		return -1;
	}
	if (!PyBytes_Check(value)) {
		PyErr_SetString(PyExc_TypeError, "Image must be byte-type.");
		return -1;
	}

	char* buffer;
	Py_ssize_t size;
	if (PyBytes_AsStringAndSize(value, &buffer, &size) == -1) {
		return -1;
	}
		
	unsigned char* _image = malloc(size);
	if (!_image) {
		PyErr_NoMemory();
		return -1;
	}

	memcpy(_image, buffer, size);
	if (self->metafile->image) {
		free(self->metafile->image);
	}

	self->metafile->image = _image;
	self->metafile->image_size = (size_t)size;

	return 0;

}