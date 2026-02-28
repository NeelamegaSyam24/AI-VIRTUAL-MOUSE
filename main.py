from splash import show_splash
import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import math
import time

# ---------------- SHOW SPLASH ----------------
show_splash()

# ---------------- SETTINGS ----------------
dpi_scale = 1.3
margin = 70

volume_cooldown = 0.4
click_cooldown = 0.6
scroll_speed = 25

# ---------------- SCREEN ----------------
screen_width, screen_height = pyautogui.size()

prev_x, prev_y = 0, 0
last_volume_time = 0
last_click_time = 0
prev_frame_time = 0

# ---------------- MEDIAPIPE ----------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape

    # FPS Display
    current_frame_time = time.time()
    fps = 1 / (current_frame_time - prev_frame_time) if prev_frame_time != 0 else 0
    prev_frame_time = current_frame_time

    cv2.putText(frame, f"FPS: {int(fps)}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    cv2.rectangle(frame, (margin, margin),
                  (w - margin, h - margin),
                  (0, 255, 0), 2)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:

            lm = hand_landmarks.landmark

            thumb_tip = lm[4]
            thumb_ip = lm[3]
            thumb_mcp = lm[2]

            index_tip = lm[8]
            index_pip = lm[6]

            middle_tip = lm[12]
            middle_pip = lm[10]

            ring_tip = lm[16]
            ring_pip = lm[14]

            pinky_tip = lm[20]
            pinky_pip = lm[18]

            wrist = lm[0]

            # Convert to pixels
            thumb_x = int(thumb_tip.x * w)
            thumb_y = int(thumb_tip.y * h)

            wrist_x = int(wrist.x * w)
            wrist_y = int(wrist.y * h)

            index_x = int(index_tip.x * w)
            index_y = int(index_tip.y * h)

            # Finger states
            thumb_up = thumb_tip.y < thumb_ip.y
            index_up = index_tip.y < index_pip.y
            middle_up = middle_tip.y < middle_pip.y
            ring_up = ring_tip.y < ring_pip.y
            pinky_up = pinky_tip.y < pinky_pip.y

            current_time = time.time()

            # ================= THUMB ONLY → CLICK =================
            thumb_vertical = thumb_tip.y < thumb_ip.y < thumb_mcp.y
            thumb_distance = math.hypot(thumb_x - wrist_x, thumb_y - wrist_y)

            thumb_only = (
                thumb_vertical and
                thumb_distance > 70 and
                not index_up and
                not middle_up and
                not ring_up and
                not pinky_up
            )

            if thumb_only:
                if current_time - last_click_time > click_cooldown:
                    pyautogui.click()
                    last_click_time = current_time
                continue

            # ================= 2 FINGERS → VOLUME UP =================
            if (index_up and middle_up and
                not ring_up and not pinky_up and
                not thumb_up):

                if current_time - last_volume_time > volume_cooldown:
                    pyautogui.press("volumeup")
                    last_volume_time = current_time
                continue

            # ================= 4 FINGERS → VOLUME DOWN =================
            if (index_up and middle_up and ring_up and pinky_up and
                not thumb_up):

                if current_time - last_volume_time > volume_cooldown:
                    pyautogui.press("volumedown")
                    last_volume_time = current_time
                continue

            # ================= 5 FINGERS → SCROLL UP =================
            if (thumb_up and index_up and middle_up and ring_up and pinky_up):
                pyautogui.scroll(scroll_speed)
                continue

            # ================= CLOSED FIST → SCROLL DOWN =================
            if (not thumb_up and not index_up and not middle_up and
                not ring_up and not pinky_up):
                pyautogui.scroll(-scroll_speed)
                continue

            # ================= INDEX ONLY → CURSOR =================
            if (index_up and not middle_up and not ring_up and not pinky_up):

                x = max(margin, min(w - margin, index_x))
                y = max(margin, min(h - margin, index_y))

                mapped_x = np.interp(x, (margin, w - margin),
                                     (0, screen_width))
                mapped_y = np.interp(y, (margin, h - margin),
                                     (0, screen_height))

                mapped_x *= dpi_scale
                mapped_y *= dpi_scale

                curr_x = prev_x + (mapped_x - prev_x) / 3
                curr_y = prev_y + (mapped_y - prev_y) / 3

                curr_x = max(1, min(screen_width - 2, curr_x))
                curr_y = max(1, min(screen_height - 2, curr_y))

                pyautogui.moveTo(curr_x, curr_y)

                prev_x, prev_y = curr_x, curr_y

    cv2.imshow("AI Gesture OS", frame)
    cv2.setWindowProperty("AI Gesture OS", cv2.WND_PROP_TOPMOST, 1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()