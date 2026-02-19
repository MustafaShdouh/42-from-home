# Push Swap

*This activity has been created as part of the 42 curriculum by mel-shdo,hqasqas.*

## Description

Push_swap is an algorithmic sorting project from the 42 curriculum.  
The objective is to sort a stack of integers using a limited set of operations and an auxiliary stack.

The challenge is not only to sort the data, but to do so using the **minimum number of operations**, while respecting algorithmic complexity constraints.

### Goal

- Sort stack **A** in ascending order
- Use only the allowed push_swap operations:
  - `sa`, `sb`, `ss`
  - `pa`, `pb`
  - `ra`, `rb`, `rr`
  - `rra`, `rrb`, `rrr`
- Output only the operations
- Optimize the number of moves

---

### Overview

Push_swap is an algorithmic sorting project from the 42 curriculum.

The goal is to sort a stack of integers in ascending order using a limited set of stack operations and a second auxiliary stack. The main challenge is not just sorting — but doing so with the **minimum number of operations**, while respecting strict complexity constraints.

This implementation provides an **adaptive multi-strategy sorting system** designed to optimize performance across different dataset sizes and disorder levels.


## Instructions

### Compilation

To compile the project, navigate to the root directory and run:

```bash
make
```

This will:
1. Build the libft library (custom C standard library functions)
2. Compile all source files
3. Link everything into the `push_swap` executable

### Available Make Targets

```bash
make          # Compile the program
make clean    # Remove object files
make fclean   # Remove object files and executable
make re       # Clean and recompile everything
```


### Execution

Run the program with a list of integers as arguments:

```bash
./push_swap 4 67 3 87 23
```

### Flags

The program supports the following optional flags:

```bash
./push_swap --simple <numbers>     # Use selection sort algorithm
./push_swap --medium <numbers>     # Use medium sorting algorithm
./push_swap --complex <numbers>    # Use complex sorting algorithm
./push_swap --adaptive <numbers>   # Use adaptive algorithm (default)
./push_swap --bench <numbers>      # Enable benchmarking mode
```

### Example

```bash
$ ./push_swap 3 2 5 1 4
sa
pb
rb
pa
sa

$ ./push_swap --bench 3 2 5 1 4
sa
pb
rb
pa
sa
Operations: sa=1 pb=1 rb=1 pa=1 sa=1 Total=5

```

## Algorithm Justification and Technical Choices

### Simple Sort: Selection Sort (O(n²))

**Algorithm Description:**
A selection-style sorting approach:

1. repeatedly locate the minimum
2. rotate A to bring it to the top
3. push it to B
4. Repeat
5. Push all elements back from stack B to stack A

**Why Selection Sort?**
- **Simplicity:** Easy to implement and debug.
- **Deterministic:** Always performs the same number of passes.
- **Stack-Friendly:** Naturally maps to push and rotate operations.
- **Ideal for Small Datasets:** Efficient when n is small (≤ 5–10 elements).

**Limitations:**
- O(n²) time complexity makes it inefficient for large datasets
- Not adaptive; doesn't take advantage of partially sorted inputs

---

### Medium Sort: Range/Window Chunk Sort (O(n√n))

**Algorithm Description:**
The medium strategy uses an index-based range partitioning approach (often called chunk / window sorting).
All values in stack A are first normalized into indices from 0 to n-1 using index_stack(). Then, the algorithm moves elements from A to B in controlled windows (ranges) to reduce rotations and improve overall operation count.

1. **Calculate Range Size**:The range is dynamically computed as:

range = stack_size(A) * 0.15 + 15


This allows the window size to scale with dataset size.

2. **Partitioning Phase**: 
   - Maintain a moving boundary i (expected smallest index).
   - If top->index <= i:
          - Push to stack B (pb)
          - Rotate stack B (rb) to distribute small indices efficiently
          - Increment i
   -Else if top->index <= i + range:
         -Push to stack B (pb)
         -Increment i
   -Else:
         -Rotate stack A (ra) to scan for a suitable element
   This ensures that elements are pushed to B in controlled index windows while minimizing excessive rotations.

3. **Merging Phase**:
   - Once stack A is empty, rebuild it from stack B.
   - Find the maximum index in stack B.
   - Move it to the top using the shortest rotation path:
            -Use rb if the max is in the first half
            -Use rrb if it is in the second half
   -Push it back to stack A using pa
   -Repeat until stack B is empty
   Since the maximum is always extracted first, stack A is rebuilt in ascending order.

