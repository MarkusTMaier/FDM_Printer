import librtd
import time

i = 0
while i < 10:
    temperature = librtd.get(0,7)
    temperature = round(temperature, 2)
    i = i+1
    print(f"The temperature is currently {temperature} °C")
    time.sleep(5)

print("Done!")