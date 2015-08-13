#!/bin/bash

export LISP_LIB=/cs/puls/lib/
export SBCL_HOME=/cs/puls/lib/sbcl-1.1.12-x86-64-linux/lib/sbcl
export PATH=/cs/puls/lib/sbcl-1.1.12-x86-64-linux/bin:$PATH
export LD_LIBRARY_PATH=/cs/puls/lib/lib64:$LD_LIBRARY_PATH

CORE=/cs/puls/Resources/cores/64-bit-cores/puls-sbcl-nox-bus.core

if [ ! -f $1 ] || [ -z $1 ]; then
	echo "'$1' does not exist"
	exit -1
fi

# DOC_DIR=/cs/taatto/home/hxiao/capitalization-recovery/corpus/puls-format-capitalized/
DOC_DIR=/cs/taatto/home/hxiao/capitalization-recovery/corpus/puls-format


while read docid; do
	doc_path="${DOC_DIR}/${docid}"
	OP="(process-document \"${doc_path}\" :output-format 'JSON :train-capitalization t :suppress-trace t)"
	sbcl --core "$CORE" \
		--noinform \
		--no-userinit \
		--disable-debugger \
		--eval "$OP" \
		--eval '(sb-ext:quit)'
done < $1
