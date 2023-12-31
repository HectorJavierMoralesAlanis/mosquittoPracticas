# python 3.6

import random
import time

from paho.mqtt import client as mqtt_client
import matplotlib.pyplot as plt
import numpy as np

broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
# Generate a Client ID with the publish prefix.
client_id = f'publish-{0}'
# username = 'emqx'
# password = 'public'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 1
    aux=0
    valores=[]
    while True:
        randomValue = random.randint(0,1000)
        time.sleep(1)
        
        msg2 = f"Grafica: {randomValue}"

        valores.append(randomValue)

        result = client.publish(topic, randomValue)
        ##client.publish(topic,randomValue)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg2}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
        aux += 1 
        if msg_count > 10:
            valoresF = np.array(valores)
            result = client.publish(topic,str(valores))
            #valoresF = np.array(valores)
            plt.plot(valoresF,marker = 'o')
            plt.show()
            break


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()


if __name__ == '__main__':
    run()
