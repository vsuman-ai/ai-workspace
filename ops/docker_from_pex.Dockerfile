FROM --platform=linux/amd64 python:3.10-slim-bookworm as deps
ARG deps_pex
COPY ${deps_pex} /binary.pex
RUN PEX_TOOLS=1 python /binary.pex venv --scope=deps --collisions-ok --compile /opt/app

FROM --platform=linux/amd64 python:3.10-slim-bookworm as srcs
ARG srcs_pex
COPY ${srcs_pex} /binary.pex
RUN PEX_TOOLS=1 python /binary.pex venv --scope=srcs --compile /opt/app

FROM --platform=linux/amd64 python:3.10-slim-bookworm
COPY --from=deps /opt/app /opt/app
COPY --from=srcs /opt/app /opt/app
CMD ["/opt/app/pex", "$@"]