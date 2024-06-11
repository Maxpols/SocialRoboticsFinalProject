from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep
import librosa
import os.path
import numpy as np
import random

# TODO:
# - write rest of code for the introduction of the other genres of music
# - Write code that interprets the aruco cards (Joris has some of this code)
# - Make custom Aruco cards
# - find more samples of the music genres
# IF ACCESS TO ROBOT:
# - test code written so far, as we'll be boilerplating alot of the code we just need to test one of each kind (showcase -> challenge -> aruco check)


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


@inlineCallbacks
def play_music(session, url: str):
    yield session.call("rom.actuator.audio.stream",
                       url=url,
                       sync=False
                       )
    yield session.call("rom.actuator.audio.stop")
    session.leave()  # Close the connection with the robot
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
    question = "Hi, today I will learn you about different music genres, or types! Are you ready?"
    answers = {"Yes": ["yes", "jes", "yus", "ja"], "No": ["no", "nee", "nay"]}

    answer = yield session.call("rie.dialogue.ask",
                                question=question,
                                answers=answers)
     
    total_answers = 5
    correct_answers = 0
    if answer == "Yes":
        # Message preceding the note showcase
        showcase_genres(session)  # showcases the different genres of music, playing a small sample and giving some additional information
        yield session.call("rie.dialogue.say",
                           text="Okay, now I will play some samples of one of the  music genres I just described to you!" +
                           "Now it's your job to hold up the card with the right genre of music on it, for every correct guess you get a point")
        correct_answers += main_loop(session)  # enters main game loop

        # function that will have the robot react with joy or shrug depending on the students score,
        # currently the function is set to react with if the student got more than 55% correct
        react_to_score(session, correct_answers, total_answers)

        # Give the option to the user to play again:
        question = "You scored: " + str(correct_answers) + ", would you like to play again?"
        answer = {"Yes": ["yes", "jes", "yus", "ja"], "No": ["no", "nee", "nay"]}
  
        answer = yield session.call("rie.dialogue.ask",
                                    question=question,
                                    answers=answers)
        if answer == "Yes":
            total_answers += 5
            yield session.call("rie.dialogue.say",
                           text="Okay, here we go again!")
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
    """ Main loop of our game, the robot announces that he will play a sample of a type of music,
        the player is supposed to show the aruco card of the correct type of music."""

    # this array will store the urls that will be used in the challenges, 
    # they will once again hear samples of the music but now the student has to correctly guess which genre of music it is.
    urls = ["classical_music_url",
             "Opera_music_url",
             "pop_music_url"]
    correct_answers = 0
    for i in range(5):
        # Now I will play a random genre
        yield session.call("rie.dialogue.say", text="Now, let me play one of the samples, "
                                                    "please tell me what note you think it is")
        # generating random integer which will select one of the urls
        random_url = random.randint(0, len(urls))
        # Playing of random note
        play_music(session, urls[random_url])
        urls.pop(random_url)

        # aruco card reading and checking answer.


    return correct_answers


def correct_answer(session):
    """ The goal of this function is to avoid code duplication,
        it is called anytime the user guesses the right note within the main game loop.
        The robot will congratulate the user with the correct answer and do a little robot dance"""
    yield session.call("rie.dialogue.say", text="Good you guessed the note! You get one point.")
    yield session.call("rom.optional.behavior.play", name="BlocklyRobotDance")


def react_to_score(session, correct_answers: int, total_answers: int):
    correct_percent = total_answers / correct_answers

    if correct_percent > 0.55:
        yield happy(session)
    else:
        yield session.call("rom.optional.behavior.play", name="BlocklyShrug")


def showcase_genres(session):
    """ A small function that iterates through the different genres of music,
        The notes are then played by the robot one by one."""
    classical_music(session)
    opera_music(session)

    

def classical_music(session):
    # message preceding the playing of audio
    """repetition of the same word (classical music) and interaction in the form of a smart question
       ensures engagement (through the smart question) and stresses the term "classical music" 
       improving chance of it being remembered by the student"""
    question = "For the first genre I would like to introduce you to: classical music! Have you heard of classical music?"
    answers = {"Yes": ["yes", "jes", "yus", "ja"], "No": ["no", "nee", "nay"]}

    """Basic information and some interaction to upkeep engagement"""
    answer = yield session.call("rie.dialogue.ask",
                                question=question,
                                answers=answers)
    if answer == "Yes":
        # compliment the student, positive reinforcement and affirmation motivate participation
        yield session.call("rie.dialogue.say",
                           text="Wow, you know your music! But did you know that:")
    elif answer == "No":
        # relativize to not discourage and lead on with the information
        yield session.call("rie.dialogue.say",
                        text="don't worry, it's a lovely type of music and I bet you know more than you say! Here let me tell you about classical music:")
    # both lead to the robot explaining some things about classical music
    yield session.call("rie.dialogue.say",
                        text="Classical music is played on string-instruments like the: violin, bass and cello. Though many more instruments are often brought to the party!")
    yield session.call("rie.dialogue.say",
                        text="When a group of people get together to play classical music, they call themselfs: a orchestra. Here is how that sounds like") 
    # plays a sample of classical music
    url = "x"  # url pointing to file with short classical music sample
    play_music(session, url)


def opera_music(session):
    # same setup as above
    pass

    


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
