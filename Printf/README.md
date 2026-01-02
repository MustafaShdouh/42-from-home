This project has been created as part of the 42 curriculum by mel-shdo.*

# ft_printf

## Description
The goal of this project is to recode the famous C library function `printf`. This project provides an opportunity to learn about variadic functions in C—functions that can take a variable number of arguments—and to deepen understanding of formatting and output parsing.The resulting library, `libftprintf.a`, mimics the behavior of the original `printf` for specific conversions (`cspdiuxX%`) and is fully integrated with my custom Libft library for code reusability.

## Instructions

### 1. Compilation
To compile the library, run the following command in the root directory:```bash

make

This will automatically:
1. Compile the internal libft library.
2. Copy libft.a to the root.
3. Add the new ft_printf object files to it to create the final libftprintf.a.

## Available commands:

* make: Compiles the library.
* make clean: Removes object files (including those in libft/).
* make fclean: Removes object files and the library file.
* make re: Recompiles everything from scratch.

### 2. Usage
To use ft_printf in your project:
    1. Include the header: #include "ft_printf.h"
    2. Link the library when compiling your code: cc main.c libftprintf.a -o my_program

## Supported Conversions:

*   %c: Single character.
*   %s: String.
*   %p: Void pointer (hexadecimal address).
*   %d / %i: Decimal (base 10) number.
*   %u: Unsigned decimal number.
*   %x: Hexadecimal number (lowercase).
*   %X: Hexadecimal number (uppercase).
*   %%: Percentage sign.

## Implementation Details & Justification

# Algorithm

The core logic of ft_printf relies on a "Dispatcher" pattern:

    1. Parsing: The main ft_printf function iterates through the input string. Standard characters are written immediately  using write or ft_putchar_fd.
    2. Dispatching: When a % symbol is detected, the ft_formats function is called. It assesses the conversion specifier (e.g., s, d, x) and directs the program to the appropriate helper function.
    3. Variadic Handling: The stdarg.h macros (va_start, va_arg, va_end) are used to retrieve arguments from the stack dynamically based on the detected type.
    4. Recursion for Numbers: Mathematical conversions (Integers, Hex, Pointers) are handled via recursion to print digits one by one.

# Justification

    * Code Reusability: Existing libft functions (like ft_strlen and ft_putstr_fd) were reused to avoid code duplication, strictly adhering to the DRY (Don't Repeat Yourself) principle.
    * Recursion vs Buffers: A recursive approach was chosen for number printing (ft_put_ptr, ft_print_hex) instead of creating string buffers (like itoa). This avoids complex memory management (malloc/free) inside the print logic, reducing the risk of leaks.
    * Modular Design: Separating logic into different files (ft_print_cs.c, ft_print_id.c, etc.) ensures the code is readable, maintainable, and Norminette compliant.

### Resources

### References

*    Standard C Library Documentation: man 3 printf, man 3 stdarg.
*    The C Programming Language (Kernighan & Ritchie): Chapter 7 (Input and Output).

### AI Usage Declaration
• AI Tool Used: Gemini
• Purpose:
I used AI to clarify the logic of the va_arg macro and how it promotes types (e.g., char to int).
I asked AI to explain the mathematical logic behind converting a memory address (uintptr_t) to a hexadecimal string for the %p conversion.
• Generated Code: The code structure and logic were implemented by me. AI provided examples for the Makefile structure to properly link Libft.