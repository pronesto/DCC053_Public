/* Define the memory regions of the system */
MEMORY
{
    /* Define RAM and ROM (or FLASH) memory regions */
    /* Read-only memory for code */
    ROM (rx)  : ORIGIN = 0x08000000, LENGTH = 512K
    /* Read-write memory for stack, heap, data */
    RAM (rwx) : ORIGIN = 0x20000000, LENGTH = 128K
}

/* Define the entry point of the program (usually the reset handler) */
ENTRY(_start)

SECTIONS
{
    /* .text section: Code goes into the ROM region (executable, read-only) */
    .text : {
        *(.text)        /* Place all .text sections (code) here */
        *(.rodata)      /* Place read-only data here (like constants) */
        _etext = .;     /* Mark the end of the .text section */
    } > ROM

    /* .data section: Initialized data goes into RAM (read-write) */
    .data : {
        _sdata = .;     /* Start of initialized data */
        *(.data)        /* All .data sections */
        _edata = .;     /* End of initialized data */
    } > RAM AT > ROM    /* Loaded from ROM at runtime but placed in RAM */

    /* .bss section: Uninitialized data (zeroed at startup) goes into RAM */
    .bss : {
        _sbss = .;      /* Start of uninitialized data */
        *(.bss)         /* All .bss sections */
        *(COMMON)       /* Common symbols */
        _ebss = .;      /* End of uninitialized data */
    } > RAM

    /* Stack setup: Place the stack at the end of RAM */
    _estack = ORIGIN(RAM) + LENGTH(RAM);  /* Top of stack (end of RAM) */
    .stack : {
        _sstack = .;    /* Start of stack */
        . = _sstack + 4K;  /* Allocate 4KB for stack */
        _estack = .;    /* End of stack */
    } > RAM

    /* Heap setup: Place the heap below the stack */
    _sheap = _ebss;     /* Heap starts after the .bss section */
    .heap : {
        _sheap = .;     /* Start of heap */
        . = _sheap + 16K;  /* Allocate 16KB for heap */
        _eheap = .;     /* End of heap */
    } > RAM

    /* Provide symbols for C runtime initialization */
    _sidata = LOADADDR(.data);  /* Initial data location in ROM */
    _sdata = ADDR(.data);       /* Address of .data in RAM */
}
