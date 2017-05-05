#!/bin/bash

proto_path=~/git_only/base/third-64/protobuf/bin/protoc

${proto_path} --python_out=./gen --proto_path=./interface/ ./interface/price_types.proto 
${proto_path} --python_out=./gen --proto_path=./interface/ ./interface/as_types.proto 
${proto_path} --python_out=./gen --proto_path=./interface/ ./interface/price_service.proto 
