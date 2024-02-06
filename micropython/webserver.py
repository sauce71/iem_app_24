from time import sleep
import json
from wlan import connect
import uasyncio
from nanoweb import Nanoweb
import urequests

import sensors
from html_functions import naw_write_http_header, render_template
from leds import blink
import buttons

sta_if = connect() # Kobler til trådløst nettverk

naw = Nanoweb() # Lager en instans av Nanoweb

data = dict(
    bme = dict(temperature=0, humidity=0, pressure=0),
    ens = dict(tvoc=0, eco2=0),
    aht = dict(temperature=0, humidity=0),
    )

inputs = dict(touched=False)
    
@naw.route("/")
def index(request):
    naw_write_http_header(request)
    html = render_template(
        'index.html',
        temperature_bme=str(data['bme']['temperature']),
        humidity_bme=str(data['bme']['pressure']),
        pressure=str(data['bme']['pressure']),        
        tVOC=str(data['ens']['tvoc']),
        eCO2=str(data['ens']['eco2']),
        temperature_aht=str(data['aht']['temperature']),
        humidity_aht=str(data['aht']['humidity']),
        )
    await request.write(html)


@naw.route("/api/data")
def api_data(request):
    naw_write_http_header(request, content_type='application/json')
    await request.write(json.dumps(data))

async def control_loop():
    while True:
        if inputs['touched']:
            print('Touched')
            inputs['touched'] = False
            # Her må dere bytte ut med eget navn på trigger og egen nøkkel
            send_data = {'value1': data['bmp']['temperature'],
                    'value2': data['bmp']['pressure'],
                    'value3': data['hdc']['humidity']}
            #r = urequests.post('https://maker.ifttt.com/trigger/send_epost_fra_esp32/with/key/mvte1BsLxR5g0AvW_QxumINgBvboGo_-CpF6C_gIdq1', json=send_data)
            print('IFTTT Status Code:' r.status_code)

        await uasyncio.sleep_ms(500)
    

loop = uasyncio.get_event_loop()
loop.create_task(sensors.collect_sensors_data(data, False))
loop.create_task(buttons.wait_for_touch(inputs))
loop.create_task(naw.run())
loop.create_task(control_loop())

loop.run_forever()
    

