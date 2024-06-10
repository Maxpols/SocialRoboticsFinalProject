from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep
import librosa
import os.path
import numpy as np
import random

# Functions that activate when the robot's builtin sensors are activated: touch-sensor on head, scanning for aruco, etc
# B--B--BB--B--BB--B--BB--B--BB--B--BB--B--BB--B--BB--B--BB--B--BB--B--BB--B--BB--B--B
@inlineCallbacks
def touched(session, frame):
    """This function is called when the robot is touched on the head"""
    if "body.head.middle" in frame["data"]:
        print("Head touched!")
        yield session.subscribe(on_card, "rie.vision.card.stream")
        yield session.call("rie.vision.card.stream")


@inlineCallbacks
def on_card(session, frame):
    """This function is called every time the robot sees a card"""
    print(frame[0])  # prints the seen MarkerID

    correct_answer = 0  # Set the MarkerID of the correct answer
    current_answer = frame[0]  # Get the MarkerID of the detected card

    if current_answer == correct_answer:
        yield session.call("rie.dialogue.say", text="Amazing! that's the right answer!")
    else:
        yield session.call("rie.dialogue.say", text="Sadly, that's not the right answer, try again!")

# B--B--BB--B--BB--B--BB--B--BB--B--BB--B--BB--B--BB--B--BB--B--BB--B--BB--B--BB--B--B


# Custom made movements, expressions and useful functions that we made over the past few assignments:
# C_-_C C_-_CC_-_C C_-_CC_-_C C_-_CC_-_C C_-_CC_-_C C_-_CC_-_C C_-_CC_-_C C_-_CC_-_C C_-_C
@inlineCallbacks
def neutral(session):
    """Resets the robot to a neutral pose and stops any ongoing audio."""
    yield session.call("rom.optional.behavior.play", name="BlocklyStand")
    yield session.call("rom.actuator.audio.stop", sync=True)  # Stop any audio


@inlineCallbacks
def happy(session):
    # Nod
    yield session.call("rom.actuator.audio.stream",
                       url="https://cdn.pixabay.com/download/audio/2024/01/25/audio_387db2c685.mp3?filename=cute"
                           "-character-wee-1-188162.mp3",
                       sync=False
                       )
    yield session.call("rom.actuator.motor.write",
                       frames=[
                           # Right arm wave motion ! NOTE: The elements of the 'data' dictionary have to always be
                           # the same for all the frames even if the value is the same(e.g. we have to always have
                           # "body.arms.right.upper.pitch" and "body.arms.right.lower.roll" in the dictionary even if
                           # the value is the same for all the frames)
                           {"time": 0, "data": {"body.arms.right.upper.pitch": -2.5, "body.arms.right.lower.roll": 3,
                                                "body.arms.left.upper.pitch": -2.5, "body.arms.left.lower.roll": 3,
                                                "body.head.pitch": 0.0}},
                           {"time": 2000, "data": {"body.arms.right.upper.pitch": -2.5, "body.arms.right.lower.roll": 2,
                                                   "body.arms.left.upper.pitch": -2.5, "body.arms.left.lower.roll": 2,
                                                   "body.head.pitch": 0.175}},
                           {"time": 3000,
                            "data": {"body.arms.right.upper.pitch": -2.5, "body.arms.right.lower.roll": -1,
                                     "body.arms.left.upper.pitch": -2.5, "body.arms.left.lower.roll": -1,
                                     "body.head.pitch": -0.175}},
                           {"time": 4000, "data": {"body.arms.right.upper.pitch": -2.5, "body.arms.right.lower.roll": 3,
                                                   "body.arms.left.upper.pitch": -2.5, "body.arms.left.lower.roll": 3,
                                                   "body.head.pitch": 0.175}},
                           {"time": 5000,
                            "data": {"body.arms.right.upper.pitch": -2.5, "body.arms.right.lower.roll": -1,
                                     "body.arms.left.upper.pitch": -2.5, "body.arms.left.lower.roll": -1,
                                     "body.head.pitch": 0.0}},
                       ],
                       force=True,
                       sync=True
                       )


@inlineCallbacks
def sad(session):
    yield session.call("rom.actuator.audio.stream",
                       url="https://cdn.pixabay.com/download/audio/2022/03/24/audio_714984025d.mp3?filename=crying"
                           "-male-103153.mp3",
                       sync=False
                       )
    # Repeat the sad movement 3 times
    for _ in range(3):
        # Lower the head
        yield session.call("rom.actuator.motor.write",
                           frames=[
                               {"time": 500,
                                "data": {"body.head.pitch": 1.5}},
                           ],
                           force=True,
                           sync=True
                           )
        yield sleep(0.5)

        # Move the arms like a sobbing gesture
        yield session.call("rom.actuator.motor.write",
                           frames=[
                               {"time": 500,
                                "data": {"body.arms.right.upper.pitch": -1.5, "body.arms.right.lower.roll": 0,
                                         "body.arms.left.upper.pitch": -1.5, "body.arms.left.lower.roll": 0}},
                               {"time": 1000,
                                "data": {"body.arms.right.upper.pitch": 0, "body.arms.right.lower.roll": 0,
                                         "body.arms.left.upper.pitch": 0, "body.arms.left.lower.roll": 0}},
                           ],
                           force=True,
                           sync=True
                           )
        yield sleep(0.5)

        # Raise the head
        yield session.call("rom.actuator.motor.write",
                           frames=[
                               {"time": 500,
                                "data": {"body.head.pitch": 0}},
                           ],
                           force=True,
                           sync=True
                           )
        yield sleep(0.5)

    # Make a sad sound or say a sad phrase
    yield session.call("rom.actuator.audio.stream",
                       url="https://cdn.pixabay.com/download/audio/2022/03/24/audio_714984025d.mp3?filename=crying"
                           "-male-103153.mp3",
                       sync=False
                       )

