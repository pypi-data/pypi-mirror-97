#!/usr/bin/env bash

if [ $1 = "train" ]; then
    python ./src/container/training/train.py
else
    python ./src/container/prediction/serve.py
fi
