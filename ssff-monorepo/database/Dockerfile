FROM postgis/postgis:16-3.4

# Install build dependencies for pgvector
RUN apt-get update && apt-get install -y \
    git \
    make \
    gcc \
    postgresql-server-dev-16 \
    && rm -rf /var/lib/apt/lists/*

# Install pgvector
RUN git clone --branch v0.7.0 https://github.com/pgvector/pgvector.git \
    && cd pgvector \
    && make \
    && make install \
    && cd .. \
    && rm -rf pgvector

# Minimal cleanup
RUN apt-get remove -y git make gcc postgresql-server-dev-16 \
    && apt-get autoremove -y
