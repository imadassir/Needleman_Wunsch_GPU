# Needleman_Wunsch_GPU

# Overview

This code implements the Needleman-Wunsch algorithm for exact string matching.

# Requirements

To compile, nvcc is required. If not available, the Makefile can be modified to execute gcc for .c files instead of nvcc for .cu files.

# Instructions

To compile:

```
make
```

To run:

```
./seq_nw <N> 
```
