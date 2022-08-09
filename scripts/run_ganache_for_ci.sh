#!/usr/bin/env bash

set -euo pipefail

# Run cleanup on exit
trap cleanup EXIT

cleanup() {
    if [ -n "$client" ]; then
        kill -9 $client
    fi
}

# Launch ganache, track its PID and wait until port is open
npx ganache-cli --noVMErrorsOnRPCResponse --port 7545 > /dev/null &
client=$!
npx wait-port 7545
