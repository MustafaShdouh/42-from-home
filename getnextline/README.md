*This project has been created as a part of the 42 curriculum by mel-shdo*

# Get Next Line

## Description

The goal of this project is to create a function, `get_next_line`, that reads a line from a file descriptor. Whether reading from a file, standard input, or a network connection, this function allows you to read content one line at a time until the end of the text.
This project introduces a new concept in C programming: Static Variables, which allow data to persist in memory between function calls.

## Instructions

### Compilation

To compile the project, you must compile the source files along with the -D BUFFER_SIZE=n flag, which determines the size of the buffer used for `read()`.
```bash
cc -Wall -Wextra -Werror -D BUFFER_SIZE=42 get_next_line.c get_next_line_utils.c main.c -o gnl
```

### Execution

After compiling, run the executable:
```bash
./gnl
```

## Usage

Include the header in your C file:
```c
#include "get_next_line.h"

int main(void)
{
    int   fd = open("file.txt", O_RDONLY);
    char  *line;

    while ((line = get_next_line(fd)) != NULL)
    {
        printf("%s", line);
        free(line);
    }
    close(fd);
    return (0);
}
```

## Algorithmic Justification

For this project, I selected the Static String Accumulation method (using `ft_strjoin`).

### Why this approach?

I chose this algorithm for its **simplicity and readability**. By treating the static variable as a simple "stash" string that grows as we read, the logic remains linear and easy to debug. It avoids the complexity of managing multiple nodes in a linked list, reducing the overhead of malloc calls for small chunks of data.

### How it works:
1. Read Phase: The function repeatedly calls `read()` with a fixed `BUFFER_SIZE`.
2. Accumulate: Each buffer read is immediately appended to a static string (`stash`) using a helper function `ft_strjoin`. This continues until a newline (\n) is found in the stash or the End of File (EOF) is reached.
3. Extract Line: Once a newline is secured, the function calculates the length up to that newline, allocates memory, and copies the line to be returned.
4. Clean Up: The remaining characters (after the newline) are moved to a new string. The old stash is freed, and the static pointer is updated to point to this new "leftover" string, ready for the next function call.

## AI and Resources

### Resources Used
* Man pages: `read(2), malloc(3), free(3), open(2).`
* Documentation: Articles on C static variables and memory management.