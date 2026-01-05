.PHONY: all clean

# Default target: clean and build
all: clean build

# Generate index.html from template and topics
build: index.html

index.html: build.py template.html topics.json
	python3 build.py

# Clean generated files
clean:
	rm -f index.html
