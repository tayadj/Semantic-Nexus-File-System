#ifndef _DATA_METAFILE_H_
#define _DATA_METAFILE_H_

#include <Python.h>

#ifdef __cplusplus
extern "C" {
#endif

	typedef struct {
		char* head;
		char* relation;
		char* tail;
	} Ontology;

	void Ontology_free(Ontology* ontology);



	typedef struct {

		char* text;

		unsigned char* image;
		size_t image_size;

		unsigned char* audio;
		size_t audio_size;

		unsigned char* video;
		size_t video_size;

		Ontology* ontology;
		size_t ontology_size;

	} Metafile;

	void Metafile_free(Metafile* metafile);



	typedef struct {

		PyObject_HEAD
		Metafile* metafile;

	} PyMetafile;

	void PyMetafile_dealloc(PyMetafile* self);
	PyObject* PyMetafile_new(PyTypeObject* type, PyObject* args, PyObject* kwargs);
	int PyMetafile_init(PyMetafile* self, PyObject* args, PyObject* kwargs);
	PyObject* PyMetafile_str(PyObject* self);

	PyObject* PyMetafile_get_text(PyMetafile* self, void* closure);
	PyObject* PyMetafile_get_image(PyMetafile* self, void* closure);
	PyObject* PyMetafile_get_audio(PyMetafile* self, void* closure);
	PyObject* PyMetafile_get_video(PyMetafile* self, void* closure);
	PyObject* PyMetafile_get_ontology(PyMetafile* self, void* closure);

	int PyMetafile_set_text(PyMetafile* self, PyObject* value, void* closure);
	int PyMetafile_set_image(PyMetafile* self, PyObject* value, void* closure);
	int PyMetafile_set_audio(PyMetafile* self, PyObject* value, void* closure);
	int PyMetafile_set_video(PyMetafile* self, PyObject* value, void* closure);
	int PyMetafile_set_ontology(PyMetafile* self, PyObject* value, void* closure);
	
	extern PyMethodDef PyMetafile_methods[];
	extern PyGetSetDef PyMetafile_getset[];
	extern PyTypeObject PyMetafileType;

#ifdef __cplusplus
}
#endif

#endif
