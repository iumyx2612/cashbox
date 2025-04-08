from typing import Literal, Optional


def calculate_time(
    today: Literal[
        "Thứ hai", "Thứ ba", "Thứ tư",
        "Thứ năm", "Thứ sáu", "Thứ bảy", "Chủ Nhật"
    ],
    mentioned_date: Optional[Literal[
        "Thứ hai", "Thứ ba", "Thứ tư",
        "Thứ năm", "Thứ sáu", "Thứ bảy", "Chủ Nhật"
    ]] = None,
    week: Optional[int] = 0,
    absolute_date: Optional[str] = None,
    relative_date: Optional[int] = None
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
            "relative_date": -int(relative_date)
        }
    if mentioned_date is None:
        mentioned_date = today
    
    start_index = DATE_ARRAY.index(today)
    end_index = DATE_ARRAY.index(mentioned_date)
    if end_index > start_index and week == 0:
        week = 1
    days_diff = (start_index - end_index) + 7 * week
    
    return {
        "absolute_date": None,
        "relative_date": -days_diff
    }   
