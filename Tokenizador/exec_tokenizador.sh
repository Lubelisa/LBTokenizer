#!/bin/bash

# Primeiro executamos o tokenizador
python3 tokenizador.py

# Em seguida executamos o udpipe
make all output_name="input_anotado.conllu" input_name="input_tokenizado.txt"