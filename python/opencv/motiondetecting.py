import cv2
import time

# lab_windows
# movie = cv2.VideoCapture('C:/Users/Kitadai/Videos/test.mp4')

# droidcam
# movie = cv2.VideoCapture('http://192.168.0.3:4747/video')

# iriun
movie = cv2.VideoCapture(1)

red = (0, 0, 255)  # 枠線の色
before = None  # 前回の画像を保存する変数
fps = int(movie.get(cv2.CAP_PROP_FPS))  # 動画のFPSを取得

while True:
    # 画像を取得
    ret, frame = movie.read()
    # 再生が終了したらループを抜ける
    if ret == False:
        break
    # 白黒画像に変換
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if before is None:
        before = gray.astype("float")
        continue

    # 現在のフレームと移動平均との差を計算
    cv2.accumulateWeighted(gray, before, 0.96)
    frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(before))

    # frameDeltaの画像を２値化
    thresh = cv2.threshold(frameDelta, 3, 255, cv2.THRESH_BINARY)[1]

    # ウィンドウで表示する場合

    # 輪郭のデータを得る
    contours = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    # ウィンドウでの再生速度を元動画と合わせる
    time.sleep(1/fps)

    # 差分があった点を画面に描く
    for target in contours:
        x, y, w, h = cv2.boundingRect(target)
        if w < 30:
            continue  # 小さな変更点は無視
        frame = cv2.rectangle(frame, (x, y), (x+w, y+h), red, 2)
 
    # ウィンドウで表示
    # cv2.imshow('target_frame', gray)
    # cv2.imshow('target_frame', frameDelta)
    # cv2.imshow('target_frame', thresh)
    # cv2.imshow('target_frame', contours)
    cv2.imshow('frame', frame)

    # Enterキーが押されたらループを抜ける
    if cv2.waitKey(1) == 13:
        break

cv2.destroyAllWindows()  # ウィンドウを破棄
