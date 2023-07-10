import datetime
import math


class Action:
    def __init__(self, start, end, text, date):
        self.start = start
        self.end = end
        self.text = text
        self.date = date


class Day:
    def __init__(self):
        self.day = {}
        for hour in range(24):
            start_one, start_two = [f"{self.convert_hours_string(hour)}:00", f"{self.convert_hours_string(hour)}:30"]
            end_one, end_two = [f"{self.convert_hours_string(hour)}:30", f"{self.convert_hours_string(hour + 1)}:00"]
            self.day[f"{start_one}-{end_one}"] = Action(start_one, end_one, None, datetime.date)
            self.day[f"{start_two}-{end_two}"] = Action(start_two, end_two, None, datetime.date)

    def add_value(self, key, start, end, text, date):
        self.day[key] = Action(start, end, text, date)

    def chart_values(self):
        values = {}
        for key, val in self.day.items():
            t = val.text
            if t is None:
                if "Unknown" not in values:
                    values["Unknown"] = 1
                else:
                    values["Unknown"] += 1
                continue
            if t not in values:
                values[t] = 1
            else:
                values[t] += 1
        return values

    def top_actions(self):
        values = self.chart_values()
        sorted_dict = dict(sorted(values.items(), key=lambda item: item[1]))
        arr = []
        for key, value in sorted_dict.items():
            arr.append(f"{key} - {self.convert_to_hours(value)}")
        arr.reverse()
        return arr[:5]

    @staticmethod
    def convert_to_hours(value):
        if value==0:
            return "0h 0min"
        if value==1:
            return "0h 30min"
        if value%2==0:
            return f"{math.floor(value/2)}h 0min"
        return f"{math.floor(value/2)}h 30min"
    @staticmethod
    def convert_hours_string(hour):
        if hour < 10:
            return f"0{hour}"
        return f"{hour}"

    def __str__(self):
        s = ""
        for key, value in self.day.items():
            s += f"{key}-{value.text}\n"
        return s
