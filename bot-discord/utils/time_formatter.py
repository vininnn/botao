# Format the study duration (HH:MM:SS)
def time_formatter(time) -> str:
    total_seconds = int(time.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return f'{hours:02}:{minutes:02}:{seconds:02}'
