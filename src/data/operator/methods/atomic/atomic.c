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

    if (fwrite(&((uint32_t)metafile->ontology_count), sizeof(uint32_t), 1, file_pointer) != 1) {
        fclose(file_pointer);
        return -1;
    }

    for (size_t i = 0; i < metafile->ontology_count; ++i) {

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

/*
int create_file(const char* id, const char* data, const char* metadata) {

	FILE* file_pointer = fopen(id, "wb");
	if (!file_pointer) {
		return -1;
	}

	uint32_t data_size = (uint32_t)strlen(data);
	uint32_t metadata_size = (uint32_t)strlen(metadata);

	if (fwrite(&data_size, sizeof(data_size), 1, file_pointer) != 1) {
		fclose(file_pointer);
		return -1;
	}

	if (fwrite(data, sizeof(char), data_size, file_pointer) != data_size) {
		fclose(file_pointer);
		return -1;
	}

	if (fwrite(&metadata_size, sizeof(metadata_size), 1, file_pointer) != 1) {
		fclose(file_pointer);
		return -1;
	}

	if (fwrite(metadata, sizeof(char), metadata_size, file_pointer) != metadata_size) {
		fclose(file_pointer);
		return -1;
	}

	fclose(file_pointer);
	return 0;

}

Metafile* read_file(const char* id) {

	FILE* file_pointer = fopen(id, "rb");
	if (!file_pointer) {
		return NULL;
	}

	uint32_t data_size = 0;
	uint32_t metadata_size = 0;

	if (fread(&data_size, sizeof(data_size), 1, file_pointer) != 1) {
		fclose(file_pointer);
		return NULL;
	}

	char* data_buffer = malloc(data_size + 1);
	if (!data_buffer) {
		fclose(file_pointer);
		return NULL;
	}
	if (fread(data_buffer, sizeof(char), data_size, file_pointer) != data_size) {
		free(data_buffer);
		fclose(file_pointer);
		return NULL;
	}
	data_buffer[data_size] = '\0';

	if (fread(&metadata_size, sizeof(metadata_size), 1, file_pointer) != 1) {
		free(data_buffer);
		fclose(file_pointer);
		return NULL;
	}

	char* metadata_buffer = malloc(metadata_size + 1);
	if (!metadata_buffer) {
		free(data_buffer);
		fclose(file_pointer);
		return NULL;
	}
	if (fread(metadata_buffer, sizeof(char), metadata_size, file_pointer) != metadata_size) {
		free(data_buffer);
		free(metadata_buffer);
		fclose(file_pointer);
		return NULL;
	}
	metadata_buffer[metadata_size] = '\0';

	fclose(file_pointer);

	Metafile* metafile = malloc(sizeof(Metafile));
	if (!metafile) {
		free(data_buffer);
		free(metadata_buffer);
		return NULL;
	}

	metafile->data = data_buffer;
	metafile->metadata = metadata_buffer;

	return metafile;

}

int delete_file(const char* id) {

	if (remove(id) != 0) {
		return -1;
	}

	return 0;

}
*/