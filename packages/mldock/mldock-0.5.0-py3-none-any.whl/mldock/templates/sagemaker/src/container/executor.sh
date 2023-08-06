#!/usr/bin/env bash

if [ $1 = "train" ]; then
    python ./container/training/train.py
else
    python ./container/prediction/serve.py
fi
