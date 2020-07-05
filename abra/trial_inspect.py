from . import visualization
from . import data

import argparse

parser = argparse.ArgumentParser(description='App arguments')
parser.add_argument('--filename',
                    help="Path name to eyetracking data")
parser.add_argument('--mode',
                    help='Mode: d = defualt, u = user defined \ndefualt = d')
parser.add_argument('--start_msg',
                    help='Regular expression of start message for user defined trials\n ex. r"TRIAL \d{1,2} START"')
parser.add_argument('--end_msg',
                    help='Regular expression of end message for user defined trials\nex. r"TRIAL \d{1,2} END"')
parser.add_argument('--create_epoch',
                    help = 'True creates timelocking epochs; False creates session by trials')
parser.add_argument('--rm_blinks',
                    help='True removes eye blinks from data; False keeps eye blinks')
parser.add_argument('--buffer',
                    help='Buffer size for eye blink removal')
parser.add_argument('--interpolate',
                    help='defualt linear')
parser.add_argument('--event_condition_file',
                    help='paht to a csv file that holds timestamps and conditions for time locking epoch')
parser.add_argument('--pre_event',
                    help='milliseconds before defined starting timestamps')
parser.add_argument('--post_event',
                    help='milliseconds after defined starting timestamps')
parser.add_argument('--pupil_baseline',
                    help='Baselining for pupil size data')




args = parser.parse_args()
print(args)

def run_app(filename, mode="d", start_msg=r"TRIAL \d{1,2} START",
            end_msg=r"TRIAL \d{1,2} END", create_epoch = False,
            rm_blinks = True, buffer=50,
            interpolate='linear',
            event_condition_file = None, pre_event=200, post_event=200, pupil_baseline=None):
    Data = data.read(filename, mode, start_msg, end_msg, autoepoch)
    if preprocess:
        Data = data.remove_eye_blinks(Data, buffer, interpolate, inplace)
    sess = Data.create_session()
    app = Visualization(sess)
    app.mainloop()
    return app
