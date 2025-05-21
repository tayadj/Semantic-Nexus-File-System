#include "read.h"
#include "metafile.h"

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>



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
		perror("Ошибка чтения data");
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
		perror("Ошибка чтения metadata");
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
