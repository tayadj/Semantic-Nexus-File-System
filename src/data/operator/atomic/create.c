#include "create.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>



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