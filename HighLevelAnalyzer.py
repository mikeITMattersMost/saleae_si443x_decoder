from typing import Iterable, Optional, Union
from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame, StringSetting, NumberSetting, ChoicesSetting

si_registers = {
	0x00: "Device Type (R)",
	0x01: "Device Version (R)",
	0x02: "Device Status (R)",
	0x03: "Interrupt Status 1 (R)",
	0x04: "Interrupt Status 2 (R)",
	0x05: "Interrupt Enable 1 (R/W)",
	0x06: "Interrupt Enable 2 (R/W)",
	0x07: "Operating & Function Control 1 (R/W)",
	0x08: "Operating & Function Control 2 (R/W)",
	0x09: "Crystal Oscillator Load Capacitance (R/W)",
	0x0A: "Microcontroller Output Clock (R/W)",
	0x0B: "GPIO0 Configuration (R/W)",
	0x0C: "GPIO1 Configuration (R/W)",
	0x0D: "GPIO2 Configuration (R/W)",
	0x0E: "I/O Port Configuration (R/W)",
	0x0F: "ADC Configuration (R/W)",
	0x10: "ADC Sensor Amplifier Offset (R/W)",
	0x11: "ADC Value (R)",
	0x12: "Temperature Sensor Control (R/W)",
	0x13: "Temperature Value Offset (R/W)",
	0x14: "Wake-Up Timer Period 1 (R/W)",
	0x15: "Wake-Up Timer Period 2 (R/W)",
	0x16: "Wake-Up Timer Period 3 (R/W)",
	0x17: "Wake-Up Timer Value 1 (R)",
	0x18: "Wake-Up Timer Value 2 (R)",
	0x19: "Low-Duty Cycle Mode Duration (R/W)",
	0x1A: "Low Battery Detector Threshold (R/W)",
	0x1B: "Battery Voltage Level (R)",
	0x1C: "IF Filter Bandwidth (R/W)",
	0x1D: "AFC Loop Gearshift Override (R/W)",
	0x1E: "AFC Timing Control (R/W)",
	0x1F: "Clock Recovery Gearshift Override (R/W)",
	0x20: "Clock Recovery Oversampling Ratio (R/W)",
	0x21: "Clock Recovery Offset 2 (R/W)",
	0x22: "Clock Recovery Offset 1 (R/W)",
	0x23: "Clock Recovery Offset 0 (R/W)",
	0x24: "Clock Recovery Timing Loop Gain 1 (R/W)",
	0x25: "Clock Recovery Timing Loop Gain 0 (R/W)",
	0x26: "Received Signal Strength Indicator (R)",
	0x27: "RSSI Threshold for Clear Channel Indicator (R/W)",
	0x28: "Antenna Diversity Register 1 (R)",
	0x29: "Antenna Diversity Register 2 (R)",
	0x2A: "AFC Limiter (R/W)",
	0x2B: "AFC Correction Read (R)",
	0x2C: "OOK Counter Value 1 (R/W)",
	0x2D: "OOK Counter Value 2 (R/W)",
	0x2E: "Slicer Peak Hold (R/W)",
	0x2F: "Reserved (0x2F)",
	0x30: "Data Access Control (R/W)",
	0x31: "EzMAC status 0 (R)",
	0x32: "Header Control 1 (R/W)",
	0x33: "Header Control 2 (R/W)",
	0x34: "Preamble Length (R/W)",
	0x35: "Preamble Detection Control (R/W)",
	0x36: "Sync Word 3 (R/W)",
	0x37: "Sync Word 2 (R/W)",
	0x38: "Sync Word 1 (R/W)",
	0x39: "Sync Word 0 (R/W)",
	0x3A: "Transmit Header 3 (R/W)",
	0x3B: "Transmit Header 2 (R/W)",
	0x3C: "Transmit Header 1 (R/W)",
	0x3D: "Transmit Header 0 (R/W)",
	0x3E: "Transmit Packet Length (R/W)",
	0x3F: "Check Header 3 (R/W)",
	0x40: "Check Header 2 (R/W)",
	0x41: "Check Header 1 (R/W)",
	0x42: "Check Header 0 (R/W)",
	0x43: "Header Enable 3 (R/W)",
	0x44: "Header Enable 2 (R/W)",
	0x45: "Header Enable 1 (R/W)",
	0x46: "Header Enable 0 (R/W)",
	0x47: "Received Header 3 (R)",
	0x48: "Received Header 2 (R)",
	0x49: "Received Header 1 (R)",
	0x4A: "Received Header 0 (R)",
	0x4B: "Received Packet Length (R)",
	0x4C: "Reserved (0x4C)",
	0x4D: "Reserved (0x4D)",
	0x4E: "Reserved (0x4E)",
	0x4F: "ADC8 Control (R/W)",
	0x50: "Reserved (0x50)",
	0x51: "Reserved (0x51)",
	0x52: "Reserved (0x52)",
	0x53: "Reserved (0x53)",
	0x54: "Reserved (0x54)",
	0x55: "Reserved (0x55)",
	0x56: "Reserved (0x56)",
	0x57: "Reserved (0x57)",
	0x58: "Reserved (0x58)",
	0x59: "Reserved (0x59)",
	0x5A: "Reserved (0x5A)",
	0x5B: "Reserved (0x5B)",
	0x5C: "Reserved (0x5C)",
	0x5D: "Reserved (0x5D)",
	0x5E: "Reserved (0x5E)",
	0x5F: "Reserved (0x5F)",
	0x60: "Channel Filter Coefficient Address (R/W)",
	0x61: "Reserved (0x61)",
	0x62: "Crystal Oscillator/Control Test (R/W)",
	0x63: "Reserved (0x63)",
	0x64: "Reserved (0x64)",
	0x65: "Reserved (0x65)",
	0x66: "Reserved (0x66)",
	0x67: "Reserved (0x67)",
	0x68: "Reserved (0x68)",
	0x69: "AGC Override 1 (R/W)",
	0x6A: "Reserved (0x6A)",
	0x6B: "Reserved (0x6B)",
	0x6C: "Reserved (0x6C)",
	0x6D: "TX Power (R/W)",
	0x6E: "TX Data Rate 1 (R/W)",
	0x6F: "TX Data Rate 0 (R/W)",
	0x70: "Modulation Mode Control 1 (R/W)",
	0x71: "Modulation Mode Control 2 (R/W)",
	0x72: "Frequency Deviation (R/W)",
	0x73: "Frequency Offset 1 (R/W)",
	0x74: "Frequency Offset 2 (R/W)",
	0x75: "Frequency Band Select (R/W)",
	0x76: "Nominal Carrier Frequency 1 (R/W)",
	0x77: "Nominal Carrier Frequency 0 (R/W)",
	0x78: "Reserved (0x78)",
	0x79: "Frequency Hopping Channel Select (R/W)",
	0x7A: "Frequency Hopping Step Size (R/W)",
	0x7B: "Reserved (0x7B)",
	0x7C: "TX FIFO Control 1 (R/W)",
	0x7D: "TX FIFO Control 2 (R/W)",
	0x7E: "RX FIFO Control (R/W)",
	0x7F: "FIFO Access (R/W)"
}

