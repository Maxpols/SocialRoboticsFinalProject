from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep
import librosa
import os.path
import numpy as np
import random

# TODO:
# - find more samples of the music genres
# - write rest of code for the introduction of the other genres of music
#       ~ opera
#       ~ jazz
# - update the urls within the main loop
# - Make custom Aruco cards
# - update the total number of genres global var to number of implemented genres

last_seen_marker_id = -1
total_number_of_genres = 4

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
    global last_seen_marker_id
    marker_id = frame['data']['body'][0][-1]  # Get the MarkerID of the detected card
    last_seen_marker_id = marker_id


@inlineCallbacks
def play_music(session, url: str, sleep: int):
    yield session.call("rom.actuator.audio.stream",
                       url=url,
                       sync=False
                       )
    yield sleep(sleep)
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
     
    total_answers = total_number_of_genres
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
            total_answers += total_number_of_genres
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


@inlineCallbacks
def main_loop(session):
    """ Main loop of our game, the robot announces that he will play a sample of a type of music,
        the player is supposed to show the aruco card of the correct type of music."""

    global last_seen_marker_id
    marker_mapping = ["classical", "opera", "jazz", "rock"]

    # this array will store the urls that will be used in the challenges, 
    # they will once again hear samples of the music but now the student has to correctly guess which genre of music it is.
    urls = [["https://audio.jukehost.co.uk/DNmlIMzBfxbZDxN18Q8Wyv8snAsrlmcp", 29, "classical"],
            ["https://audio.jukehost.co.uk/qsDBff84JLT3bk8BR1eA24CZddhcqwu0", 14, "opera"],
            ["https://audio.jukehost.co.uk/5b61OYEWvGYtl95Nv2DtI0aJcdOM4SJb", 20, "jazz"],
            ["https://audio.jukehost.co.uk/KWZF7uKEhj6IW4SbAtvQKSkRa3hshPGW", 28, "rock"]]
    correct_answers = 0
    total_genres = len(urls)
    for i in range(total_genres):
        # Now I will play a random genre
        yield session.call("rie.dialogue.say", text="Now, let me play one of the samples, "
                                                    "please tell me what genre you think it is by showing me the aruco cards."
                                                    "All aruco cards are to be used only once")
        # generating random integer which will select one of the urls
        random_url = random.randint(0, len(urls))
        # Playing of random note(session, selected url, sleep_time associated w selected url)
        play_music(session, urls[random_url][0], [random_url][1])

        aruco_bool = True
        while aruco_bool:
            # aruco card reading and checking answer.
            yield session.subscribe(on_card, "rie.vision.card.stream")
            yield session.call("rie.vision.card.stream")

            if last_seen_marker_id != -1: # the last seen marker is not equal to -1
                aruco_bool = False  # halt the loop
        
        # if the aruco card belongs to the played music
        if marker_mapping[last_seen_marker_id] == urls[random_url][2]:
            correct_answers += 1    # add one point to correct answers
            text = f"good job! That is correct! It was indeed " + marker_mapping[random_url]
            yield session.call("rie.dialogue.say", text)
        else:
            text = "Better luck next time, this was " + urls[random_url][2]
            yield session.call("rie.dialogue.say", text)
        

        # remove the url from the rotation.
        urls.pop(random_url)

    return correct_answers


@inlineCallbacks
def correct_answer(session):
    """ The goal of this function is to avoid code duplication,
        it is called anytime the user guesses the right note within the main game loop.
        The robot will congratulate the user with the correct answer and do a little robot dance"""
    yield session.call("rie.dialogue.say", text="Good you guessed the note! You get one point.")
    yield session.call("rom.optional.behavior.play", name="BlocklyRobotDance")


@inlineCallbacks
def react_to_score(session, correct_answers: int, total_answers: int):
    correct_percent = total_answers / correct_answers

    if correct_percent > 0.55:
        yield happy(session)
    else:
        yield session.call("rom.optional.behavior.play", name="BlocklyShrug")


