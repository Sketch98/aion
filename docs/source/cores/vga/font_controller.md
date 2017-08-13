font_controller documentation

font_controller is a hardware block that provides the simplest solution to displaying text on a monitor with hardware. The only signal inputs to font_controller takes are clk and ram_write_port. ram_write_port is an interface to the ram which maps each tile to the character displayed in that tile. vga_ports is an interface to the red, green, and blue outputs that travel to the monitor. The widths of the red, green, and blue signals do not affect font_controller because font_controller only displays white and black.

font_controller has three paramters. The first, resolution, is a tuple with the monitor's displayable width and height as elements. Frequency is the refresh rate of the monitor. font_size is a tuple with the width and height of a character as elements.

#### Counters

font_controller operates by using two pairs of chained counters, one for x and one for y. For the x chained counter there is a counter which counts x mod font_width and a counter that counts x div font_width (same for y and font_height).

```
................
...M......MM....
..MM.......MM...
MMMM........MM..
..MM.........MM.
..MM..........MM
..MM.........MM.
..MM........MM..
..MM.......MM...
MMMMMM....MM....
................
................
................
...MMMM.........
..MM..MM........
..MM..MM........
..MM.MMM.MMMMMM.
...MMMM.........
..MMM.MM.MMMMMM.
..MM..MM........
..MM..MM........
...MMMM.........
................
................

```

Here's an example screen that has a 2x2 grid of characters that are 8x12. x div 8 and y div 8 correspond to the position in the grid (which is the font_ram). We can't just ask the ram is the for the character at 1,0. We have to give it the address instead. An easy way to do this is:

```
read_port.addr.next = y_div_12 * (characters per line) + x_div_8
```

This works if characters per line is a power of two. If it isn't, then we need a multiplier which is resource heavy. Instead y_div_12 will just increment by characters per line every time y_mod_12 overflows. Now we have the address of the character in the ram and the x and y positions of the bit in that character which we need to display. This information is transfered to the ram and rom.

#### RAM

The font_rom contains a grid of ascii values that represent the characters to be displayed. For instance, if we are given the address 0, then the data will be the ascii value for the character '1' (0x31) which is displayed at position (0, 0) on our example screen. The ascii value multiplied by the font_height is the starting address in the rom of the character we need to displayed. This value is used to find the sprite in the rom.

#### ROM

The font_controller has one job. It is to characters located in the font_ram on the monitor. To do that it reads the sprites stored in the font_rom, then displays black or white appropriately. First we must understand how the font_rom is laid out. The font_rom contains the sprite for 128 characters (because ascii). Each character is font_width pixels wide and font_height rows tall. Each row for a character is stored as one value. This means that a character takes up font_height consecutive positions in the font_rom. To read a certain bit from a character in the font_rom we need three pieces of information: the character starting address along with the x and y positions of the bit in the character. The bit will be the xth bit in the value at address (character addr + y position).

##### Extra stuff

The widths and heights of the screen and font can be modified which means that screen width and height won't always be multiples of font width and height. This will lead to partial characters being shown on the right and bottom edges of the screen. To counteract this edge buffers are added so there is a black outline around the screen where text cannot be displayed.

The x_mod_8 counter in our example counts from left to right, but bits are read from right to left. To fix the discrepancy the characters are all stored reversed in the rom.