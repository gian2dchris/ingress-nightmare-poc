# !/bin/bash
# -fPIC: for generating a shared object (PIC: Position Independent Code)
# -c: compile and assemble, but do not link.
gcc -fPIC -o shell.o -c shell.c 
# -shared: create a shared library.
gcc -shared -o shell.so -lcrypto shell.o