PYTHON = venv/bin/python
PROTO_DIR = ./protos
PROTO_FILE = api.proto
PROTO_DIR ?=.
GEN_DIR = ./

# Install dependencies
install: venv
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install grpcio grpcio-tools pysyncobj

# Generate gRPC code
generate:
	python3 -m grpc_tools.protoc -I$(PROTO_DIR) \
		--python_out=$(GEN_DIR)/ \
		--pyi_out=$(GEN_DIR)/ \
		--grpc_python_out=$(GEN_DIR)/ \
		$(PROTO_FILE)

# Run the test
test:
	$(PYTHON) test.py

# Clean generated files
clean:
	rm -f $(GEN_DIR)/*_pb2.py $(GEN_DIR)/*_pb2.pyi $(GEN_DIR)/*_pb2_grpc.py

# Build everything
build: install generate