#include "atomic.h"

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>



int create_file(const char* id, const Metafile* metafile) {

	FILE* file_pointer = fopen(id, "wb");
	if (!file_pointer) {
		return -1;
	}

	uint32_t size;

	size = (metafile->text != NULL) ? (uint32_t)strlen(metafile->text) : 0;
	if (fwrite(&size, sizeof(uint32_t), 1, file_pointer) != 1) {
		fclose(file_pointer);
		return -1;
	}
	if (size > 0) {
		if (fwrite(metafile->text, sizeof(char), size, file_pointer) != size) {
			fclose(file_pointer);
			return -1;
		}
	}

	if (fwrite(&metafile->image_size, sizeof(uint32_t), 1, file_pointer) != 1) {
		fclose(file_pointer);
		return -1;
	}
	if (metafile->image_size > 0 && metafile->image != NULL) {
		if (fwrite(metafile->image, 1, metafile->image_size, file_pointer) != metafile->image_size) {
			fclose(file_pointer);
			return -1;
		}
	}

	if (fwrite(&metafile->audio_size, sizeof(uint32_t), 1, file_pointer) != 1) {
		fclose(file_pointer);
		return -1;
	}
	if (metafile->audio_size > 0 && metafile->audio != NULL) {
		if (fwrite(metafile->audio, 1, metafile->audio_size, file_pointer) != metafile->audio_size) {
			fclose(file_pointer);
			return -1;
		}
	}

	if (fwrite(&metafile->video_size, sizeof(uint32_t), 1, file_pointer) != 1) {
		fclose(file_pointer);
		return -1;
	}
	if (metafile->video_size > 0 && metafile->video != NULL) {
		if (fwrite(metafile->video, 1, metafile->video_size, file_pointer) != metafile->video_size) {
			fclose(file_pointer);
			return -1;
		}
	}

	if (fwrite(&((uint32_t)metafile->ontology_size), sizeof(uint32_t), 1, file_pointer) != 1) {
		fclose(file_pointer);
		return -1;
	}

	for (size_t i = 0; i < metafile->ontology_size; ++i) {

		size = (metafile->ontology[i].head != NULL) ? (uint32_t)strlen(metafile->ontology[i].head) : 0;
		if (fwrite(&size, sizeof(uint32_t), 1, file_pointer) != 1) {
			fclose(file_pointer);
			return -1;
		}
		if (size > 0) {
			if (fwrite(metafile->ontology[i].head, sizeof(char), size, file_pointer) != size) {
				fclose(file_pointer);
				return -1;
			}
		}

		size = (metafile->ontology[i].relation != NULL) ? (uint32_t)strlen(metafile->ontology[i].relation) : 0;
		if (fwrite(&size, sizeof(uint32_t), 1, file_pointer) != 1) {
			fclose(file_pointer);
			return -1;
		}
		if (size > 0) {
			if (fwrite(metafile->ontology[i].relation, sizeof(char), size, file_pointer) != size) {
				fclose(file_pointer);
				return -1;
			}
		}

		size = (metafile->ontology[i].tail != NULL) ? (uint32_t)strlen(metafile->ontology[i].tail) : 0;
		if (fwrite(&size, sizeof(uint32_t), 1, file_pointer) != 1) {
			fclose(file_pointer);
			return -1;
		}
		if (size > 0) {
			if (fwrite(metafile->ontology[i].tail, sizeof(char), size, file_pointer) != size) {
				fclose(file_pointer);
				return -1;
			}
		}
	}

	fclose(file_pointer);
	return 0;
}

PyObject* py_create_file(PyObject* self, PyObject* args) {

	const char* id;
	PyObject* metafile;

	if (!PyArg_ParseTuple(args, "sO", &id, &metafile)) {
		return NULL;
	}
	  
	if (!PyObject_TypeCheck(metafile, &PyMetafileType)) {
		PyErr_SetString(PyExc_TypeError, "Expected a Metafile object.");
		return NULL;
	}

	PyMetafile* pyMetafile = (PyMetafile*)metafile;

	if (create_file(id, pyMetafile->metafile) != 0) {
		PyErr_SetString(PyExc_IOError, "Failed to create file.");
		return NULL;
	}

	Py_RETURN_NONE;

}

