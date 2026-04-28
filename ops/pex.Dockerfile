# Declare build arguments with default values and If we need to change the value then pass with --build-args param
ARG CACHE_IMAGE
ARG BASE_IMAGE

FROM --platform=linux/amd64 python:3.10-slim-bookworm as pants

RUN apt update && apt -y install curl wget cmake build-essential git unzip && apt clean
RUN curl --proto '=https' --tlsv1.2 -fsSL https://static.pantsbuild.org/setup/get-pants.sh | bash
ENV PATH $PATH:/root/.local/bin

FROM ${CACHE_IMAGE} as cache

FROM --platform=linux/amd64 ${BASE_IMAGE} as builder
RUN apt update && apt -y install curl wget cmake build-essential git unzip && apt clean
COPY --from=pants /root/.local/bin/pants /root/.local/bin/pants
RUN mkdir -p /root/.cache/nce
COPY --from=cache /root/.cache/nce/ /root/.cache/nce/
COPY --from=cache /root/.cache/pants/ /root/.cache/pants/
ARG deps_pex
ARG srcs_pex
ARG deps_pex_target
ARG srcs_pex_target

WORKDIR /opt/app
COPY pants.toml pants.toml
COPY pyproject.toml pyproject.toml
COPY .envrc.build .envrc.build
#COPY .envrc.cpu_exec .envrc.cpu_exec
COPY tools tools
COPY 3rdParty 3rdParty
COPY BUILD BUILD
COPY ai ai

RUN bash -c "source .envrc.build && /root/.local/bin/pants package ${deps_pex_target}"
RUN --mount=id=ai-cache,type=cache,target=/pants cp -r /root/.cache/pants/* /pants/
RUN --mount=id=ai-nce,type=cache,target=/nce cp -r /root/.cache/nce/* /nce/
RUN bash -c "source .envrc.build && /root/.local/bin/pants package ${srcs_pex_target}"

RUN mkdir -p /out
RUN mv /opt/app/${deps_pex} /out/deps.pex
RUN mv /opt/app/${srcs_pex} /out/srcs.pex

FROM python:3.10-slim-bookworm as deps
COPY --from=builder /out/deps.pex /binary.pex
RUN PEX_TOOLS=1 python /binary.pex venv --collisions-ok --scope=deps --compile /opt/app

FROM python:3.10-slim-bookworm as srcs
COPY --from=builder /out/srcs.pex /binary.pex
RUN PEX_TOOLS=1 python /binary.pex venv --scope=srcs --compile /opt/app

FROM ${BASE_IMAGE}
COPY --from=deps /opt/app /opt/app
COPY --from=srcs /opt/app /opt/app
CMD ["/opt/app/pex", "$@"]

