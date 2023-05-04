from slab.instruments import SerialInstrument
import time


class TT075(SerialInstrument):
        def __init__(self,name="hemt_power_supply",address='COM3',enabled=True,timeout=1):
            SerialInstrument.__init__(self,name,address,enabled,timeout)

            self.read_sleep=0.01


        def set_slot(self, slot, verbose=False):
            """
            Set the slot you want to set 
            Valid arguments are 1 or 2, power on default is 1
            """

            if verbose:
                self.read() # clear buffer

            if int(slot) in [1, 2]:
                 cmd = 'S' + str(int(slot)) + ';'
                 self.write(cmd)
            else: print('Slot should be 1 or 2')

            if verbose:
                rep = self.read()
                if rep[:-1] == 'S' + str(int(slot)) + '!':
                    print('Slot set on: %i'%slot)
                else: 
                    print('Slot could not be set')

        def set_channel(self, channel, verbose=False):
            """
            Set the channel you want to set 
            Valid arguments are 1 or 2, power on default is 1
            """

            if verbose:
                self.read() # clear buffer

            if int(channel) in [1, 2]:
                 cmd = 'C' + str(int(channel)) + ';'
                 self.write(cmd)
            else: print('Channel should be 1 or 2')

            if verbose:
                rep = self.read()
                if rep[:-1] == 'C' + str(int(channel)) + '!':
                    print('Channel set on: %i'%channel)
                else: 
                    print('Channel could not be set')

        def get_drain_voltage(self, channel, slot=1):
            """Get the drain voltage on the active channel and slot"""

            self.set_channel(channel)
            self.set_slot(slot)
            self.read() # clear buffer
            cmd = 'd;'
            self.write(cmd)
            V_in_volt = float(self.read()[1:-2])/1e3
            print('Drain voltage set to: %.3f V'%V_in_volt)

        def get_gate_voltage(self, channel, slot=1):
            """Get the gate voltage on the active channel and slot"""

            self.set_channel(channel)
            self.set_slot(slot)

            self.read() # clear buffer
            cmd = 'g;'
            self.write(cmd)
            V_in_volt = float(self.read()[1:-2])/1e3
            print('Gate voltage set to: %.3f V'%V_in_volt)

        def get_drain_current(self, channel, slot=1):
            """Get the gate voltage on the active channel and slot"""

            self.set_channel(channel)
            self.set_slot(slot)

            self.read() # clear buffer
            cmd = 'i;'
            self.write(cmd)
            I_in_mA = float(self.read()[1:-2])/1e3
            print('Drain current set to: %.3f mA'%I_in_mA)

        def set_drain_voltage(self, voltage, channel, slot=1, verbose=False, mesure=False):
            """ Set the drain voltage on the active channel and slot"""

            self.set_channel(channel, verbose)
            self.set_slot(slot, verbose)

            cmd = 'D%.1f;'%(voltage*1e3)
            self.write(cmd)
            if mesure:
                self.get_drain_voltage(channel, slot)

        def set_gate_voltage(self, voltage, channel, slot=1, verbose=False, measure=False):

            """ Set the gate voltage on the active channel and slot"""

            self.set_channel(channel, verbose)
            self.set_slot(slot, verbose)

            cmd = 'G%.1f;'%(voltage*1e3)
            self.write(cmd)
            if measure:
                self.get_gate_voltage(channel, slot)

        def on(self):
            """ Switch on the active channel and slot"""

            cmd = 'N;'
            self.write(cmd)

        def off(self):
            """ Switch off the active channel and slot"""

            cmd = 'F;'
            self.write(cmd)

        def switch_on(self, slot=1, channel=1, drain_voltage=0, gate_voltage=0, verbose=True):
            """ 
            Recommended way to switch on the active channel and slot
            It set the drain and gate voltage and then switch on the channel
            """

            self.set_drain_voltage(drain_voltage, channel, slot, verbose)
            self.set_gate_voltage(gate_voltage, channel, slot, verbose=False)
            self.on()
            if verbose:
                print('Channel switched on')
                self.get_drain_voltage(channel, slot)
                self.get_gate_voltage(channel, slot)

        def switch_off(self, slot=1, channel=1, verbose=True):

            """ 
            Recommended way to switch off the active channel and slot
            It switch off the channel and then set the drain and gate voltage to 0
            """
            self.set_slot(slot, verbose)
            self.set_channel(channel, verbose)
            self.off()
            self.set_drain_voltage(0, slot, channel, verbose)
            self.set_gate_voltage(0, slot, channel, verbose)
            if verbose:
                print('Channel switched off')
                self.get_drain_voltage(channel, slot)
                self.get_gate_voltage(channel, slot)
            
        




