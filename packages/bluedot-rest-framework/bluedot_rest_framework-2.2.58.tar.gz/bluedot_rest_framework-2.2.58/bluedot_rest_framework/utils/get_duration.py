from datetime import datetime


def get_duration(start, end):
    if len(start) >= 18:
        start = start.split('T')
        end = end.split('T')
        start = start[0] + " " + start[1][0:5]
        end = end[0] + " " + end[1][0:5]

    start = datetime.strptime(str(start), '%Y-%m-%d %H:%M')
    end = datetime.strptime(str(end), '%Y-%m-%d %H:%M')
    day = (end - start).days
    minute = ((end - start).seconds // 60)
    return day*24*60+minute
