import os

from myhdl import block, Signal, intbv, always_comb, always

from simple_components import counter
from structural_decorators import chain


def _prime_factors(n):
    powers_two = 0
    while n % 2 == 0:
        powers_two += 1
        n //= 2
    
    factors = []
    prime_file = '\\'.join([os.path.dirname(__file__), '_primes.txt'])
    with open(prime_file) as p:
        for line in p:
            i = int(line.strip())
            while n % i == 0:
                factors.append(i)
                n //= i
            if n == 1:
                break
        else:
            factors.append(n)
    return powers_two, tuple(factors[::-1])


@chain('clk_in', 'clk_out')
@block
def div_two(clk_in=None, clk_out=None, master_clk=None):
    clk_reg = Signal(False)
    
    @always_comb
    def foo():
        clk_out.next = clk_reg
    
    if master_clk is None:
        @always(clk_in.posedge)
        def bar():
            clk_reg.next = not clk_reg
        
        return foo, bar
    
    last_clk_in = Signal(False)
    
    @always(master_clk.posedge)
    def bar():
        last_clk_in.next = clk_in
        if clk_in and not last_clk_in:
            clk_reg.next = not clk_reg
    
    return foo, bar


@chain('clk_in', 'chain_out')
@block
def odd_duty_cycle_50_div(divide_by, clk_in, clk_out, master_clk=None):
    threshold = divide_by // 2
    if master_clk is None:
        pos_count = Signal(intbv(0, min=0, max=divide_by))
        neg_count = Signal(intbv(0, min=0, max=divide_by))
        
        @always(clk_in.posedge)
        def pos_counter():
            pos_count.next = pos_count + 1
            if pos_count == divide_by - 1:
                pos_count.next = 0
        
        @always(clk_in.negedge)
        def neg_counter():
            neg_count.next = neg_count + 1
            if neg_count == divide_by - 1:
                neg_count.next = 0
        
        @always_comb
        def foo():
            clk_out.next = 0
            if pos_count > threshold or neg_count > threshold:
                clk_out.next = 1
        
        return pos_counter, neg_counter, foo
    
    pos_count = Signal(intbv(0, min=0, max=divide_by))
    neg_count = Signal(intbv(0, min=0, max=divide_by))
    
    last_clk_in_pos = Signal(bool(0))
    last_clk_in_neg = Signal(bool(0))
    
    @always(master_clk.posedge)
    def pos_counter():
        last_clk_in_pos.next = clk_in
        if clk_in and not last_clk_in_pos:
            if pos_count == divide_by - 1:
                pos_count.next = 0
            else:
                pos_count.next += 1
    
    @always(master_clk.negedge)
    def neg_counter():
        last_clk_in_neg.next = clk_in
        if not clk_in and last_clk_in_neg:
            if neg_count == divide_by - 1:
                neg_count.next = 0
            else:
                neg_count.next += 1
    
    @always_comb
    def foo():
        clk_out.next = 0
        if pos_count > threshold or neg_count > threshold:
            clk_out.next = 1
    
    return pos_counter, neg_counter, foo


@block
def clk_div(divide_by, clk_in, clk_out, duty_cycle_50=False):
    """a clk divider based on prime factorization."""
    if divide_by == 1:
        @always_comb
        def pass_through():
            clk_out.next = clk_in
        
        return pass_through
    
    powers_two, factors = _prime_factors(divide_by)
    # print(powers_two)
    # print(factors)
    
    if not factors:
        return div_two(clk_in=clk_in, clk_out=clk_out, num_chains=powers_two)
    if powers_two == 0:
        if duty_cycle_50:
            if len(factors) == 1:
                return odd_duty_cycle_50_div(factors[0], clk_in=clk_in,
                                             clk_out=clk_out)
            return odd_duty_cycle_50_div(list(factors), clk_in=clk_in,
                                         clk_out=clk_out,
                                         num_chains=len(factors))
        else:
            return counter(clk_in, list(factors), pulse_out=clk_out,
                           num_chains=len(factors))
    odd_divs_clk_out = Signal(False)
    odd_divs = counter(clk_in, max_value=list(factors),
                       pulse_out=odd_divs_clk_out,
                       num_chains=len(factors))
    
    div_twos = div_two(clk_in=odd_divs_clk_out, clk_out=clk_out,
                       num_chains=powers_two)
    
    return odd_divs, div_twos
