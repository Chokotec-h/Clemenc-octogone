/*==============================================================================
FMOD Example Framework
Copyright (c), Firelight Technologies Pty, Ltd 2012-2023.
==============================================================================*/
#include <pthread.h>
#include <assert.h>

#define COMMON_PLATFORM_SUPPORTS_FOPEN
#define Common_TTY(format, ...) fprintf(stderr, format, __VA_ARGS__)

