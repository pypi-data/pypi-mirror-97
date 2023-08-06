"""Everthing that has do with time"""


import datetime


class Time:

    def __init__(self):
        pass

    def get_today_at_time(self, hours, minutes):
        today = datetime.datetime.today()
        today_at_h = today.replace(hour=hours, minute=minutes, second=0, microsecond=0)
        return today_at_h

    def get_date_today_from_h_m_string(self, h_m_string):
        time = h_m_string.split(":")
        today_at_time = self.get_today_at_time(int(time[0]), int(time[1]))
        return today_at_time

    def format_break_time(self, break_time):
        if ':' in break_time:
            split = break_time.split(":")
            delta = datetime.timedelta(
                hours=int(split[0]), minutes=int(split[1]))
            return delta.seconds/3600
        return float(break_time.replace(",", "."))
