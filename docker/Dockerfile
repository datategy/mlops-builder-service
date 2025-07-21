FROM python:3.13-slim-bookworm

WORKDIR /app

ARG USERNAME=papai
ARG USER_UID=20000907
ARG USER_GID=$USER_UID
RUN groupadd --gid "$USER_GID" "$USERNAME" \
    && useradd --uid "$USER_UID" --gid "$USER_GID" -m "$USERNAME" \
    && chown -R "$USER_UID":"$USER_GID" /app

USER papai

WORKDIR /app

# copy the source code to the docker image
COPY --chown=papai . .
