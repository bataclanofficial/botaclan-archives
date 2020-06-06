FROM gitpod/workspace-full

USER gitpod

ENV GIT_EDITOR="vim"

RUN sudo apt update \
   && sudo rm -rf /var/lib/apt/lists/* \
   && pyenv global 3.8.2 \
   && pip3.8 install --upgrade \
   poetry \
   pre-commit
