#!/bin/bash
# Simple command runner that ensures PATH is correct

export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:$PATH

"$@"
