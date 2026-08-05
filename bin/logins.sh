#!/bin/bash
set -xe

# gcloud
gcloud auth login
gcloud auth application-default login

if [[ -f "${HOME}/.logins.sh" ]]; then
	source "${HOME}/.logins.sh"
fi
