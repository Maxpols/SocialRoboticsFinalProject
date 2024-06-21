"""
Author: Joris Postmus
Date: June 16, 2024
Description: This program runs a guitar note recognition game using a robot interface. 
             The robot introduces itself, plays random guitar notes, and asks the user 
             to identify the notes. Points are awarded for correct guesses, and the user 
             is given the option to play again after a set number of rounds. The current 
             implementation operates in an easy mode where the user needs to recognize one 
             note at a time for a specified number of rounds.
             Check the provided readme for more information on how to run the program.

Settings:
- URLs for guitar note audio files.
- URLs for success and fail audio files.
- Number of rounds for the game.
"""

import random
from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep

# SETTINGS
chordURLS = {
    "A": "https://audio.jukehost.co.uk/dNQshEWsKaC9CBTyaicXGXKNYMR1OO0H",
    "C": "https://audio.jukehost.co.uk/0Ty2zDs2ieXrsGqao2jC24WffTT1ZC0i",
    "D": "https://audio.jukehost.co.uk/7E8kkTF3ZbaLZFuCU4cdL6ZqCRlbImum",
    "E": "https://audio.jukehost.co.uk/ZTjEP8GRbS98YPmshr2IPkF2UtJYUR6S",
    "G": "https://audio.jukehost.co.uk/0C2dTo0xpBEnPWV2rMSJorYQUnB7izU9"
}
successURL = "https://audio.jukehost.co.uk/ExEdJnj8yolYaIX3SdjwX8asJukJ55gx"
failURL = "https://audio.jukehost.co.uk/XNSKFJNIaJnHDvtssNsx9EjYDApqfHfD"
NUM_ROUNDS = 5 # EASY MODE, feel free to reduce for testing purposes

@inlineCallbacks
def main(session):
    """
    Main function that runs the guitar note recognition game.
    """
    answer = yield game_intro(session)

    if answer == "Yes":
        yield play_and_showcase_notes(session)
        correct_answers = yield main_loop(session)
        answer = yield play_again(session, correct_answers)

        if answer == "Yes":
            yield main_loop(session)
        else:
            yield session.call("rie.dialogue.say", text="Oh, well maybe some other time.")
    else:
        yield session.call("rie.dialogue.say", text="Oh, well maybe some other time.")

    session.leave()

@inlineCallbacks
def game_intro(session):
    """
    Introduce the game and ask if the user is ready to play.
    """
    yield session.call("rom.sensor.hearing.info")
    yield session.call("rie.dialogue.config.language", lang="en")

    print("Robot is looking for a face, if the robot appears to freeze, check the code and uncomment the line that makes the robot look at the user first. (Line 49)")
    yield session.call("rie.dialogue.say", text=f"What a beautiful day to learn some guitar notes. Let me look at you first.")
    yield session.call("rie.vision.face.find") # Makes the robot look at the user first, please uncomment if the program appears to freeze, this functionality does not work as well on all robots.
    yield session.call("rom.optional.behavior.play", name="BlocklyWaveRightArm")
    yield session.call("rie.dialogue.say", text="Hi there! It is really nice to see you. My name is Guitary and today I am going to teach you to recognize the 5 most important guitar notes. Namely the notes A, C, D, E and G. Did you know that you can play almost all popular songs using these? For this game, I will randomly play one of those notes and you have to guess which one it is. Each time you guess correctly you will score a point.")
    yield session.call("rie.dialogue.say", text=f"This will be the Easy mode, so you will only need to recognize one note at a time for {NUM_ROUNDS} rounds.")

    question = "Are you ready?"
    answers = {"Yes": ["yes", "jes", "yus", "ja"], "No": ["no", "nee", "nay"]}
    yield session.call("rom.optional.behavior.play", name="BlocklyWaveRightArm")
    answer = yield session.call("rie.dialogue.ask", question=question, answers=answers)
    print(answer)

    return answer

