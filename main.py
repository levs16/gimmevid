# Importing the required modules
import cv2
import numpy as np
import random
import string
import simpleaudio as sa

# Defining the app name
app_name = "GimmeVid2"

# Asking the user for the input values
quantity = int(input("How many videos do you want to generate? "))
length = int(input("How long do you want each video to be in seconds? "))
fps = int(input("What frame rate do you want for the videos in frames per second? "))
speed = int(input("What speed do you want for the videos in pixels per second? "))
sound = input("Do you want sound in the videos? (yes/no) ")

# Checking if the user wants sound
if sound.lower() == "yes":
    # Asking the user for the sound parameters
    pitch = int(input("What pitch do you want for the sound in hertz? "))
    frame_sound = input("Do you want to use a new sound every prompted frame or one per all frames? (new/one) ")

# Defining some constants and variables
width = 640 # The width of the video frame in pixels
height = 480 # The height of the video frame in pixels
radius = 10 # The radius of the dot in pixels
font = cv2.FONT_HERSHEY_SIMPLEX # The font for the text
font_size = 1 # The font size for the text
font_color = (255, 255, 255) # The font color for the text (white)
text_length = 10 # The length of the random text in characters
num_frames = length * fps # The number of frames for each video
dot_x = width // 2 # The initial x-coordinate of the dot in pixels
dot_y = height // 2 # The initial y-coordinate of the dot in pixels
dot_color = (0, 0, 0) # The initial color of the dot (black)
bg_color = (255, 255, 255) # The initial color of the background (white)
direction_x = random.choice([-1, 1]) # The initial direction of the dot along x-axis (-1 for left, 1 for right)
direction_y = random.choice([-1, 1]) # The initial direction of the dot along y-axis (-1 for up, 1 for down)

# Generating a sine wave for the sound
sample_rate = 44100 # The sample rate for the sound in samples per second
T = 1 / pitch # The period of the sound wave in seconds
t = np.linspace(0, T, int(T * sample_rate), False) # The time array for one cycle of the sound wave
wave = np.sin(pitch * 2 * np.pi * t) # The amplitude array for one cycle of the sound wave
wave *= 32767 / np.max(np.abs(wave)) # Scaling the amplitude to fit in the range of int16
wave = wave.astype(np.int16) # Converting the amplitude to int16 type

# Creating a loop to generate videos
for i in range(quantity):
    # Creating a video writer object
    video_name = app_name + "_" + str(i+1) + ".avi" # The name of the video file
    fourcc = cv2.VideoWriter_fourcc(*"MJPG") # The codec for the video file
    video_writer = cv2.VideoWriter(video_name, fourcc, fps, (width, height)) # The video writer object

    # Creating a loop to generate frames
    for j in range(num_frames):
        # Creating a blank image as the frame
        frame = np.zeros((height, width, 3), dtype=np.uint8)

        # Filling the frame with a random background color
        bg_color = tuple(random.randint(0, 255) for _ in range(3)) # Generating a random color
        frame[:] = bg_color # Filling the frame with the color

        # Drawing a dot at the center of the frame with a random color
        dot_color = tuple(random.randint(0, 255) for _ in range(3)) # Generating a random color
        cv2.circle(frame, (dot_x, dot_y), radius, dot_color, -1) # Drawing a circle with the color

        # Moving the dot according to the speed and direction
        dot_x += direction_x * speed // fps # Updating the x-coordinate of the dot
        dot_y += direction_y * speed // fps # Updating the y-coordinate of the dot

        # Checking if the dot hits any edge and changing its direction accordingly
        if dot_x - radius <= 0 or dot_x + radius >= width: # If the dot hits left or right edge
            direction_x *= -1 # Changing the direction along x-axis
        if dot_y - radius <= 0 or dot_y + radius >= height: # If the dot hits top or bottom edge
            direction_y *= -1 # Changing the direction along y-axis

        # Putting the current frame number at the left top corner of the frame
        frame_text = "Frame: " + str(j+1) # The text for the frame number
        cv2.putText(frame, frame_text, (10, 30), font, font_size, font_color) # Putting the text on the frame

        # Generating a random text and putting it at a random position on the frame
        random_text = "".join(random.choice(string.ascii_letters) for _ in range(text_length)) # Generating a random text
        text_x = random.randint(0, width - 100) # Generating a random x-coordinate for the text
        text_y = random.randint(0, height - 50) # Generating a random y-coordinate for the text
        cv2.putText(frame, random_text, (text_x, text_y), font, font_size, font_color) # Putting the text on the frame

        # Writing the frame to the video file
        video_writer.write(frame)

        # Playing the sound if the user wants it
        if sound.lower() == "yes":
            # Checking if the user wants a new sound every prompted frame or one per all frames
            if frame_sound.lower() == "new":
                # Generating a new sound with a random pitch
                pitch = random.randint(100, 1000) # Generating a random pitch in hertz
                T = 1 / pitch # The period of the sound wave in seconds
                t = np.linspace(0, T, int(T * sample_rate), False) # The time array for one cycle of the sound wave
                wave = np.sin(pitch * 2 * np.pi * t) # The amplitude array for one cycle of the sound wave
                wave *= 32767 / np.max(np.abs(wave)) # Scaling the amplitude to fit in the range of int16
                wave = wave.astype(np.int16) # Converting the amplitude to int16 type

            # Playing the sound for one frame duration
            play_obj = sa.play_buffer(wave, 1, 2, sample_rate) # Creating a play object for the sound wave
            play_obj.wait_done() # Waiting for the sound to finish playing

    # Releasing the video writer object
    video_writer.release()

    # Printing a message to indicate the completion of video generation
    print("Video", i+1, "generated successfully.")

# Printing a message to indicate the end of program execution
print("Program", app_name, "finished.")
