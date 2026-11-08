.PHONY: run

CC = gcc
CFLAGS = -std=c11 -Wall -Wextra -Wpedantic -g

ENGINE_DIR = src/engine
BUILD_DIR = build

CPPFLAGS = -I$(ENGINE_DIR)/src
SOURCES = $(shell find $(ENGINE_DIR) -name '*.c')

$(BUILD_DIR)/engine: $(SOURCES)
	mkdir -p $(BUILD_DIR)
	$(CC) $(CPPFLAGS) $(CFLAGS) $(SOURCES) -o $@

run: $(BUILD_DIR)/engine
	PYTHONPATH=src python3 -m app.main