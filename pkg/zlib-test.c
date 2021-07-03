#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <time.h>
#include <sys/types.h>
#include <sys/stat.h>

#include "zlib.h"

#define BUFSIZE 4096
#define TRIES 10000  // Optimized tries.

void printusage(char *cmdline) {
    printf("Usage: %s inputfile\n", cmdline);
    return;
}



int iv_compress(char *uncompressed, int uncompressed_size, char *compressed, int compressed_size) {
    z_stream strm;
    int ret;

    strm.zalloc = Z_NULL;
    strm.zfree = Z_NULL;
    strm.opaque = Z_NULL;

    ret = deflateInit(&strm, Z_DEFAULT_COMPRESSION);
    if(ret != Z_OK) {
        fprintf(stderr, "deflatInit failed: %d\n", ret);
        return -1;
    }

    strm.avail_in = uncompressed_size;
    strm.next_in = uncompressed;

    strm.avail_out = compressed_size;
    strm.next_out = compressed;

    ret = deflate(&strm, Z_FINISH);

    ret = (int)strm.total_out;
    deflateEnd(&strm);

    return ret;
}


int iv_decompress(char *compressed, int compressed_size, char *decompressed, int decompressed_size) {
    int ret;
    z_stream strm;
    strm.zalloc = Z_NULL;
    strm.zfree = Z_NULL;
    strm.opaque = Z_NULL;

    ret = inflateInit(&strm);
    if(ret != Z_OK) {
        return -1;
    }
    strm.avail_in = compressed_size;
    strm.next_in = compressed;
    strm.avail_out = decompressed_size;
    strm.next_out = decompressed;
    ret = inflate(&strm, Z_NO_FLUSH);
    if(ret != Z_STREAM_END) {
        ret = -2;
        goto end;
    }

    ret = strm.total_out;

    end:
    inflateEnd(&strm);
    return ret;
}



int main(int argc, char *argv[]) {
    int ret, fd, original_size, compressed_size, decompressed_size;
    char *original = NULL, *compressed = NULL, *decompressed = NULL;
    struct stat fd_stat;
    float rate;

    if(argc != 2) {
        printusage(argv[0]);
        ret = -1;
        goto end;
    }

    fd = open(argv[1], O_RDONLY);
    if(fd < 0) {
        fprintf(stderr, "Open file failed\n");
        ret = -2;
        goto end;
    }

    if(fstat(fd, &fd_stat) < 0) {
        fprintf(stderr, "fstat failed\n");
        ret = -3;
        goto end;
    }

    original = malloc(BUFSIZE);
    if(original == NULL) {
        fprintf(stderr, "malloc failed\n");
        ret = -4;
      goto end;
    }

    original_size = read(fd, original, BUFSIZE);
    if (original_size != BUFSIZE) {
        fprintf(stderr, "read size too small.\n");
        ret = -5;
        goto end;
    }

    if(close(fd) < 0) {
        fprintf(stderr, "close failed\n");
        ret = -6;
        goto end;
    }
    printf("Measuring zlib performance:...\n");

    compressed_size = BUFSIZE * 2;
    compressed = malloc(compressed_size);
    if(compressed == NULL) {
        fprintf(stderr, "malloc failed\n");
        ret = -7;
        goto end;
    }
    decompressed_size = BUFSIZE * 2;
    decompressed = malloc(decompressed_size);
    if(decompressed == NULL) {
        fprintf(stderr, "malloc failed\n");
        ret = -9;
        goto end;
    }

    for(int i = 0 ; i < TRIES ; i++) {
        compressed_size = iv_compress(original, original_size, compressed, compressed_size);
        if(compressed_size < 0) {
            fprintf(stderr, "Compress failed\n");
            ret = -8;
            goto end;
        }
        decompressed_size = iv_decompress(compressed, compressed_size, decompressed, decompressed_size);
        if(decompressed_size < 0) {
            fprintf(stderr, "Decompress failed\n");
            ret = -10;
            goto end;
        }
        if(original_size != decompressed_size) {
            fprintf(stderr, "Data size mismatch: %d vs %d\n", original_size, decompressed_size);
            ret = -11;
            goto end;
        }
        if(memcmp(original, decompressed, original_size) != 0) {
            fprintf(stderr, "Data mismatch. Test failed\n");
            ret = -12;
            goto end;
        }
    }
end:
    if(original != NULL) {
        free(original);
    }
    if(compressed != NULL) {
        free(compressed);
    }
    if(decompressed != NULL) {
        free(decompressed);
    }
    return ret;
}
