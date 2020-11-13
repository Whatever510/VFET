import cv2
import numpy as np
import argparse
import os
import string
import random



def run():
    input_name, output_loc = opt.source,opt.output
    
    if not os.path.isfile(input_name):
        print("[ERROR] Could not find file {}. Please check your input".format(input_name))
        exit()
    if not os.path.exists(output_loc):
        print("[Error] Could not find output directory. Should the directory be created?")
        answer = input("[y/n]")
        if answer.lower() is "y" or answer.lower() is "yes":
            os.mkdir(output_loc)
        else:
            exit()

    cap = cv2.VideoCapture(input_name)
    ret, frame = cap.read()
    height,width,_ = frame.shape
    started = False
    random_name = False
    nbrs_of_frames = 1
    show_help = True
    save_remaining = 0
    runningIndex = 0

    while(True):
        
        if started:
            _, saveFrame = cap.read()
            frame = saveFrame.copy()
            frame = cv2.putText(frame, "[h] Hide/show help",
                                (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0, 0, 255), 2, cv2.LINE_AA)
            if show_help:
                frame = cv2.putText(frame, "[p] Pause video",
                                    (50, 100), cv2.FONT_HERSHEY_SIMPLEX,
                                    1, (0, 0, 255), 2, cv2.LINE_AA)
                frame = cv2.putText(frame, "[space] Save {} frames".format(nbrs_of_frames),
                                    (50, 150), cv2.FONT_HERSHEY_SIMPLEX,
                                    1, (0, 0, 255), 2, cv2.LINE_AA)
                frame = cv2.putText(frame, "[ESC] To exit",
                                    (50, 200), cv2.FONT_HERSHEY_SIMPLEX,
                                    1, (0, 0, 255), 2, cv2.LINE_AA)
        else:
            frame = np.zeros((height,width,3))
            frame = cv2.putText(frame, 'Settings. To switch press key before the setting', (50,50), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0,0,255), 2, cv2.LINE_AA)
            frame = cv2.putText(frame, "[r] RandomName = {}".format(bool(random_name)), (50,100), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0,0,255) , 2, cv2.LINE_AA)
            frame = cv2.putText(frame, "[+/-] Amount of frames saved after key pressed  = {}".format(nbrs_of_frames), (50,150), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0,0,255) , 2, cv2.LINE_AA)

            frame = cv2.putText(frame, "[s] If you press r the video will start",
                                (50, 200), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0, 0, 255), 2, cv2.LINE_AA)
        if frame is None:
            cv2.destroyAllWindows()
            break

        cv2.imshow('image', frame)
        c = cv2.waitKey(int(cap.get(cv2.CAP_PROP_FPS)))

        if c != -1:
            if c == 27:
                cv2.destroyAllWindows()
                break
            if (c == 114 or c == 'r') and not started:
                random_name = ~random_name
            if c == 45:
                nbrs_of_frames-=1 if nbrs_of_frames>1 else 0
            if c == 43:
                nbrs_of_frames += 1 if nbrs_of_frames < 10 else 0
            if c == 115:
                started = True
            if c == 104:
                show_help = ~show_help
            if c == 32 or c == 's':
                save_remaining = nbrs_of_frames
            if c == 112:
                frame = cv2.putText(frame, "VIDEO PAUSED.",
                                    (120, height//2), cv2.FONT_HERSHEY_SIMPLEX,
                                    3, (0, 0, 255), 2, cv2.LINE_AA)
                frame = cv2.putText(frame, "PRESS ANY KEY TO CONTINUE",
                                    (120, height // 2+80), cv2.FONT_HERSHEY_SIMPLEX,
                                    2, (0, 0, 255), 2, cv2.LINE_AA)

                cv2.imshow('image',frame)
                cv2.waitKey(-1)

        if save_remaining != 0:
                if random_name:
                    letters = string.ascii_lowercase
                    filename = ''.join(random.choice(letters) for i in range(10))+".jpg"

                else:
                    filename = output_loc + str(runningIndex) + ".jpg"
                    runningIndex += 1

                cv2.imwrite(filename,saveFrame)
                save_remaining -= 1




        print(save_remaining)







if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Declare input and output")
    
    parser.add_argument("--source",type=str,default="",help="source",required = False)
    parser.add_argument("--output", type = str,default = "",help="output",required=False)

    opt = parser.parse_args()
    if opt.source == "" or opt.output == "":
        print("[ERROR] Please specify input and output path")
        exit()
    run()


