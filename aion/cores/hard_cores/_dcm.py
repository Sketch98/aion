from myhdl import always, block


@block
def dcm(clk_out_freq, name, clk_in, clk_out, rst_out_n='open'):
    dcms = {
        10: dcm_10mhz,
        20: dcm_20mhz,
    }
    return dcms[clk_out_freq](name, clk_in, clk_out, rst_out_n)


@block
def dcm_10mhz(name, clk_in, clk_out, rst_out_n='open'):
    @always(clk_in)
    def foo():
        pass
    clk_in.read = True
    clk_out.driven = True
    if rst_out_n != 'open':
        rst_out_n.driven = True
    return foo
dcm_10mhz.vhdl_code =\
    """
    $name: entity work.dcm_10mhz
        port map (
            CLKIN_IN        => $clk_in,
            RST_IN          => '0',
            CLKFX_OUT       => $clk_out,
            CLKIN_IBUFG_OUT => open,
            CLK0_OUT        => open,
            LOCKED_OUT      => $rst_out_n);
    """


@block
def dcm_20mhz(name, clk_in, clk_out, rst_out_n='open'):
    @always(clk_in)
    def foo():
        pass
    clk_in.read = True
    clk_out.driven = True
    if rst_out_n != 'open':
        rst_out_n.driven = True
    return foo
dcm_20mhz.vhdl_code =\
    """
    $name: entity work.dcm_20mhz
        port map (
            CLKIN_IN        => $clk_in,
            RST_IN          => '0',
            CLKFX_OUT       => $clk_out,
            CLKIN_IBUFG_OUT => open,
            CLK0_OUT        => open,
            LOCKED_OUT      => $rst_out_n);
    """
