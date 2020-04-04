import smbus
import time


prime_address = 0x19
alt_address = 0x1e
address = alt_address
bus = smbus.SMBus(1)


def registryDump():
    result = []
    for i in range(13):
        result.append(bus.read_byte_data(address,i))
    return result


print('Writing mode value')
bus.write_byte_data(address,2,0x00)

while True:
    try:
        blockResult = registryDump()
        registryOut = ""
        for i in range(13):
            registryOut += "{}\t".format(blockResult[i])
        print(registryOut)
        time.sleep(1)
    except IOError:
        if address == prime_address :
            address = alt_address
        else:
            address = prime_address
        time.sleep(.1)
        print("IO error")
