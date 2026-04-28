FROM ghcr.io/huggingface/neuronx-tgi:0.0.26 AS neuronx-tgi

FROM python:3.10-slim-bookworm

# Set environment variables to avoid user interaction during install
ENV DEBIAN_FRONTEND=noninteractive

# Set the Ubuntu version codename (e.g., jammy for 22.04)
ARG VERSION_CODENAME=jammy

COPY --from=neuronx-tgi /opt/aws /opt/aws

# Add the AWS Neuron repository and GPG key
RUN apt-get update && \
    apt-get install -y gnupg wget && \
    echo "deb https://apt.repos.neuron.amazonaws.com ${VERSION_CODENAME} main" \
    | tee /etc/apt/sources.list.d/neuron.list > /dev/null && \
    wget -qO - https://apt.repos.neuron.amazonaws.com/GPG-PUB-KEY-AMAZON-AWS-NEURON.PUB | apt-key add - && \
    apt-get update

RUN apt-get update && \
    apt-get install -y udev pciutils

# Install the Neuron Runtime/tooling that matches torch-neuronx 2.8.x requirements.
RUN apt-get update && \
    apt-get install -y \
        aws-neuronx-runtime-lib=2.30.51.0* \
        aws-neuronx-collectives=2.30.59.0* \
        aws-neuronx-tools=2.28.23.0* && \
    rm -rf /var/lib/apt/lists/*



# Add PATH
ENV PATH /opt/aws/neuron/bin:/opt/app/bin:$PATH
