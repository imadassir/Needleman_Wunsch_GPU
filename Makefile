
NVCC        = gcc
NVCC_FLAGS  = -O3
OBJ         = main.o
EXE         = seq_nw


default: $(EXE)

%.o: %.c
	$(NVCC) $(NVCC_FLAGS) -c -o $@ $<

$(EXE): $(OBJ)
	$(NVCC) $(NVCC_FLAGS) $(OBJ) -o $(EXE)

clean:
	rm -rf $(OBJ) $(EXE)

