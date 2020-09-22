from abra import visualization as vis
from abra import data

import argparse
import warnings
warnings.filterwarnings("ignore")

"""
Terminal App
filename:
> required argument that has the path to the file you want to import

--eyes_recorded:
> Define which eye data to extract "left", "right", "auto"

--both_eyes_recorded:
> True if both eyes were recorded
> False is only the left or right eyes was being recorded

--mode:
> Mode: d = defualt
> u = user defined
> defualt = d

--start_msg:
> Regular expression of start message for user defined trials
> ex. r"TRIAL \d{1,2} START"

--end_msg:
> Regular expression of end message for user defined trials
> ex. r"TRIAL \d{1,2} END"

--create_epoch:
> True creates timelocking epochs; False creates session by trials

--rm_blinks:
> True removes eye blinks from data; False keeps eye blinks

--buffer:
> Buffer size for eye blink removal

--interpolate:
> defualt: linear
> More options being developed

--event_condition_file:
> path to a csv file that holds timestamps and conditions for time locking epoch

--pre_event:
> milliseconds before defined starting timestamps

--post_event:
> milliseconds after defined starting timestamps

--pupil_baseline:
> Baselining for pupil size data

--start_marker:
> Start trial marker type ['msg', 'input', 'button']

--end_marker:
> End trial marker type ['msg', 'input', 'button']

--input_start:
> Input number set to indicate start trial (int)

--input_end:
> Input number set to indicate end trial (int)

--button_start:
> Button number to indicate start trial and whether button press is start or not
  1 == button press
  0 == button release
  eg. [1,0] button 1 release and [1,1] button 1 press

--button_end:
> Button number to indicate start trial and whether button press is start or not
  1 == button press
  0 == button release
  eg. [1,0] button 1 release and [1,1] button 1 press


"""


parser = argparse.ArgumentParser(description='App arguments')
parser.add_argument('filename',
                    help="Path name to eyetracking data")
parser.add_argument('--eyes_recorded',
                    help='Define which eye data to extract "left", "right", "auto"')
parser.add_argument('--both_eyes_recorded',
                    help='True if both eyes were recorded;    False is only the left or right eyes was being recorded')
parser.add_argument('--mode',
                    help='Mode: d = defualt, u = user defined, defualt = d')
parser.add_argument('--start_msg',
                    help='Regular expression of start message for user defined trials: ex. r"TRIAL \d{1,2} START"')
parser.add_argument('--end_msg',
                    help='Regular expression of end message for user defined trials: ex. r"TRIAL \d{1,2} END"')
parser.add_argument('--create_epoch',
                    help = 'True creates timelocking epochs; False creates session by trials')
parser.add_argument('--rm_blinks',
                    help='True removes eye blinks from data; False keeps eye blinks')
parser.add_argument('--buffer',
                    help='Buffer size for eye blink removal')
parser.add_argument('--interpolate',
                    help='defualt linear')
parser.add_argument('--event_condition_file',
                    help='path to a csv file that holds timestamps and conditions for time locking epoch')
parser.add_argument('--pre_event',
                    help='milliseconds before defined starting timestamps')
parser.add_argument('--post_event',
                    help='milliseconds after defined starting timestamps')
parser.add_argument('--pupil_baseline',
                    help='Baselining for pupil size data')
parser.add_argument('--quality_list',
                    help='True if you want to import a previous quality list file; False is no file exists')
parser.add_argument('--start_marker',
                    help='Start trial marker type [\'msg\', \'input\', \'button\']')
parser.add_argument('--end_marker',
                    help='End trial marker type [\'msg\', \'input\', \'button\']')
parser.add_argument('--input_start',
                    help='Input number set to indicate start trial (int)')
parser.add_argument('--input_end',
                    help='Input number set to indicate end trial (int)')
parser.add_argument('--button_start',
                    help='Button number to indicate start trial and whether button pressed or not \n1 == button \npress 0 == button release \neg. [1,0] button 1 release and [1,1] button 1 press')
parser.add_argument('--button_end',
                    help='Button number to indicate end trial and whether button pressed or not \n1 == button \npress 0 == button release \neg. [1,0] button 1 release and [1,1] button 1 press')