@inlineCallbacks
def showcase_genres(session):
    """ A small function that iterates through the different genres of music,
        The notes are then played by the robot one by one."""
    classical_music(session)
    opera_music(session)
    jazz_music(session)
    rock_music(session)

    
@inlineCallbacks
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
                        text="don't worry, it's a lovely type of music and I bet you know more than you think! Here let me tell you about classical music:")
    # both lead to the robot explaining some things about classical music
    yield session.call("rie.dialogue.say",
                        text="Classical music is played on string-instruments like the: violin, bass and cello. Though many more instruments are often brought to the party!")
    yield session.call("rie.dialogue.say",
                        text="When a group of people get together to play classical music, they call themselfs: an orchestra. Here is how that sounds like") 
    # plays a sample of classical music
    url = "https://audio.jukehost.co.uk/5uiytuvreqb69AWlncw9eFy7jVWuCsWt"  # url pointing to file with short classical music sample
    sleep_time = 13
    play_music(session, url, sleep_time)
    

@inlineCallbacks
def opera_music(session):
      # message preceding the playing of audio
    yield session.call("rie.dialogue.say",
                           text="Now if you've ever been to a theatre you might have heard of opera!") 
    """Introduce the core concepts of opera, introduction of the word 'vocals' by association with the word singer"""
    yield session.call("rie.dialogue.say",
                           text="Opera is a form of music where they focus on the singers and their vocals, each singer portrays a character in a story." + 
                                "The story is played out on the stage with the several actors. It sounds a little bit like this:") 

    url = "https://audio.jukehost.co.uk/iF9E7Yfu5Cmm8b2Bso8i9NGQ920YkVFK"  # url pointing to file with short opera music sample
    sleep_time = 10
    play_music(session, url, sleep_time)


@inlineCallbacks
def jazz_music(session):
    # message(s) preceding the playing of audio
    """Introduce jazz and mention brass instruments, by naming instruments the student can get some rough idea of what the term describes
        By starting with the trumpet then going to saxophones a picture of what a brass instrument is begins to form meaning that even if the student
        is unfamiliar with the trombone he or she is not confused by these terms"""
    yield session.call("rie.dialogue.say",
                           text="Now here is another interesting music genre: Jazz. The players play all kinds of instruments," + 
                            " but often you'll notice brass instruments like: trumpets, saxophones and trombones") 
    """We hammer home that jazz is based on improvisation over some before-hand agreed base-tune and then queue the jazz music sample."""
    yield session.call("rie.dialogue.say",
                           text="Jazz is a form of music where improvisation is key! The musicians agree beforehand on some base tunes" + 
                                "but while playing they will start to improvise, like this:") 
    
    url = "https://https://audio.jukehost.co.uk/OgAmcWnZQbxZUbWcumTVYhzwiuCjS1AUaudio.jukehost.co.uk/as5c8k0gibu7iN9aavbOsoU4ZgpCG3pz"  # url pointing to file with short jazz music sample
    sleep_time = 25
    play_music(session, url, sleep_time)


@inlineCallbacks
def rock_music(session):
    # message(s) preceding the playing of audio
    """Introduce rock music, as it is quite a broad genre of music we try to describe the instruments that tend to make an appearance
        in a rock song. By description the student is able to individually pick out the sounds that the different instruments make.
        Even though the student may never have heard of a "bass" """
    yield session.call("rie.dialogue.say",
                           text="Perhaps you ever heard the screeching sounds of an electric guitar," + 
                                "banging of the drums and the heavy sound of a bass. That is the sound of rock music" +
                                "often characterized by the electric instruments. Here, listen to this:") 
    
    
    url = "https://audio.jukehost.co.uk/Xpe17EsiHQOiQUknc2TvRpZjxdZ7Lgeh"  # url pointing to file with short rock music sample
    sleep_time = 18
    play_music(session, url, sleep_time)
    


wamp = Component(
    transports=[{
        "url": "ws://wamp.robotsindeklas.nl",
        "serializers": ["msgpack"],
        "max_retries": 0
    }],
    realm="rie.666a203c961f249628fc242a",
)

wamp.on_join(main)

if __name__ == "__main__":
    run([wamp])
