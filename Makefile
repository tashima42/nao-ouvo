SOURCE_FILE ?= generate.c
DIST_FILE ?= dist/generate

build: $(SOURCE_FILE)
	gcc -o $(DIST_FILE) $(SOURCE_FILE)
