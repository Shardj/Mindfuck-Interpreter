# Mindfuck - A Brainfuck dialect for the truly insane

Warning, this is the shittiest interpreter ever, I'm speed coding this just so I have something to check against when I make a proper compiler later

    Original brainfuck syntax:
    > 	increment the data pointer (to point to the next cell to the right).
    < 	decrement the data pointer (to point to the next cell to the left).
    + 	increment (increase by one) the byte at the data pointer.
    - 	decrement (decrease by one) the byte at the data pointer.
    . 	output the byte at the data pointer.
    , 	accept one byte of input, storing its value in the byte at the data pointer.
    [ 	if the byte at the data pointer is zero, then instead of moving the instruction pointer forward to the next command, jump it forward to the command after the matching ] command.
    ] 	if the byte at the data pointer is nonzero, then instead of moving the instruction pointer forward to the next command, jump it back to the command after the matching [ command.


    New mindfuck syntax:
    ~ 	resets data pointer to zero.
    *       writes byte at pointer to the end of the naming string, naming string is an implicit group of bytes in mindfuck used to hold a list of ascii characters. Essentially no different to the data array brainfuck usually operates on except this one has the explicit purpose of file handling.
    !       empties the naming string
    ;       a file name is taken from the naming string using ascii values. The value at our current pointer will be used as an index. The value at the given index from the given file will replace the value in the cell.
    : 	a file name is taken from the naming string using ascii values. The value at our current pointer will be appended to the given file.
    { 	creates a method stored at the pointer. Code written after here before exit is stored.
    } 	exits method creation.
    {}      a combination of both enter and exit function with no contents will read from the file given in the naming string and save its contents as a function to the pointer.
    .       if used on a cell holding a function will run the function.
