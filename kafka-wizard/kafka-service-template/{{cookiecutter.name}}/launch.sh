#!/bin/bash
# Copyright {% now 'local', '%Y' %} {{ cookiecutter.author }}
# See LICENSE for details.

sudo python3 -m pip install pip --upgrade
sudo python3 -m pip install . --upgrade
sudo {{ cookiecutter.name }}