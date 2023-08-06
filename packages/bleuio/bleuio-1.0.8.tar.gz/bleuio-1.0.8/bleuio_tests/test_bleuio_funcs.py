# (C) 2021 Smart Sensor Devices AB

import time

from bleuio_lib.bleuio_funcs import BleuIo

# Start // BleuIo(debug=True)
my_dongle = BleuIo()
my_dongle.start_daemon()


def simplescan():
    # Saves the response (string list) of the ATI command to the status variable
    status = my_dongle.ati()
    for i in status:
        # Prints each line of status variable
        print(i)
        # Checks if dongle is in Peripheral
        # If it is it puts the dongle in Central Mode to allow scanning
        if i.__contains__("Peripheral"):
            setCentral = my_dongle.at_central()
            for l in setCentral:
                print(l)

    # Runs a scan for 4 seconds then prints out the results, line by line
    my_dongle.at_gapscan(4)
    scan_result = my_dongle.rx_scanning_results
    for y in scan_result:
        print(y)


simplescan()

# Some more examples of almost every function
# print(my_dongle.help())
#print(my_dongle.at_central())
#print(my_dongle.at_set_passkey("123456"))
#print(my_dongle.at_set_passkey())
#print(my_dongle.at_numcompa("0"))
#print(my_dongle.at_gapiocap("1"))
#print(my_dongle.at_gapconnect("[0]00:00:00:00:0D:D0"))
#print(my_dongle.at_gappair())
#time.sleep(2)
#print(my_dongle.at_numcompa())
#print(my_dongle.at_enter_passkey("123456"))
#print(my_dongle.at_cancel_connect())
#time.sleep(2)
#print(my_dongle.at_get_services())
#print(my_dongle.at_setnoti("0021"))
#print(my_dongle.at_sec_lvl("1"))
#print(my_dongle.at_sec_lvl())
#print(my_dongle.at_gapiocap("1"))
#print(my_dongle.at_numcompa("0"))
#print(my_dongle.at_numcompa("1"))
# print(my_dongle.at_peripheral())
# print(my_dongle.at())
# print(my_dongle.ate(0))
# print(my_dongle.ati())
# print(my_dongle.ate(1))
# print(my_dongle.at_advdata())
# print(my_dongle.at_advdata("04:09:43:41:54"))
# print(my_dongle.at_advdatai("ebbaaf47-0e4f-4c65-8b08-dd07c98c41ca0000000000"))
# time.sleep(2)
# print(my_dongle.at_advstart())
# time.sleep(2)
# print(my_dongle.at_advstop())
# print(my_dongle.at_advstart("1","500","600","20"))
# time.sleep(2)
# print(my_dongle.at_advstop())
# print(my_dongle.at_central())
# print(my_dongle.at_findscandata(""))
# time.sleep(6)
# print(my_dongle.stop_scan())
# find = my_dongle.rx_scanning_results
# print("my_dongle.at_findscandata()")
# print("="*21)
# for line in find:
#     print(line)
# print("="*21)
# cmd = my_dongle.at_gapconnect("[0]40:48:FD:E5:2C:D9")
# time.sleep(0.5)
# print(cmd)
# cmd = my_dongle.at_gapdisconnect()
# print(cmd)
# print(my_dongle.at_gapscan(10))
# find = my_dongle.rx_scanning_results
# print("my_dongle.at_gapscan(10)")
# print("="*21)
# for line in find:
#     print(line)
# print("="*21)
# print("="*21)
# print(my_dongle.at_gapscan())
# time.sleep(3)
# print(my_dongle.stop_scan())
# gapscan = my_dongle.rx_scanning_results
# print("my_dongle.at_gapscan()")
# print("="*21)
# for line in gapscan:
#     print(line)
# print("="*21)
# print(my_dongle.at_gapstatus())
# cmd = my_dongle.at_gattcread("000b")
# print(cmd)
# cmd = my_dongle.at_gattcwrite("000b", "HEJ")
# print(cmd)
# cmd = my_dongle.at_gattcwriteb("000b", "010101")
# print(cmd)
# print(my_dongle.at_scantarget("[1]F3:D1:ED:AD:8A:10"))
# time.sleep(3)
# print(my_dongle.stop_scan())
# scan = my_dongle.rx_scanning_results
# print("my_dongle.at_scantarget([1]F3:D1:ED:AD:8A:10)")
# print("="*21)
# print(scan)
# print("="*21)
#cmd = my_dongle.at_spssend("howdy")
#print(cmd)
# cmd = my_dongle.at_spssend()
# print(cmd)
# my_dongle._send_command("Hello")
# my_dongle.stop_sps()
# time.sleep(0.5)
