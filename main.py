from machine import I2C, Pin, Timer
import ssd1306
import time
import dht

sensor = dht.DHT11(Pin(2))

temp_timer = Timer(-1)
screen_off = Timer(-2)
set_temp = '18'
in_temp = ''

def turn_off(p):
    display.poweroff()

is_on = False
relay = Pin(0, Pin.OUT)
 
def temp():
    sensor.measure()
    return str(sensor.temperature())
    
def humi():
    sensor.measure()
    return sensor.humidity()

def add_temp(p):
    global set_temp, in_temp
    
    display.poweron()
    if not button_plus.value():
        print('Button pressed!')
        set_temp = str(int(set_temp) + 1)
        display.fill(0)
        display.text("ZADANA: " + set_temp, 0, 5, 1)
        display.show()
        display.text("AKTUALNA: " + in_temp, 0, 25, 1)
        display.show()
        screen_off.init(period=10000, mode=Timer.ONE_SHOT, callback=turn_off)
    
def min_temp(p):
    global set_temp, in_temp
    
    display.poweron()
    if not button_minus.value():
        print('Button pressed!')
        set_temp = str(int(set_temp) - 1)
        display.fill(0)
        display.text("ZADANA: " + set_temp, 0, 5, 1)
        display.show()
        display.text("AKTUALNA: " + in_temp, 0, 25, 1)
        display.show()
        screen_off.init(period=10000, mode=Timer.ONE_SHOT, callback=turn_off)
        
def refresh_temp(p):
    global in_temp, set_temp, is_on, relay

    in_temp_new = temp()
    if in_temp != in_temp_new:
        in_temp = in_temp_new
        display.fill(0)
        display.text("ZADANA: " + set_temp, 0, 5, 1)
        display.show()
        try:
            in_temp = temp()
        except OSError:
            display.fill(0)
            display.text("ZADANA: " + set_temp, 0, 5, 1)
            display.show()
            display.text("AKTUALNA: " + in_temp, 0, 25, 1)
            display.show()
            
        display.text("AKTUALNA: " + in_temp, 0, 25, 1)
        display.show()
        
    if is_on == False and int(in_temp) < int(set_temp):
        relay.on()
        is_on = True
    elif is_on == True and int(in_temp) >= int(set_temp):
        relay.off()
        is_on = False
        
button_plus = Pin(14, Pin.IN, Pin.PULL_UP)
button_minus = Pin(13, Pin.IN, Pin.PULL_UP)

i2c = I2C(-1, Pin(5), Pin(4))
display = ssd1306.SSD1306_I2C(128, 32, i2c)

display.text("MICRO TERMOSTAT", 4, 13, 1)
display.show()

time.sleep(3)

display.fill(0)
display.text("ZADANA: " + set_temp, 0, 5, 1)
display.show()

in_temp = str(temp())
display.text("AKTUALNA: " + in_temp, 0, 25, 1)
display.show()

button_plus.irq(trigger=Pin.IRQ_FALLING, handler=add_temp)
button_minus.irq(trigger=Pin.IRQ_FALLING, handler=min_temp)

temp_timer.init(period=6000, mode=Timer.PERIODIC, callback=refresh_temp)
screen_off.init(period=10000, mode=Timer.ONE_SHOT, callback=turn_off)