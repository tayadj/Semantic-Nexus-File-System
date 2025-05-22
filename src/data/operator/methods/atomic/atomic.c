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
