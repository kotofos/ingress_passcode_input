#/usr/bin/env python3

import subprocess
import argparse
import time

def check_is_not_used(p):
    with open('used_passcodes', 'r') as log:
        for line in log:
            if p in line:
                return False
    return True

def write_to_used_log(p):
    with open('used_passcodes', 'a+') as log:
        log.write('{}\n'.format(p))
    print('writed')

def tap(x, y):
    def to_coord(percent, full_scale):
        return str(int(round(percent * full_scale / 100, 0)))

    res_x = 1440
    res_y = 2560

    x = to_coord(x, res_x)
    y = to_coord(y, res_y)
    adb_input(['tap', x, y])

def input_text(text):
    adb_input(['text', text])

def adb_long_tap(x, y, time_ms):
    x = str(x)
    y = str(y)
    adb_input(['swipe', x, y, x, y, str(time_ms)])

def clear_input(length):
    if length > 0:
        adb_input(['keyevent'] + ['KEYCODE_DEL'] * length)

def adb_input(command):
    subprocess.call(['adb', 'shell', 'input'] + command )

def run():
    arg_parser = argparse.ArgumentParser('input ingress pascodes')
    arg_parser.add_argument('input', help='list of passcodes one per line')
    args = arg_parser.parse_args()

    with open(args.input, 'r') as f:
        passcodes = f.readlines()

    for t in passcodes:
        t = ''.join([x for x in t if ord(x) < 128]) # remove non acsii # todo remove not printable
        t = t.strip()
        if t == '':
            continue

        if check_is_not_used(t):
            print('trying', t)

            input_text(t) # print
            tap(90.3, 91) # submit button
            #_ = input('press enter to continue') # wait user
            write_to_used_log(t) # todo remove used from list ?

            time.sleep(1)
            clear_input(len(t))

        else:
            print(t, 'already used')

if __name__ == '__main__':
    run()
