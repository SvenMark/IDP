import sys
from threading import Timer

sys.path.insert(0, '../../../src')

from entities.movement.sequences.dance_sequence import *

seconds = -4


def routine():
    global seconds
    seconds += 1
    t = Timer(1, routine)
    t.start()


def run(name, control):
    movement = control.movement
    emotion = control.emotion
    shared_object = control.shared_object
    speed_factor = control.speed_factor
    dead_zone = control.dead_zone

    forwards = True
    prev = 0

    routine()

    print("[RUN] " + str(name))

    while not shared_object.has_to_stop():
        print(str(seconds))
        if seconds < 0:
            # COUNTDOWN
            print(str(abs(seconds)))
        elif seconds < 5:
            print("Dums")
            movement.legs.run_sequence(speeds=[100, 100, 100], self_update=True, sequences=None, sequence=drum)
        elif seconds < 12 :
            print("Clap")
            movement.legs.run_sequence(speeds=[100, 100, 100], self_update=True, sequences=None, sequence=clap)
        elif seconds < 19:
            print("Clap and move")
            movement.legs.run_sequence(speeds=[100, 100, 100], self_update=True, sequences=None, sequence=clap)
            if forwards and prev < seconds:
                movement.tracks.forward(60, 65, 0, 0)
                forwards = False
                prev = seconds
            elif not forwards and prev < seconds:
                movement.tracks.backward(60, 65, 0, 0)
                forwards = True
                prev = seconds
        elif seconds < 35:
            print("Ballerina pirouette")
            movement.tracks.turn_right(40, 50, 0, 0)
            movement.legs.run_sequence(speeds=[100, 100, 100], self_update=True, sequences=None, sequence=ballerina)
        elif seconds < 46:
            print("Pirouette wave")
            movement.legs.run_sequence(speeds=[100, 100, 100], self_update=True, sequences=None, sequence=wave)
        elif seconds < 53:
            print("Running man")
            movement.tracks.forward(65, 70, 0, 0)
            movement.legs.run_sequence(speeds=[100, 100, 100], self_update=True, sequences=[0], sequence=running_man)
            movement.tracks.backward(65, 70, 0, 0)
            movement.legs.run_sequence(speeds=[100, 100, 100], self_update=True, sequences=[1], sequence=running_man)
        elif seconds < 59:
            print("Whats goin on?")
            emotion.set_emotion("confused")
            movement.tracks.turn_right(50, 55, 0.2, 0)
            movement.tracks.turn_left(50, 55, 0.2, 0)
        elif seconds < 70:
            emotion.set_emotion("neutral")
            movement.legs.run_sequence(speeds=[200, 200, 200], self_update=True, sequences=None, sequence=clap)
            movement.tracks.turn_right(65, 70, 0.4, 0)
            movement.tracks.turn_left(65, 70, 0.4, 0)
        elif seconds < 80:
            movement.tracks.stop()
            emotion.set_emotion("searching")
            movement.legs.run_sequence(speeds=[200, 200, 200], self_update=True, sequences=None, sequence=drum)
        elif seconds < 90:
            emotion.set_emotion("cycle")
            movement.tracks.forward(45, 50, 0, 0)
            movement.legs.run_sequence(speeds=[100, 100, 100], self_update=True, sequences=[0], sequence=running_man)
            movement.tracks.backward(65, 70, 0, 0)
            movement.legs.run_sequence(speeds=[100, 100, 100], self_update=True, sequences=[1], sequence=running_man)
        elif seconds < 98:
            print("Fast ballerina pirouette")
            emotion.set_emotion("happy")
            movement.tracks.turn_right(95, 100, 0, 2)
            movement.legs.run_sequence(speeds=[150, 150, 150], self_update=True, sequences=None, sequence=ballerina)
        elif seconds < 102:
            print("Fast pirouette wave")
            movement.legs.run_sequence(speeds=[150, 150, 150], self_update=True, sequences=None, sequence=wave)
        elif seconds < 104:
            movement.tracks.stop()
            emotion.set_emotion("shutdown")
        elif seconds < 120:
            emotion.set_emotion("neutral")
            movement.legs.run_sequence(speeds=[100, 100, 100], self_update=True, sequences=None, sequence=left_dab)
            movement.legs.run_sequence(speeds=[100, 100, 100], self_update=True, sequences=None, sequence=right_dab)
        else:
            print("DONE")
            emotion.set_emotion("mad")
            movement.legs.retract()
            shared_object.stop = True

    # Notify shared object that this thread has been stopped
    print("[STOPPED]" + str(name))
    shared_object.has_been_stopped()