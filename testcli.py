#!/usr/bin/env python3

import time
import sys
import brickpi3

try:
    def get_motor_power(port):
        return BP.get_motor_status(port)[1]

    BP = brickpi3.BrickPi3()

    NOTE_TIME = 0.3
    def play_note(power, bpm):
        print("note",2* power / 100)
        start_time = time.time()
        duration = 1 / (bpm / 60)
        BP.set_motor_power(BP.PORT_A,   power/3)
        time.sleep(duration * NOTE_TIME)
        BP.set_motor_power(BP.PORT_A, 0)
        end_time = time.time()
        time.sleep(duration - (end_time - start_time))

    D4 = 146
    G4 = 196
    A4 = 220
    Bb4 = 233
    C5 = 261
    D5 = 294


    def play_notes(notes, bpm):
        for note in notes:
            play_note(note, bpm)

    def D(note):
        return [D4, D4, note]

    NOTES_1 = D(A4) + D(Bb4) + D(C5) + D(A4) + D(Bb4) + [G4]
    NOTES_2 = D(A4) + D(Bb4) + D(D5) + D(A4) + D(Bb4) + [G4]
    NOTES = NOTES_1 + NOTES_2

    for x in range(8):
        play_notes(NOTES, 480)


    while True:
        try:
            val = int(input())
            print(val / 10000)
            for x in range(8):
                play_note(val, 392)
        except(e):
            print(e)
            break



    BP.reset_all()
except:
    BP.reset_all()
