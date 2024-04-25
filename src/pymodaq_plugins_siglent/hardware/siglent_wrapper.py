import pyvisa

serial_address = 'USB0::0xF4EC::0x1102::SDG7ABAD7R0103::INSTR'
rm = pyvisa.ResourceManager()
global siglent
siglent = rm.open_resource(serial_address)

class ActuatorWrapper:
    """
    Attributes:
    -----------
    burst: string
        Burst operating mode, either "ON" or "OFF"

    load: string
        Impedance load, "50" to "100000" Ohm or "HiZ"

    amplitude: float
        Amplitude of the signal, in V
    
    offset: float
        Offset of the signal, in V

    phase: float
        Phase of the signal, in degrees °

    frequency: float   
        Frequency of the signal, in Hz

    cycles: int
        Number of repetition of the burst original signal, only available in "BURST" mode

    trig_src: string
        Trigger source, either "EXT", "INT" or "MAN", only available in "BURST" mode

    delay: float
        Trigger delay, in s (min value is 2.494us and it is not stable when set too high (like 1ms))
    
    wavetype: string
        Wavetype of the signal, either "SINE", "SQUARE", "RAMP", "DC" or "ARB"
        "ARB" as in arbitrary waveform which is sent via EasyWaveX and cannot originate from here

    channel: string
        The output channel, "CH1" by default

    state: string
        Either "ON" or "OFF"
    """

    units = 'V'

    def __init__(self):
        self.address = serial_address
        self.burst = "OFF"
        self.amplitude = 2
        self.offset = 0
        self.phase = 0
        self.frequency = 1000
        self.cycles = 1
        self.trig_src = "INT"
        self.wavetype = "SINE"
        self.channel = "CH1"
        self.state = "OFF"

    def open_communication(self):
        return True

    def set_burst(self, mode):
        """Sets the burst parameter "ON" or "OFF" """
        siglent.write("C1:BTWV STATE," + mode)
        self.mode = mode

    def get_burst_state(self):
        return(self.burst)
    
    def set_amplitude(self, amp):
        """Sets the amplitude to amp, in V"""
        # siglent.write(self.channel + ":" + self.mode + " " + self.carrier
        #               + ',AMP,' + str(amp)) 
        # completement overkill car la commande suivante marche aussi bien
        siglent.write(self.channel + ":BSWV AMP," + str(amp))
        self.amplitude = amp

    def get_amplitude(self):
        return(self.amplitude)
    
    def set_phase(self, phi):
        """Sets the phase to phi, in degrees"""
        # siglent.write(self.channel + ":" + self.mode + " " + self.carrier
        #               + ',PHSE,' + str(phi))
        # completement overkill
        siglent.write(self.channel + ":BSWV PHSE," + str(phi))
        self.phase = phi

    def get_phase(self):
        return(self.phase)
    
    def set_wavetype(self, wtype):
        siglent.write(self.channel + ":BSWV WVTP," + wtype)
        self.wavetype = wtype

    def get_wavetype(self):
        return(self.wavetype)
    
    def set_load(self, load):
        """Sets the load to "HiZ" (ie High Z) or "50" to "100000" Ohm """
        siglent.write(self.channel + ":OUTP LOAD," + load)
        self.load = load

    def get_load(self):
        return(self.load)
    
    def set_trig_src(self, source):
        """Sets the trigger source, either "EXT", "INT" or "MAN"
            only available when burst mode is on"""
        siglent.write(self.channel + ":BTWV TRSR," + source)
        self.trig_src = source
    
    def get_trig_src(self):
        return(self.trig_src)
    
    def set_frequency(self, freq):
        """sets the basewave frequency, in Hz"""
        siglent.write(self.channel + ":BSWV FRQ," + str(freq))
        self.frequency = freq
    
    def get_frequency(self):
        return(self.frequency)
    
    def set_delay(self, time):
        """Sets the delay, in s, only available in BTWV ext trigger mode"""
        siglent.write(self.channel + ":BTWV DLAY," + str(time))
        self.delay = time

    def get_delay(self):
        return(self.delay)
    
    def set_cycles(self, n):
        """Sets the number of repetition of the basewave in the burst, int"""
        siglent.write(self.channel + ":BTWV TIME," + str(n))
        self.cycles = n

    def get_cycles(self):
        return(self.cycles)
    
    def set_state(self, state):
        """Sets the channel output "ON" or "OFF" """
        siglent.write(self.channel + ":OUTP " + state)
        self.state = state

    def get_state(self):
        return(self.state)