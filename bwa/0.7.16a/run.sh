#!/bin/bash

if [ $# -eq 0 ];then
    /bin/bash
else
    exec "$@"
fi
