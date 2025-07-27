#!/bin/bash
# render-build.sh

# Install Python 3.10 using pyenv
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
curl https://pyenv.run | bash
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
pyenv install 3.10.13
pyenv global 3.10.13

# Install pip and dependencies
python -m ensurepip
python -m pip install --upgrade pip
pip install -r requirements.txt
