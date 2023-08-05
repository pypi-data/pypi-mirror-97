import smbus
import time
class analogInput():

    def __init__(self, channel=2):
        # Get I2C bus
        self.bus = smbus.SMBus(1)
        
        # I2C address of the device
        self.ADDRESS = 0x48
        
        # PCF8591 Command
        self.PCF8591_CMD =0x40  #Command
        
        self.channel = channel

        # ADS7830 Command 
        self.ADS7830_CMD = 0x84 # Single-Ended Inputs
        
        for i in range(3):
            aa=self.bus.read_byte_data(self.ADDRESS,0xf4)
            if aa < 150:
                self.index="PCF8591"
            else:
                self.index="ADS7830" 

    def analogReadPCF8591(self,chn):#PCF8591 read ADC value,chn:0,1,2,3
        value=[0,0,0,0,0,0,0,0,0]
        for i in range(9):
            value[i] = self.bus.read_byte_data(self.ADDRESS,self.PCF8591_CMD+chn)
        value=sorted(value)
        return value[4]   
    
        
    def recvPCF8591(self,channel):#PCF8591 write DAC value
        while(1):
            value1 = self.analogReadPCF8591(channel)   #read the ADC value of channel 0,1,2,
            value2 = self.analogReadPCF8591(channel)
            if value1==value2:
                break
        voltage = value1 / 256.0 * 3.3  #calculate the voltage value
        voltage = round(voltage,2)
        return voltage
    def recvADS7830(self,channel):
        """Select the Command data from the given provided value above"""
        COMMAND_SET = self.ADS7830_CMD | ((((channel<<2)|(channel>>1))&0x07)<<4)
        self.bus.write_byte(self.ADDRESS,COMMAND_SET)
        while(1):
            value1 = self.bus.read_byte(self.ADDRESS)
            value2 = self.bus.read_byte(self.ADDRESS)
            if value1==value2:
                break
        voltage = value1 / 255.0 * 3.3  #calculate the voltage value
        voltage = round(voltage,2)
        return voltage
        
    def getVoltage(self):
        if self.index=="PCF8591":
            data=self.recvPCF8591(self.channel)
        elif self.index=="ADS7830":
            data=self.recvADS7830(self.channel)
        return data

    #TODO Add more of the analog input functions from wpilib


    def i2cClose(self):
        self.bus.close()