from datetime import datetime
import random as rnd
import time
import sys, os
from lifxlan import LifxLAN, Light
from appdirs import user_config_dir
from pathlib import Path
import json
CHANGE_INTERVAL = 60*10
DURATION = 2000 # transition duration
RETRIES = 3
RETRY_PAUSE = 5

# hour e.g. 13.5 for 13:30 h | brightness 0 - 1 | kelvin 0 - 1
schedule = [
    [0,      0.1,   0],
    [7,      0.1,   0],
    [8,      1,     1],
    [17,     0.6,   0.5],
    [18,     0.5,   0.25],
    [20,     0.01,  0],
    [24,     0.01,  0]
]


def change(lights:list, b:float, k:float) -> set:
    color = [0, 0, round(b * 65535), round(6500 - 1500) * k + 1500]
    fails = set()

    for retries in range(RETRIES):
        for light in lights:
            light_mac = light.get_mac_addr()
            if light_mac in fails:
                fails.remove(light_mac)
            try:
                light.set_color(color, DURATION)
            except Exception as e:
                print("light failed", light_mac, "...")
                fails.add(light_mac)

        if len(fails) == 0:
            break
        else:
            time.sleep(RETRY_PAUSE)

    return fails

def calc_diff(schedule, time_h):
    # cleaning
    time_h = round(time_h, 2)
    if time_h >= 24:
        time_h = 23.99

    # find start end end slot int times
    for i, slot in enumerate(schedule):
        if time_h < slot[0]:
            start = schedule[i - 1]
            end = schedule[i]
            break

    ratio = round((time_h - start[0]) / (end[0] - start[0]), 2)

    # calc brightness and kevlin from the diff
    b = round(start[1] + (end[1] - start[1]) * ratio, 2)
    k = round(start[2] + (end[2] - start[2]) * ratio, 2)
    return b, k

# Simulate full day
def run_simulation(lights):
    for it in [x * 1 for x in range(0, 25)]:
        result = calc_diff(schedule, it)
        print(f"{it}: {result}")
        time.sleep(0.5)

        for light in lights:
            change(light, result[0], result[1])

def run_random(lights):
    for light in lights:
        b = max(rnd.random(), 0.1)
        k = rnd.random()
        change(light, b, k)

        print(f"random - found {len(lights)} changing to {b} | {k}")


def get_config_file():
    path_folder = os.path.join(user_config_dir(), 'lights')
    Path(path_folder).mkdir(parents=True, exist_ok=True)
    path = os.path.join(path_folder, 'lights.json')
    return path

def load_lamps(path: str) -> (list, dict):
    if os.path.exists(path):
        with open(path, 'r') as fp:
            lights_dict = json.load(fp)

        lights = []
        if lights_dict:
            for mac, value in lights_dict.items():
                light = Light(value['mac'], value['ip'])
                # print('as mac? ', light.get_mac_addr())
                lights.append(light)
    else:
        print("gen")
        lights, lights_dict = find_new_lights(path)

    return lights, lights_dict

def find_new_lights(path, lights_dict:dict={}) -> (list, dict):
    lights = LifxLAN().get_lights()

    before = len(lights_dict)
    for light in lights:
        mac = light.get_mac_addr()
        lights_dict.update({mac: {'label': light.get_label(), 'ip': light.get_ip_addr(), 'mac': mac}})

    if len(lights_dict) > before:
        print("write light config... [find_new_lights]")
        with open(path, 'w') as fp:
            json.dump(lights_dict, fp, indent=4)

    lights = []
    if lights_dict:
        for mac, value in lights_dict.items():
            light = Light(value['mac'], value['ip'])
            lights.append(light)

    return lights, lights_dict

def remove_fails(path, fails, lights_dict:dict) -> dict:
    if len(fails) > 0:
        for fail in fails:
            lights_dict.pop(fail)

        print("write light config... [remove_fails]")
        with open(path, 'w') as fp:
            json.dump(lights_dict, fp, indent=4)

        return lights_dict

def cache_lamps(lights, lights_dict_loaded):
    lights_dict = find_new_lights(CONFIG_PATH, lights_dict_loaded)
    print(f"found {len(lights_dict) - len(lights_dict_loaded)} new lights... {len(lights_dict)} in total:")
    for mac, value in lights_dict.items():
        print(f" > {mac}: '{value['label']}'")

CONFIG_PATH = get_config_file()

def main():
    lights, lights_dict = load_lamps(CONFIG_PATH)

    if len(sys.argv) == 2:
        if 'on' == sys.argv[1]:
            for light in lights:
                light.set_power(1)
        elif 'off' == sys.argv[1]:
            for light in lights:
                light.set_power(0)
        elif 'test' == sys.argv[1]:
            run_simulation(lights)
        elif 'random' == sys.argv[1]:
            run_random(lights)
        elif 'cache' == sys.argv[1]:
            cache_lamps(lights, lights_dict)
        else:
            print("options: on|off|test|random|cache")
    else:
        while True:
            t = datetime.now()
            current_time = round(t.hour + t.minute / 60, 2)
            values = calc_diff(schedule, current_time)

            fails = change(lights, values[0], values[1])
            remove_fails(CONFIG_PATH, fails, lights_dict)
            lights, lights_dict = find_new_lights(CONFIG_PATH, lights_dict)

            print(f"found {len(lights)} changing to {values[0]} | {values[1]}")
            time.sleep(CHANGE_INTERVAL)


