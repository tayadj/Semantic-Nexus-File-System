#ifndef _DATA_OPERATOR_ATOMIC_H_
#define _DATA_OPERATOR_ATOMIC_H_

#include "metafile.h"

#ifdef __cplusplus
extern "C" {
#endif

	int create_file(const char* id, const char* data, const char* metadata);
	Metafile* read_file(const char* id);
	int delete_file(const char* id);

#ifdef __cplusplus
}
#endif

#endif 
