from typing import Literal, Optional


def calculate_time(
    today: Literal[
        "Thứ hai", "Thứ ba", "Thứ tư",
        "Thứ năm", "Thứ sáu", "Thứ bảy", "Chủ Nhật"
    ],
    mentioned_date: Optional[Literal[
        "Thứ hai", "Thứ ba", "Thứ tư",
        "Thứ năm", "Thứ sáu", "Thứ bảy", "Chủ Nhật"
    ]],
    week: Optional[int] = 0,
    absolute_date: Optional[str] = None,
    relative_date: Optional[str] = None
):
    """
    An advanced date calculating tool.
    Please use when user provide "today" and "mentioned date".
    Note that "week" is always POSITIVE
    """

    DATE_ARRAY = [
        "Thứ hai",
        "Thứ ba",
        "Thứ tư",
        "Thứ năm",
        "Thứ sáu",
        "Thứ bảy",
        "Chủ Nhật"
    ]

    if absolute_date:
        return {
            "absolute_date": absolute_date,
            "relative_date": None
        }
    if relative_date:
        return {
            "absolute_date": None,
            "relative_date": relative_date
        }

    start_index = DATE_ARRAY.index(today)
    end_index = DATE_ARRAY.index(mentioned_date)
    if end_index > start_index:
        relative_date = 7 - (end_index - start_index)
    elif end_index < start_index:
        relative_date = end_index - start_index
    else:
        relative_date = 0

    if week >= 1:
        if start_index < end_index:
            add = 7 * (week - 1)
        else:
            add = 7 * week
    else:
        add = 0

    return {
        "absolute_date": None,
        "relative_date": - (relative_date + add)
    }