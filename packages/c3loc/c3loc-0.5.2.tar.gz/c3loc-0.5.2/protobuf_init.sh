#!/bin/sh

(cd proto; protoc --python_out=../src c3loc/proto/*.proto; cd ..)