@inlineCallbacks
def play_and_showcase_notes(session):
    """
    Function that plays and showcases the guitar notes to the player.
    """
    yield session.call("rom.optional.behavior.play", name="BlocklyWaveRightArm")
    yield session.call("rie.dialogue.say", text="All right, let me play all the notes for you to start with, try to memorize them as well as you can.")
    notes = ["A", "C", "D", "E", "G"]
    for note in notes:
        yield session.call("rie.dialogue.say", text=f"Let me play the following note for you. {note}.")
        yield session.call("rom.optional.behavior.play", name="BlocklyArmsForward") # This kind of looks like the robot is playing a guitar
        yield sleep(1)
        yield session.call("rom.actuator.audio.stream", url=chordURLS[note], sync=False)
        yield sleep(1)

@inlineCallbacks
def main_loop(session):
    """
    Function that runs the main loop of the guitar note recognition game.
    """
    correct_answers = 0
    notes = ["A", "C", "D", "E", "G"]
    
    for _ in range(NUM_ROUNDS):
        yield session.call("rie.dialogue.say", text="Alright, let me play one of the notes, please try to recognize it")
        
        random_note = random.choice(notes)
        print("The note played is: " + random_note)
        
        yield session.call("rom.actuator.audio.stream", url=chordURLS[random_note], sync=False)
        yield sleep(2)

        question = "Could you please tell me what note I just played?"
        answers = {note: [note, note.lower()] for note in notes}

        answer = yield session.call("rie.dialogue.ask", question=question, answers=answers)
        print(answer)

        if answer == random_note:
            yield correct_answer(session)
            correct_answers += 1
        else:
            yield incorrect_answer(session, random_note)

    return correct_answers

@inlineCallbacks
def play_again(session, correct_answers):
    """
    Informs the user of their score and asks them if they would like to play again.
    """
    question = f"You scored: {correct_answers}, would you like to play again?"
    answers = {"Yes": ["yes", "jes", "yus", "ja"], "No": ["no", "nee", "nay"]}

    if correct_answers >= int(NUM_ROUNDS/2):
        yield session.call("rie.dialogue.say", text=f"{correct_answers} is a really good score by the way, you're getting the hang of this! Let's celebrate!")
        yield session.call("rom.optional.behavior.play", name="BlocklyRobotDance")
    else:
        yield session.call("rie.dialogue.say", text=f"{correct_answers} is not a bad start, you will get there next time. Let's aim for a better score next time!")
        yield session.call("rom.optional.behavior.play", name="BlocklyShrug")
    
    answer = yield session.call("rie.dialogue.ask", question=question, answers=answers)
    return answer

@inlineCallbacks
def correct_answer(session):
    """
    Function that handles a correct answer by playing a positive sound, movement, and verbal queue.
    """
    yield session.call("rom.actuator.audio.stream", url=successURL, sync=False)
    yield session.call("rom.optional.behavior.play", name="BlocklyApplause")
    yield session.call("rie.dialogue.say", text="Good job you guessed the note! You get one point.")

@inlineCallbacks
def incorrect_answer(session, random_note):
    """
    Function that handles an incorrect answer by playing a negative sound, movement, and verbal queue.
    """
    yield session.call("rom.actuator.audio.stream", url=failURL, sync=False)
    yield session.call("rom.optional.behavior.play", name="BlocklyShrug")
    yield sleep(1)
    yield session.call("rie.dialogue.say", text=f"Sorry, but I don't think that was the answer. I played the: {random_note} note. Here is what the {random_note} note sounds like, please remember it for next time")
    yield session.call("rom.actuator.audio.stream", url=chordURLS[random_note], sync=False)
    yield sleep(2)

wamp = Component(
    transports=[{
        "url": "ws://wamp.robotsindeklas.nl",
        "serializers": ["msgpack"],
        "max_retries": 2
    }],
    realm="rie.666ab353961f249628fc272e", # Make sure to change this to your own realm
)

wamp.on_join(lambda session, _: main(session))

if __name__ == "__main__":
    run([wamp])
