import cv2, numpy as np
import sys, json

def main():
    for i in range(1, 5):
        video_in = cv2.VideoCapture('fire{}.mp4'.format(i))
        in_fps = video_in.get(cv2.CAP_PROP_FPS)
        in_resolution = (int(video_in.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video_in.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        overlay_out = cv2.VideoWriter('overlay_fire{}.avi'.format(i), 1482049860, in_fps, in_resolution)
        pc_data = json.load(open('overlay{}i7.avi_log.json'.format(i), 'r'))
        pi_data = json.load(open('overlay{}rpi.avi_log.json'.format(i), 'r'))
        step = (float(in_resolution[0]) / 100., float(in_resolution[1]) / 100.)

        pi_id = 0
        pi_id_repeat_cnt = 0
        for pc_id in range(0, len(pc_data)):
            ok, frame = video_in.read()
            if not ok:
                break
            for bbox in pc_data[pc_id]['bboxes']:
                real_bbox = (
                    (int(bbox['x'] * step[0]), int(bbox['y'] * step[1])),
                    (int(bbox['w'] * step[0]), int(bbox['h'] * step[1]))
                )
                cv2.rectangle(frame, real_bbox[0], real_bbox[1], (0xff, 0, 0), 2)

            pi_id_repeat_cnt = pi_data[pi_id]['frame_num'] - pc_data[pc_id]['frame_num']

            for bbox in pi_data[pi_id]['bboxes']:
                real_bbox = (
                    (int(bbox['x'] * step[0]), int(bbox['y'] * step[1])),
                    (int(bbox['w'] * step[0]), int(bbox['h'] * step[1]))
                )
                cv2.rectangle(frame, real_bbox[0], real_bbox[1], (0, 0, 0), 2)

            overlay_out.write(frame)
            if pi_data[pi_id]['frame_num'] - pc_data[pc_id]['frame_num'] != 0:
                print 'video #{}: frame [#{}, #{}] done'.format(i, pc_data[pc_id]['frame_num'], pi_data[pi_id]['frame_num'])

            if pi_id_repeat_cnt > 0:
                pi_id_repeat_cnt -= 1
            else:
                pi_id += 1

            cv2.waitKey(int(1000 / in_fps))
        overlay_out.release()
        video_in.release()


if __name__ == '__main__':
    main()