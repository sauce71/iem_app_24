from machine import Pin, TouchPad
import uasyncio

TOUCH_PIN = 4
TOUCH_TRIGGER_VALUE = 320

was_touched = False


touchpad = TouchPad(Pin(TOUCH_PIN, Pin.IN, Pin.PULL_UP))

async def wait_for_touch(inputs):
    counter = 0
    while True:
        counter += 1
        if (counter % 200) == 0: # Printer verdien hvert 10. sekund pga 100 ms pause lenger ned
            print('Touchpad value', touchpad.read())
        
        if touchpad.read() < TOUCH_TRIGGER_VALUE: # Hvis større en trigger verdi
            inputs['touched'] = True
            await uasyncio.sleep_ms(5000) # Venter5  sek for å unngå retrigger
        await uasyncio.sleep_ms(100)

def test():
    inputs = dict(touched=False)
    loop = uasyncio.get_event_loop()
    loop.create_task(wait_for_touch(inputs))
    loop.run_forever()

if __name__ == '__main__':
    test()