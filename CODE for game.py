
import cv2
import mediapipe as mp
import random
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

def count_fingers(hand_landmarks):
    tips = [8, 12, 16, 20]
    fingers = []

    # Thumb (simple check)
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    for tip in tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers.count(1)

def get_gesture(count):
    if count == 0:
        return "Rock"
    elif count == 2:
        return "Scissors"
    elif count >= 4:
        return "Paper"
    else:
        return "Unknown"

def get_winner(user, comp):
    if user == comp:
        return "Draw"
    elif (user == "Rock" and comp == "Scissors") or \
         (user == "Paper" and comp == "Rock") or \
         (user == "Scissors" and comp == "Paper"):
        return "You Win!"
    else:
        return "Computer Wins!"

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    user_gesture = "None"

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            fingers = count_fingers(handLms)
            user_gesture = get_gesture(fingers)

    comp_choice = random.choice(["Rock", "Paper", "Scissors"])
    winner = get_winner(user_gesture, comp_choice)

    cv2.putText(img, f"Your: {user_gesture}", (10,50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.putText(img, f"Comp: {comp_choice}", (10,100),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

    cv2.putText(img, winner, (10,150),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    cv2.imshow("RPS Game", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