parser.add_argument('--conditions',
                    help='Sessions condition')



args = parser.parse_args()
if args.filename:
    filename = args.filename

if args.eyes_recorded:
    eyes_recorded = args.eyes_recorded
else:
    eyes_recorded = "auto"

if args.both_eyes_recorded:
    both_eyes_recorded = bool(args.both_eyes_recorded)
else:
    both_eyes_recorded = False

if args.mode:
    mode = args.mode
else:
    mode = "d"

if args.start_msg:
    start_msg = args.start_msg
else:
    start_msg=r"TRIAL \d{1,2} START"

if args.end_msg:
    end_msg = args.end_msg
else:
    end_msg=r"TRIAL \d{1,2} END"

if args.create_epoch:
    create_epoch = args.create_epoch
else:
    create_epoch = False

if args.rm_blinks:
    rm_blinks = bool(args.rm_blinks)
else:
    rm_blinks = True

if args.buffer:
    buffer = int(args.buffer)
else:
    buffer=50

if args.interpolate:
    interpolate = args.interpolate
else:
    interpolate='linear'

if args.event_condition_file:
    event_condition_file = args.event_condition_file
else:
    event_condition_file = None

if args.pre_event:
    pre_event = int(args.pre_event)
else:
    pre_event=200

if args.post_event:
    post_event = int(args.post_event)
else:
    post_event=200

if args.pupil_baseline:
    pupil_baseline = list(map(int,args.pupil_baseline))
else:
    pupil_baseline=None

if args.quality_list:
    quality_list = args.quality_list
else:
    quality_list = False

if args.start_marker:
    start_marker = args.end_marker.lower()
else:
    start_marker = 'msg'
print(args.start_marker)
if args.end_marker:
    end_marker = args.end_marker.lower()
else:
    end_marker = 'msg'

if args.input_start:
    input_start = int(args.input_start)
else:
    input_start = None

if args.input_end:
    input_end = int(args.input_end)
else:
    input_end = None

if args.button_start:
     button_start = list(map(int, args.button_start))
else:
    button_start = None

if args.button_end:
    button_end = list(map(int, args.button_end))
else:
    button_end = None
if args.conditions:
    conditions = args.conditions
else:
    conditions = None
# print(args)


def run_app(filename, eyes_recorded = "auto", both_eyes_recorded = False, mode="d", start_msg=r"TRIAL \d{1,2} START",
            end_msg=r"TRIAL \d{1,2} END", create_epoch = False,
            rm_blinks = True, buffer=50,
            interpolate='linear',
            event_condition_file = None, pre_event=200, post_event=200, pupil_baseline=None,
            quality_list = False,
            start_marker = 'msg', end_marker = 'msg', input_start = None,
            input_end = None, button_start = None, button_end = None):

    print("reading in data from ", filename)
    Data = data.read(filename, eyes_recorded = eyes_recorded, both_eyes_recorded = both_eyes_recorded,
                     mode = mode, start_msg = start_msg, end_msg = end_msg)

    if rm_blinks:
        print('Removing eye blinks')
        Data = data.remove_eye_blinks(abra_obj = Data, buffer = buffer, interpolate = interpolate)

    print("creating session")
    print(start_marker)
    sess = Data.create_session(conditions=conditions, start_marker = start_marker,
                       end_marker = end_marker, input_start = input_start, input_end = input_end,
                       button_start = button_start, button_end = button_end)

    print("creating GUI")
    app = vis.Visualization(sess, quality_list = quality_list)
    app.mainloop()

    return app

if __name__ == "__main__":
    run_app(filename = filename, mode = mode, start_msg = start_msg,
                end_msg = end_msg, create_epoch = create_epoch,
                rm_blinks = rm_blinks, buffer = buffer,
                interpolate = interpolate,
                event_condition_file = event_condition_file , pre_event = pre_event,
                post_event = post_event, pupil_baseline = pupil_baseline,
                quality_list = quality_list, start_marker = start_marker,
                end_marker = end_marker, input_start = input_start,
                input_end = input_end, button_start = button_start,
                button_end = button_end)
