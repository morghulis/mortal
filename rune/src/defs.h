#ifndef _DEFS_H
#define _DEFS_H

#include <inttypes.h>

#ifndef __C99_OR_LATER__
typedef signed char         int8_t;
typedef unsigned char       uint8_t;

typedef short int           int16_t;
typedef unsigned short int  uint16_t;

typedef int                 int32_t;
typedef unsigned int        uint32_t;

#if __X64__
typedef long int            int64_t;
typedef unsigned long int   uint64_t;
#else
typedef long long int       int64_t;
typedef unsigned long int   uint64_t;
#endif

#endif /* __C99_OR_LATER__ */


#ifndef bool
typedef unsigned char bool;

#define true 1
#define false 0

#endif /* bool */


#endif /* _DEFS_H */
