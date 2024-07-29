#!/bin/bash

make migration

make migrate

exec python main.py
