#!/bin/sh

MODEL="open_llama_3b"
# Get  open_llama_3b_ggml q5_1 quantization
python3 ./hug_model.py -a SlyEcho -s ${MODEL} -f open-llama-3b-q5_1.bin
ls -lh *.bin

# Build the default OpenBLAS image
docker build -e CMAKE_ARGS="-DLLAMA_OPENBLAS=1 -DSSE3=1 -DAVX1=1 -DFMA=1 -DAVX2=0 -DAVX512=0 -DAVX512_VBMI=0 -DAVX512_VNNI=0 -DF16C=0 -DFP16_VA=0 -DWASM_SIMD=0" -t $MODEL .
docker images | egrep "^(REPOSITORY|$MODEL)"

echo
echo "To start the docker container run:"
echo "docker run -t -p 8000:8000 $MODEL"
