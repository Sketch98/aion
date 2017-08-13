from myhdl import always, block


@block
def font_rom(font_size, name, rom_port):
    font_roms = {
        (4, 6): font_rom_4x6,
        (5, 12): font_rom_5x12,
        (7, 12): font_rom_7x12,
        (8, 12): font_rom_8x12,
        (10, 18): font_rom_10x18,
        (12, 16): font_rom_12x16
    }
    assert font_size in font_roms, 'font size {} is not supported.\n' \
                                  'supported font sizes are \n' \
                                  '{}'.format(font_size, font_roms.keys())
    return font_roms[font_size](name, rom_port.clk, rom_port.addr,
                                rom_port.data)


@block
def font_rom_4x6(name, clk, addr, data):
    @always(clk)
    def foo():
        pass

    assert len(addr) == 10, 'addr width = {}, should be 10'.format(len(addr))
    assert len(data) == 4, 'data width = {}, should be 4'.format(len(data))
    clk.read = True
    addr.read = True
    data.driven = True
    return foo
font_rom_4x6.vhdl_code = \
    """
    --copy this signal declaration to architecture declaration
    signal ${data}_slv : std_logic_vector(3 downto 0);

    ${data} <= unsigned(${data}_slv);
    $name: entity work.font_rom_4x6
        port map (
            clka    => $clk,
            addra   => std_logic_vector($addr),
            douta   => ${data}_slv);
    """


@block
def font_rom_5x12(name, clk, addr, data):
    @always(clk)
    def foo():
        pass

    assert len(addr) == 11, 'addr width = {}, should be 11'.format(len(addr))
    assert len(data) == 5, 'data width = {}, should be 5'.format(len(data))
    clk.read = True
    addr.read = True
    data.driven = True
    return foo
font_rom_5x12.vhdl_code = \
    """
    --copy this signal declaration to architecture declaration
    signal ${data}_slv : std_logic_vector(4 downto 0);

    ${data} <= unsigned(${data}_slv);
    $name: entity work.font_rom_5x12
        port map (
            clka    => $clk,
            addra   => std_logic_vector($addr),
            douta   => ${data}_slv);
    """


@block
def font_rom_7x12(name, clk, addr, data):
    @always(clk)
    def foo():
        pass

    assert len(addr) == 11, 'addr width = {}, should be 11'.format(len(addr))
    assert len(data) == 7, 'data width = {}, should be 7'.format(len(data))
    clk.read = True
    addr.read = True
    data.driven = True
    return foo
font_rom_7x12.vhdl_code = \
    """
    --copy this signal declaration to architecture declaration
    signal ${data}_slv : std_logic_vector(6 downto 0);

    ${data} <= unsigned(${data}_slv);
    $name: entity work.font_rom_7x12
        port map (
            clka    => $clk,
            addra   => std_logic_vector($addr),
            douta   => ${data}_slv);
    """


@block
def font_rom_8x12(name, clk, addr, data):
    @always(clk)
    def foo():
        pass

    assert len(addr) == 11, 'addr width = {}, should be 11'.format(len(addr))
    assert len(data) == 8, 'data width = {}, should be 8'.format(len(data))
    clk.read = True
    addr.read = True
    data.driven = True
    return foo
font_rom_8x12.vhdl_code = \
    """
    --copy this signal declaration to architecture declaration
    signal ${data}_slv : std_logic_vector(7 downto 0);

    ${data} <= unsigned(${data}_slv);
    $name: entity work.font_rom_8x12
        port map (
            clka    => $clk,
            addra   => std_logic_vector($addr),
            douta   => ${data}_slv);
    """


@block
def font_rom_10x18(name, clk, addr, data):
    @always(clk)
    def foo():
        pass

    assert len(addr) == 12, 'addr width = {}, should be 12'.format(len(addr))
    assert len(data) == 10, 'data width = {}, should be 8'.format(len(data))
    clk.read = True
    addr.read = True
    data.driven = True
    return foo
font_rom_10x18.vhdl_code = \
    """
    --copy this signal declaration to architecture declaration
    signal ${data}_slv : std_logic_vector(9 downto 0);

    ${data} <= unsigned(${data}_slv);
    $name: entity work.font_rom_10x18
        port map (
            clka    => $clk,
            addra   => std_logic_vector($addr),
            douta   => ${data}_slv);
    """


@block
def font_rom_12x16(name, clk, addr, data):
    @always(clk)
    def foo():
        pass

    assert len(addr) == 11, 'addr width = {}, should be 11'.format(len(addr))
    assert len(data) == 12, 'data width = {}, should be 12'.format(len(data))
    clk.read = True
    addr.read = True
    data.driven = True
    return foo
font_rom_12x16.vhdl_code = \
    """
    --copy this signal declaration to architecture declaration
    signal ${data}_slv : std_logic_vector(11 downto 0);

    ${data} <= unsigned(${data}_slv);
    $name: entity work.font_rom_12x16
        port map (
            clka    => $clk,
            addra   => std_logic_vector($addr),
            douta   => ${data}_slv);
    """