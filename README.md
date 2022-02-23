# Si4430/31/32 Decoder
  
Decodes register reads and writes to the Silicon Labs Si4430/31/32 radio.
This is a fork from [saleae_rfm69_decoder ](https://github.com/newAM/saleae_rfm69_decoder) which I mainly modified to match the registers of the Si443x ICs.


## Features

* Annotates the first byte of SPI transfers with "Read {register}" or "Write {register}" 
* Annotates following bytes with "Read {register} {value}" or "Write {register} {value}"


## Example
![Example](https://github.com/mikeITMattersMost/saleae_si443x_decoder/blob/main/sihla_demo.png?raw=true)