Metafile* read_file(const char* id) {

	FILE* file_pointer = fopen(id, "rb");
	if (!file_pointer) {
		return NULL;
	}

	Metafile* metafile = malloc(sizeof(Metafile));
	if (!metafile) {
		fclose(file_pointer);
		return NULL;
	}
	memset(metafile, 0, sizeof(Metafile)); 

	uint32_t size;

	if (fread(&size, sizeof(uint32_t), 1, file_pointer) != 1) {
		fclose(file_pointer);
		Metafile_free(metafile);
		return NULL;
	}
	if (size > 0) {
		metafile->text = malloc(size + 1);
		if (!metafile->text) {
			fclose(file_pointer);
			Metafile_free(metafile);
			return NULL;
		}
		if (fread(metafile->text, sizeof(char), size, file_pointer) != size) {
			fclose(file_pointer);
			Metafile_free(metafile);
			return NULL;
		}
		metafile->text[size] = '\0';
	} else {
		metafile->text = NULL;
	}

	if (fread(&metafile->image_size, sizeof(uint32_t), 1, file_pointer) != 1) {
		fclose(file_pointer);
		Metafile_free(metafile);
		return NULL;
	}
	if (metafile->image_size > 0 && metafile->image != NULL) {
		metafile->image = malloc(metafile->image_size);
		if (!metafile->image) {
			fclose(file_pointer);
			Metafile_free(metafile);
			return NULL;
		}
		if (fread(metafile->image, 1, metafile->image_size, file_pointer) != metafile->image_size) {
			fclose(file_pointer);
			Metafile_free(metafile);
			return NULL;
		}
	} else {
		metafile->image = NULL;
	}

	if (fread(&metafile->audio_size, sizeof(uint32_t), 1, file_pointer) != 1) {
		fclose(file_pointer);
		Metafile_free(metafile);
		return NULL;
	}
	if (metafile->audio_size > 0 && metafile->audio != NULL) {
		metafile->audio = malloc(metafile->audio_size);
		if (!metafile->audio) {
			fclose(file_pointer);
			Metafile_free(metafile);
			return NULL;
		}
		if (fread(metafile->audio, 1, metafile->audio_size, file_pointer) != metafile->audio_size) {
			fclose(file_pointer);
			Metafile_free(metafile);
			return NULL;
		}
	} else {
		metafile->audio = NULL;
	}

	if (fread(&metafile->video_size, sizeof(uint32_t), 1, file_pointer) != 1) {
		fclose(file_pointer);
		Metafile_free(metafile);
		return NULL;
	}
	if (metafile->video_size > 0 && metafile->video != NULL) {
		metafile->video = malloc(metafile->video_size);
		if (!metafile->video) {
			fclose(file_pointer);
			Metafile_free(metafile);
			return NULL;
		}
		if (fread(metafile->video, 1, metafile->video_size, file_pointer) != metafile->video_size) {
			fclose(file_pointer);
			Metafile_free(metafile);
			return NULL;
		}
	} else {
		metafile->video = NULL;
	}

	uint32_t ontology_size;
	if (fread(&ontology_size, sizeof(uint32_t), 1, file_pointer) != 1) {
		fclose(file_pointer);
		Metafile_free(metafile);
		return NULL;
	}
	metafile->ontology_size = ontology_size;
	if (ontology_size > 0) {
		metafile->ontology = malloc(ontology_size * sizeof(*(metafile->ontology)));
		if (!metafile->ontology) {
			fclose(file_pointer);
			Metafile_free(metafile);
			return NULL;
		}
		for (size_t i = 0; i < ontology_size; ++i) {
			
			if (fread(&size, sizeof(uint32_t), 1, file_pointer) != 1) {
				fclose(file_pointer);
				Metafile_free(metafile);
				return NULL;
			}
			if (size > 0) {
				metafile->ontology[i].head = malloc(size + 1);
				if (!metafile->ontology[i].head) {
					fclose(file_pointer);
					Metafile_free(metafile);
					return NULL;
				}
				if (fread(metafile->ontology[i].head, sizeof(char), size, file_pointer) != size) {
					fclose(file_pointer);
					Metafile_free(metafile);
					return NULL;
				}
				metafile->ontology[i].head[size] = '\0';
			} else {
				metafile->ontology[i].head = NULL;
			}

			if (fread(&size, sizeof(uint32_t), 1, file_pointer) != 1) {
				fclose(file_pointer);
				Metafile_free(metafile);
				return NULL;
			}
			if (size > 0) {
				metafile->ontology[i].relation = malloc(size + 1);
				if (!metafile->ontology[i].relation) {
					fclose(file_pointer);
					Metafile_free(metafile);
					return NULL;
				}
				if (fread(metafile->ontology[i].relation, sizeof(char), size, file_pointer) != size) {
					fclose(file_pointer);
					Metafile_free(metafile);
					return NULL;
				}
				metafile->ontology[i].relation[size] = '\0';
			} else {
				metafile->ontology[i].relation = NULL;
			}

			if (fread(&size, sizeof(uint32_t), 1, file_pointer) != 1) {
				fclose(file_pointer);
				Metafile_free(metafile);
				return NULL;
			} if (size > 0) {
				metafile->ontology[i].tail = malloc(size + 1);
				if (!metafile->ontology[i].tail) {
					fclose(file_pointer);
					Metafile_free(metafile);
					return NULL;
				}
				if (fread(metafile->ontology[i].tail, sizeof(char), size, file_pointer) != size) {
					fclose(file_pointer);
					Metafile_free(metafile);
					return NULL;
				}
				metafile->ontology[i].tail[size] = '\0';
			} else {
				metafile->ontology[i].tail = NULL;
			}
		}
	} else {
		metafile->ontology = NULL;
	}

	fclose(file_pointer);

	return metafile;

}

PyObject* py_read_file(PyObject* self, PyObject* args) {

	const char* id;
	if (!PyArg_ParseTuple(args, "s", &id)) {
		return NULL;
	}

	Metafile* metafile = read_file(id);
	if (!metafile) {
		PyErr_SetString(PyExc_IOError, "Failed to read file.");
		return NULL;
	}

	PyMetafile* pyMetafile = PyObject_New(PyMetafile, &PyMetafileType);
	if (!pyMetafile) {
		Metafile_free(metafile);
		return NULL;
	}
	pyMetafile->metafile = metafile;

	return (PyObject*)pyMetafile;

}

int delete_file(const char* id) {

	if (remove(id) != 0) {
		return -1;
	}

	return 0;

}

PyObject* py_delete_file(PyObject* self, PyObject* args) {

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