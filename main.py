from datetime import datetime, timedelta
from slots import busy

START_TIME = '09:00'
END_TIME = '21:00'

SLOT_DURATION = 30

TIME_FORMAT = '%H:%M'

start_time = datetime.strptime(START_TIME, TIME_FORMAT)
end_time = datetime.strptime(END_TIME, TIME_FORMAT)


def convert_slots_into_datetime(busy_intervals: list[dict]) -> list[dict]:
    busy_periods: list[dict] = [
        create_slot_dict_datetime(interval['start'], interval['stop'])
        for interval in busy_intervals]

    return busy_periods


def create_slot_dict(start, end) -> dict:
    return {'start': start.strftime(TIME_FORMAT),
            'end': end.strftime(TIME_FORMAT)}


def create_slot_dict_datetime(start, end) -> dict:
    return {'start': datetime.strptime(start, TIME_FORMAT),
            'end': datetime.strptime(end, TIME_FORMAT)}


def get_free_slots(start, end, busy_intervals, slot_size):

    busy_periods: list[dict] = convert_slots_into_datetime(busy_intervals)

    busy_periods.sort(key=lambda period: period['start'])

    delta: timedelta = timedelta(minutes=slot_size)

    current_time = start

    free_slots: list[dict] = []

    temp_busy = iter(busy_periods)
    temp_busy_period = next(temp_busy, None)

    while current_time + delta < end:

        if temp_busy_period and current_time + delta > temp_busy_period['start']:
            current_time = max(temp_busy_period['end'], current_time)
            temp_busy_period = next(temp_busy, None)
            continue

        slot = create_slot_dict(current_time, current_time + delta)
        free_slots.append(slot)

        current_time += delta

    return free_slots


def print_slots(slots):
    for index, slot in enumerate(slots):
        print(f"{index + 1}. Свободное окно: {slot['start']} - {slot['end']}")


free_windows = get_free_slots(start_time, end_time, busy, SLOT_DURATION)

print_slots(free_windows)
