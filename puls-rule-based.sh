#!/bin/bash

export LISP_LIB=/cs/puls/lib/
export SBCL_HOME=/cs/puls/lib/sbcl-1.1.12-x86-64-linux/lib/sbcl
export PATH=/cs/puls/lib/sbcl-1.1.12-x86-64-linux/bin:$PATH
export LD_LIBRARY_PATH=/cs/puls/lib/lib64:$LD_LIBRARY_PATH

CORE=/cs/puls/Resources/cores/puls-sbcl-nox-bus-5078.core
DOC=$2

OP="(process-document-stdout-silently \"$2\" :train-capitalization t :suppress-trace t :validate-capitalization t)"

# echo $PATH >> /cs/puls/tmp/sbcl-log
#which sbcl >> /cs/puls/tmp/sbcl-log

sbcl --core "$CORE" \
     --noinform \
     --no-userinit \
     --disable-debugger \
     --eval "$OP" \
     --eval '(sb-ext:quit)' 
