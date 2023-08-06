#!/usr/bin/env bash

# echo $PWD
# if [ $1 = "train" ]; then
#     python ./src/container/runner.py train
# else
#     python ./src/container/runner.py serve
# fi

if [ $1 = "train" ]; then
    python ./src/container/training/train.py
else
    python ./src/container/prediction/serve.py
fi