# C_-_C C_-_CC_-_C C_-_CC_-_C C_-_CC_-_C C_-_CC_-_C C_-_CC_-_C C_-_CC_-_C C_-_CC_-_C C_-_C

@inlineCallbacks
def main(session, details):
    info = yield session.call("rom.sensor.hearing.info")
    # setting of standard language to English
    yield session.call("rie.dialogue.config.language", lang="en")

    # smart starting question and keyword answers
    # priming
    question = "Hi, I will teach you some musical notes, are you ready?"
    answers = {"Yes": ["yes", "jes", "yus", "ja"], "No": ["no", "nee", "nay"]}

    answer = yield session.call("rie.dialogue.ask",
                                question=question,
                                answers=answers)
    if answer == "Yes":
        # Message preceding the note showcase
        yield session.call("rie.dialogue.say",
                           text="All right, let me play all the notes for you to start with")
        showcase_notes(session)  # Note showcase (duh)
        correct_answers = main_loop(session)  # enters main game loop

        # Give the option to the user to play again:
        question = "You scored: " + str(correct_answers) + ", would you like to play again?"
        answers = {"Yes": ["yes", "jes", "yus", "ja"], "No": ["no", "nee", "nay"]}

        if correct_answers > 1:
            yield session.call("rom.optional.behavior.play", name="BlocklyDab")
        else:
            yield session.call("rom.optional.behavior.play", name="BlocklyShrug")
        answer = yield session.call("rie.dialogue.ask",
                                    question=question,
                                    answers=answers)
        if answer == "Yes":
            main_loop(session)  # run the main loop another 5 times
        elif answer == "No":
            yield session.call("rie.dialogue.say",
                           text="Oh, well maybe some other time.")
        else:
            yield session.call("rie.dialogue.say",
                           text="Sorry, but I didn't hear you properly.")

    elif answer == "No":
        yield session.call("rie.dialogue.say",
                           text="Oh, well maybe some other time.")
    else:
        yield session.call("rie.dialogue.say",
                           text="Sorry, but I didn't hear you properly.")

    session.leave()  # Close the connection with the robot


def main_loop(session):
    """ Main loop of our game, the robot announces that he will play a note,
        the player is supposed to then say out loud the note that he or she thinks was played.
        Only takes the current session as argument but needs the right .wav files in the Audio directory"""

    correct_answers = 0
    for i in range(5):
        # Now I will play a random note
        yield session.call("rie.dialogue.say", text="Now, let me play one of the notes, "
                                                    "please tell me what note you think it is")
        # generating random note
        random_note1st = random.randint(0, 5) + 65
        random_note2nd = random.randint()
        # Playing of random note
        if os.path.exists(os.path.abspath("Audio\\" + chr(random_note) + ".wav")):
            y, sr = librosa.load("Audio\\" + chr(random_note) + ".wav")
            yield session.call("rom.actuator.audio.play", data=y, rate=sr, sync=True)

        # Please tell me what note it is and listen for response, second smart question and keyword answers
        question = "Could you please tell me what Note I just played?"
        answers = {"A": ["A", "AA"], "B": ["B", "Bee"], "C": ["C", "see"],
                   "D": ["D", "Dee"], "E": ["E", "EE"], "F": ["F", "ehF"]}

        answer = yield session.call("rie.dialogue.ask",
                                    question=question,
                                    answers=answers)
        # Is this note correct?
        if answer == "A" and random_note == int('A'):
            correct_answer(session)
            correct_answers += 1
        elif answer == "B" and random_note == int('B'):
            correct_answer(session)
            correct_answers += 1
        elif answer == "C" and random_note == int('C'):
            correct_answer(session)
            correct_answers += 1
        elif answer == "D" and random_note == int('D'):
            correct_answer(session)
            correct_answers += 1
        elif answer == "E" and random_note == int('E'):
            correct_answer(session)
            correct_answers += 1
        elif answer == "F" and random_note == int('F'):
            correct_answer(session)
            correct_answers += 1

        else:
            yield session.call("rie.dialogue.say",
                               text="Sorry, but I don't think that was the answer."
                                    "I played the: " + chr(random_note) + "note")
    return correct_answers


def correct_answer(session):
    """ The goal of this function is to avoid code duplication,
        it is called anytime the user guesses the right note within the main game loop.
        The robot will congratulate the user with the correct answer and do a little robot dance"""
    yield session.call("rie.dialogue.say", text="Good you guessed the note! You get one point.")
    yield session.call("rom.optional.behavior.play", name="BlocklyRobotDance")


def showcase_notes(session):
    """ A small little function that just iterates through the audio files we have,
        The notes are then played by the robot one by one."""

    for i in range(6):
        # the 65th character in ASCII is 'A'
        note = 65 + i
        if os.path.exists(os.path.abspath("Audio\\" + chr(note) + ".wav")):
            y, sr = librosa.load("Audio\\" + chr(note) + ".wav")
            yield session.call("rom.actuator.audio.play", data=y, rate=sr, sync=True)


wamp = Component(
    transports=[{
        "url": "ws://wamp.robotsindeklas.nl",
        "serializers": ["msgpack"],
        "max_retries": 0
    }],
    realm="rie.66350585c887f6d074f03970",
)

wamp.on_join(main)

if __name__ == "__main__":
    run([wamp])
