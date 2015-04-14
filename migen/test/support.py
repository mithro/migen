from migen.fhdl.std import *
from migen.sim.generic import run_simulation
from migen.fhdl import verilog


class SimBench(Module):
    callback = None
    def do_simulation(self, selfp):
        if self.callback is not None:
            return self.callback(self, selfp)


def wrap_callback_with_timeout(cb, max_cycles):
    if not max_cycles:
        return cb

    def wrapped_callback(tb, tbp):
        cycles = tbp.simulator.cycle_counter
        assert cycles < max_cycles, "Timeout after %s cycles" % cycles
        cb(tb, tbp)

    return wrapped_callback


class SimCase:
    TestBench = SimBench

    MAX_CYCLES = 100000

    def setUp(self, *args, **kwargs):
        self.tb = self.TestBench(*args, **kwargs)

    def test_to_verilog(self):
        verilog.convert(self.tb)

    def run_with(self, cb, ncycles=None):
        self.tb.callback = wrap_callback_with_timeout(cb, self.MAX_CYCLES)
        run_simulation(self.tb, ncycles=ncycles)
