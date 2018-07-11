# Mindfuck - A Brainfuck dialect for the truly insane

Warning, this is the shittiest interpreter ever, I'm speed coding this just so I have something to check against when I make a proper compiler later. Also then I can have fun with the new syntax sooner rather than later.

### Original brainfuck syntax:
    > 	increment the data pointer (to point to the next cell to the right).
    < 	decrement the data pointer (to point to the next cell to the left).
    + 	increment (increase by one) the byte at the data pointer.
    - 	decrement (decrease by one) the byte at the data pointer.
    . 	output the byte at the data pointer.
    , 	accept one byte of input, storing its value in the byte at the data pointer.
    [ 	if the byte at the data pointer is zero, then instead of moving the instruction pointer forward to the next command, jump it forward to the command after the matching ] command.
    ] 	if the byte at the data pointer is nonzero, then instead of moving the instruction pointer forward to the next command, jump it back to the command after the matching [ command.


### New mindfuck syntax:
The byte at the data pointer will be refered to as "cells", "cell" singular refers to the cell at the data pointer.

    #       line comment syntax, everything from `#` until the end of the line will be ignored.
    /       area comment syntax, everything from `/` will be ignored until another `/` is found.
    @     	moves data pointer to value given in cell. Now we can take full advantage of the 30,000 cells in the data array
    ~       wipes all values in data array.
    *       writes byte at pointer to the end of the naming string, naming string is an implicit group of bytes in mindfuck used to hold a list of ascii characters.
    !       resets the naming string.
    ;       a file name is taken from the naming string. The cell value will be used as an index. The character at the given index from the given file will be read and replace the value in the cell. If any of the following fail: finding file, finding index, or converting ascii -> decimal we set the cell to zero
    :     	a file name is taken from the naming string. Our cell value will be appended to the given file.
    ?       will take the file found under the naming string and insert the values into our runtime code in place of this symbol
    ^       ends execution of program, helpful in combination with loop syntax. If not 0 sys.exit() equivilient: `[^]`. This saves us from having to do nasty wrapping with loop syntax around all of our code.

Note: if it wasn't clear already when interpreting as a 'character' or from a 'character' in Mindfuck, an ascii conversion is made. For example when using the `?` syntax, it'll convert the decimal value to ascii before trying to interpret it. When reading a character from a file with `;` an ascii to decimal conversion will be made
