#! /bin/bash

save_error() {
	sym=$1
	echo "doing $sym"
	python pred_err.py tmp/cap-$sym.model data/reuters/trainable/reuters-$sym tmp/test-$sym.crfsuite.txt > errors/test-$sym.txt
}

save_error "a"
save_error "b" 
save_error "c" 
save_error "d" 
save_error "e" 
save_error "f" 
save_error "g" 
save_error "h" 
save_error "j" 
