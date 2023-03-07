ARG VARIANT="debian-11"
FROM mcr.microsoft.com/vscode/devcontainers/base:${VARIANT}

# Python
ARG PYTHON_VERSION="latest"
ARG PYTHON_INSTALL_PATH="/usr/local/python"
ARG PIPX_HOME="/usr/local/py-utils"
ARG USERNAME="automatic"
ARG UPDATE_RC="true"
ARG INSTALL_PYTHON_TOOLS="true"
ARG USE_ORYX_IF_AVAILABLE="true"
ARG OPTIMIZE_BUILD_FROM_SOURCE="false"
ADD https://raw.githubusercontent.com/microsoft/vscode-dev-containers/main/script-library/python-debian.sh /tmp/library-scripts/
RUN apt-get update && bash /tmp/library-scripts/python-debian.sh \
    "${PYTHON_VERSION}" \
    "${PYTHON_INSTALL_PATH}" \
    "${PIPX_HOME}" \
    "${USERNAME}" \
    "${UPDATE_RC}" \
    "${INSTALL_PYTHON_TOOLS}" \
    "${USE_ORYX_IF_AVAILABLE}" \
    "${OPTIMIZE_BUILD_FROM_SOURCE}"

# Pip
ADD https://bootstrap.pypa.io/get-pip.py /tmp/pip-tmp/
RUN ${PYTHON_INSTALL_PATH}/bin/python /tmp/pip-tmp/get-pip.py

# Dependencies
RUN ${PYTHON_INSTALL_PATH}/bin/pip --disable-pip-version-check --no-cache-dir install \
    poetry

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

 # Clean up
RUN apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /tmp/library-scripts/ && \
    rm -rf /tmp/pip-tmp/