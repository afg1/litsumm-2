from python:3.10.13-bookworm

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python get-pip.py

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml

RUN PATH="$PATH:/root/.local/bin" poetry config virtualenvs.create false
RUN PATH="$PATH:/root/.local/bin" poetry install


