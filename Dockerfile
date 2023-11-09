from nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

RUN apt update && apt install -y curl python3.10

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3.10 get-pip.py

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3.10 -

COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml

RUN PATH="$PATH:/root/.local/bin" poetry config virtualenvs.create false
RUN PATH="$PATH:/root/.local/bin" poetry install

RUN CMAKE_ARGS="-DLLAMA_CUBLAS=on" python3.10 -m pip install llama-cpp-python