def get_register_name(register_addr: int) -> str:
    try:
        return si_registers[register_addr]
    except KeyError:
        return "UNKNOWN_REGISTER"

class Hla(HighLevelAnalyzer):
    
    result_types = {
        "si_address": {"format": "{{data.rw}} {{data.reg}} {{data.value}}"},
        "si_read": {"format": "{{data.rw}} {{data.reg}} {{data.value}}"},
        "si_write": {"format": "{{data.rw}} {{data.reg}} {{data.value}}"},        
    }

    def __init__(self):
        # Previous frame type
        # https://support.saleae.com/extensions/analyzer-frame-types/spi-analyzer
        self._previous_type: str = ""
        # current address
        self._address: Optional[int] = None
        # current access type
        self._rw: str = ""
        
    def decode(self, frame: AnalyzerFrame) -> Optional[Union[Iterable[AnalyzerFrame], AnalyzerFrame]]:
        """ Decode frames. """
        is_first_byte: bool = self._previous_type == "enable"
        self._previous_type: str = frame.type
        
        if frame.type != "result":
            return None
            
        mosi: bytes = frame.data["mosi"]
        miso: bytes = frame.data["miso"]
        
        #print("mosi bytes: ", mosi)
        #print("miso bytes: ", miso)
        
        if is_first_byte:
            try:
                self._address = mosi[0]
            except IndexError:
                return None

            self._rw = "Write" if self._address & 0x80 != 0 else "Read"

            # normalize the address, removing the read/write bit
            self._address &= 0x7F

            return AnalyzerFrame(
                "si_address",
                start_time=frame.start_time,
                end_time=frame.end_time,
                data={"reg": get_register_name(self._address), "rw": self._rw, "value": "reg_"+f"0x{self._address:02X}"},
            )
            
        else:
            if self._rw.lower() == "write":
                try:
                    byte = mosi[0]
                except IndexError:
                    return None
            else:
                try:
                    byte = miso[0]
                except IndexError:
                    return None

            ret = AnalyzerFrame(
                "si_"+self._rw.lower(),
                start_time=frame.start_time,
                end_time=frame.end_time,
                data={
                    "reg": get_register_name(self._address),
                    "rw": self._rw,
                    "value": self._rw.lower()+"-> "+f"0x{byte:02X}" + " = ASCII "+chr(byte),                                        
                },
            )

            if self._address != 0xFF:  # FIFO
                self._address += 1
                self._address &= 0x7F

            return ret            
            
            
