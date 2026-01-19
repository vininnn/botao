def time_formatter(time : int) -> str:
    """Converts a duration in seconds into a formatted HH:MM:SS string.

    Args:
        time (int): Total duration in seconds.

    Returns:
        str: Formatted time string (e.g., "01:30:15")
    """
    hours = time // 3600
    minutes = (time % 3600) // 60
    seconds = time % 60

    return f'{hours:02}:{minutes:02}:{seconds:02}'