**Algorithm Complexity**: O(n√n)

**Why Range-Based Approach?**
- **Balanced Efficiency**:Faster than selection sort for medium inputs
- **Adaptive Range**: Adapts to dataset size using a proportional formula

**Key Optimization**:
- Dynamically scaled range (n * 0.15 + 15)
- Selective rotation of stack B when handling very small indices
- Shortest-path max extraction using rb or rrb
- Index normalization for simplified comparisons

**When Used:**
The medium strategy is selected:

Manually via --medium

Automatically in adaptive mode for moderately disordered datasets

Typically optimal for medium-sized inputs (50–1000 elements)

---

### Complex Sort: Radix Sort with Bit-Shifting (O(n × bits) ≈ O(n log n))

The complex strategy implements an **LSD Radix Sort** using **bit shifting** on normalized indices.

All values in stack A are first converted into indices from 0 to n-1 (rank normalization). This makes every number non-negative and bounded, which is ideal for radix processing.

1. **Bit Counting**:Determine how many bits are needed to represent the largest index:

      max_bits = ⌈log₂(n)⌉
   
2. **Bit-by-Bit Partitioning (LSB → MSB):** For each bit position from 0 to max_bits - 1:
   Scan stack A exactly n times:
     - **push to B (pb)**: If the current element has bit = 0
     - **rotate A (ra)**: If bit = 1
   - Push everything back from B to A (pa) to restore elements for the next bit pass

3. **Stability Preservation**: Processing from least significant bit to most significant bit, while reinserting from B to A after each pass, preserves the ordering of previously processed bits.

**Algorithm Complexity**: O(n × max_bits) ≈ O(n log n)

**Why Radix Bit-Shifting?**
- **Deterministic Performance:**: Same behavior regardless of input pattern
- **Non-Comparative**: Doesn’t rely on comparing values; only checks bits.

**Implementation Details**:
Bit extraction is done using:
```c
(index >> bit_position) & 1
```

**When Used**
The complex strategy is selected:
- Manually via --complex
- Automatically in adaptive mode for highly disordered or large datasets where O(n log n) outperforms range-based methods.

---

### Adaptive Algorithm

The program includes an **adaptive sorting system** that:

1. **Computes Disorder**: Calculates the ratio of inversions in the input (how "unsorted" it is)
2. **Selects Strategy**: Based on disorder level and dataset size, chooses the optimal algorithm
3. **Optimizes Performance**: Balances operation count across different input patterns

**Disorder Calculation:**
Disorder is computed as the ratio of inverted pairs (where element i > element j but i comes before j) to total pairs. This provides a normalized metric (0.0 to 1.0) representing how far the data is from being sorted.

### Stack Operations Implemented

All sorting algorithms use these four types of operations:

| Operation | Description |
|-----------|-------------|
| `sa` / `sb` / `ss` | Swap top two elements (stack A, B, or both) |
| `pa` / `pb` | Push top element from one stack to another |
| `ra` / `rb` / `rr` | Rotate stack upward (shift all elements up) |
| `rra` / `rrb` / `rrr` | Reverse rotate (shift all elements down) |

### Data Structures

```c
typedef struct s_node {
    int value;
    int index;           // Normalized rank of the value
    struct s_node *next;
    struct s_node *prev; // Doubly-linked for efficiency
} t_node;

typedef struct s_stack {
    int size;
    t_node *top;
    t_node *bottom;
} t_stack;
```

**Design Choices:**
- **Doubly-linked list**: efficient bidirectional traversal
- **Index field**: simplifies radix logic
- **Stored size**:O(1) size access
- **Separate stacks** : clean partition logic

### Input Validation

The program checks:
- Valid integer input
- No duplicates
- Within INT_MIN and INT_MAX
- At least one valid number provided
On error:

```bash
   Error
```


## Resources

### Documentation
- [42 School Curriculum](https://42.fr/) - Project guidelines and specifications

### AI Usage

AI assistance was used for:

- clarifying the disorder metric requirements and bench expectations

- explaining and documenting radix sort (bit-shifting) and complexity reasoning

- documentation structure and readability improvements

All implementation choices were tested and validated by the authors.
## Features

✓ Multiple Sorting Algorithms
✓ Radix bit-shifting implementation
✓ Disorder-based strategy selection
✓ Efficient doubly-linked stack structure
✓ Detailed benchmarking system 
✓ Clean and norm-compliant C code  
✓ Automated test targets  
✓ Deterministic and stable sorting