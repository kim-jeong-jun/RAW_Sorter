# -----------------------------------------------------------------------------
# Copyright (c) 2019, Jeong-Jun Kim. All Rights Reserved.
# -----------------------------------------------------------------------------

import os
import shutil
import tqdm
import time
import exifread

From = input("input directory: ")
To = input("destination directory: ")

start = time.time()
totalFileCount = 0
trashCount = 0
negCount = 0
ovlCount = 0
sortedCount = 0
fileCount = 0
processed = 0


def process(directory):
    global fileCount, trashCount, processed
    files = list(os.walk(directory))
    toSort = []
    for dirpath, dirnames, filenames in files:
        fileCount += len([x for x in filenames if os.path.splitext(x)[-1].lower() in ('.nef', '.dng', '.jpg')])

    for dirpath, dirnames, filenames in files:
        for file in [x for x in filenames if os.path.splitext(x)[-1].lower() in ('.nef', '.dng', '.jpg')]:
            toSort.append((dirpath, file))

    for dirpath, file in tqdm.tqdm(toSort):
        filepath = dirpath + "/" + file
        try:
            configPhoto(filepath, file)
        except Exception as e:
            pass

# TODO : configPhoto 단계 진입 자체를 확장자로 걸러야함.
#  안그러면 ratio가 100 %를 넘어버림;
#  100 %는 안 넘는데, 왜 아닌 것까지 옮기지?


def configPhoto(fromDir, filename):
    toDir = configData(fromDir, filename)
    sorting(fromDir, toDir, filename)


def configData(filepath, filename):
    currentPhoto = open(filepath, 'rb')
    tag = exifread.process_file(currentPhoto)

    cameraTag = "Image Model"
    if cameraTag in tag:
        camera = str(tag[cameraTag])
        if not camera:
            camera = "Misc"
    else:
        camera = "Misc"

    shootTimeTag = "EXIF DateTimeOriginal"
    if shootTimeTag in tag:
        shootTime = str(tag[shootTimeTag])
        if not shootTime:
            shootTime = "0000:00:00 0000:0000"
    else:
        shootTime = "0000:00:00 0000:0000"

    timeArray = shootTime.split(" ")[0].split(":")
    year = timeArray[0]
    month = timeArray[1]
    day = timeArray[2]
    return To + "/" + camera.strip() + "/" + year + "/" + "/" + year + "-" + month + "-" + day


def sorting(fromDir, toDir, filename):
    global sortedCount, ovlCount, negCount, trashCount
    # 개수 Count를 광역 변수로 지정
    tryDir = toDir + "/" + filename
    # 이동하고자 하는 폴더를 정의
    toRedundant = toDir + "/Redundant"
    # 중복일 경우 폴더의 이름과 해당 경로를 정의

    if not os.path.isdir(toDir):
        # 이동하려던 경로가 없을 경우,
        os.makedirs(toDir)
        # 경로를 생성

    if os.path.isfile(tryDir):
        # 중복 경로 조회
        tryRebundant = toRedundant + "/" + filename
        # 중복 경로를 생성
        if os.path.isfile(tryRebundant):
            # print(f"Rebundance exists!:")
            # 중복 경로에도 파일이 있는 경우, 아무 것도 하지 않고 Count만 함
            negCount += 1
        else:
            if not os.path.isdir(toRedundant):
                # 중복 경로가 없으면
                os.makedirs(toRedundant)
                # 중복 경로를 만듦

            shutil.move(fromDir, toRedundant)
            # 해당 파일을 이동
            ovlCount += 1
            # 중복 Count
            # print(f"Already exists!")

    else:
        shutil.move(fromDir, tryDir)
        # 둘 다 아닌 경우, 필요한 경로로 이동
        # print(f"Sorted to")
        sortedCount += 1
    ratio = 100 * (ovlCount + negCount + sortedCount) / fileCount
    # print(f"Progress: {'%0.4f' % float(ratio)} %", end='\n\r')


process(From)


def s_to_time(num):
    return time.strftime('%H:%M:%S', time.gmtime(int(num)))


print(f"\n\nTotal : {sortedCount + negCount + ovlCount} files.\n"  # 총 사진 수
      f" - Sorted : {sortedCount} files.\n"  # 옮긴 사진 수 
      f" - Overlaped  : {ovlCount} files.\n"  # 중복 사진 수 
      f" - Neglection : {negCount} files.\n"  # 제낀 사진 수 
      f"\nTotal Running time : {s_to_time(time.time() - start)}")  # 총 진행 시간
