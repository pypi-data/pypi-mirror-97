#!/bin/bash

# File directory
DIR=`dirname $0`
. $DIR/setup.sh
. $DIR/init.sh
. $DIR/content.sh
. $DIR/deploy.sh

hlk() {
    local cmd=$1
    shift
    "cmd__$cmd" "$@"
}

hlk "$@"