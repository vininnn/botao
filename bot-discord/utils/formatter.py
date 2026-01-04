# Format the study duration (HH:MM:SS)
def time_formatter(time : int) -> str:
    hours = time // 3600
    minutes = (time % 3600) // 60
    seconds = time % 60

    return f'{hours:02}:{minutes:02}:{seconds:02}'

# def time_formatter_by_time(time: datetime) -> str:
#     total_seconds = (time.total_seconds())
#     hours = total_seconds // 3600
#     minutes = (total_seconds % 3600) // 60
#     seconds = total_seconds % 60

#    return f'{hours:02}:{minutes:02}:{seconds:02}'