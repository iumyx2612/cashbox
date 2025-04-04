from llama_index.core.prompts import ChatMessage


GEN_VALUE_SENTENCE_SYSTEM = ("You are a Vietnamese money manager assistant.\n"
                             "These under examples are sentences about spending money "
                             "for {subcategory} which has value is multiple of {value} VND"
                             "indicated by keyword {keyword}\n"
                             "Please generate 10 sentences that have value is multiple "
                             "of {value} VND with same {keyword} "
                             "for {subcategory} similar to the examples.\n"
                             "EXAMPLES:\n{example}")

GEN_VALUE_SENTENCE_USER = "Similar sentences:\n"

GEN_VALUE_SENTENCE_SYSTEM_PROMPT = ChatMessage(
    content=GEN_VALUE_SENTENCE_SYSTEM,
    role="system"
)

GEN_VALUE_SENTENCE_USER_PROMPT = ChatMessage(
    content=GEN_VALUE_SENTENCE_USER,
    role="user"
)


CATEGORY_EXAMPLE_MAPPING = {
    "Đồ uống": {
        "1k": {
            "k": [
                "mua nước uống hết 6k",
                "trà sữa hôm qua ở công viên hết 30 k"
            ],
            "cành": [
                "mua nước uống hết 6 cành",
                "trà sữa hôm qua ở công viên hết 30 cành"
            ],
            "nghìn": [
                "mua nước uống hết 6 nghìn",
                "trà sữa hôm qua ở công viên hết 30 nghìn"
            ],
            "ngàn": [
                "mua nước uống hết 6 ngàn",
                "trà sữa hôm qua ở công viên hết 30 ngàn"
            ]
        },
        "10k": {
            "chục": [
                "mua nước uống hết 6 chục",
                "trà sữa hôm qua ở công viên hết 30 chục",
                "trà đá vỉa hết hết 3,5 chục",
                "sinh tố bơ Thứ bảy chi 4 chục lẻ 6 cành"
            ],
            "sịch": [
                "mua nước uống hết 6 sịch",
                "trà sữa hôm qua ở công viên hết 30 sịch",
                "trà đá vỉa hết hết 3,5 sịch",
                "sinh tố bơ Thứ bảy chi 4 sịch lẻ 6 cành"
            ],
            "xị": [
                "mua nước uống hết 6 xị",
                "trà sữa hôm qua ở công viên hết 30 xị",
                "trà đá vỉa hết hết 3,5 xị",
                "sinh tố bơ Thứ bảy chi 4 xị lẻ 6 cành"
            ],
            "sọi": [
                "mua nước uống hết 6 sọi",
                "trà sữa hôm qua ở công viên hết 30 sọi",
                "trà đá vỉa hết hết 3,5 sọi",
                "sinh tố bơ Thứ bảy chi 4 sọi lẻ 6 cành"
            ]
        },
        "100k": {
            "trăm": [
                "mua nước uống hết 6 trăm",
                "trà sữa hôm qua ở công viên hết 30 trăm",
                "trà đá vỉa hết hết 3,5 trăm",
                "sinh tố bơ Thứ bảy chi 4 trăm 40k",
                "đi vincom mua nước hết 2 trăm mốt",
                "nước khoáng thiên nhiên 2 trăm rưỡi"
            ],
            "lít": [
                "mua nước uống hết 6 lít",
                "trà sữa hôm qua ở công viên hết 30 lít",
                "trà đá vỉa hết hết 3,5 lít",
                "sinh tố bơ Thứ bảy chi 4 lít 3",
                "đi vincom mua nước hết 2 lít mốt",
                "nước khoáng thiên nhiên 2 lít rưỡi",
                "đi vincom mua nước hết 2 lít 40.000 đ",
                "trà sữa Mixue thứ bảy 3 lít 8 chục"
            ],
            "loét": [
                "mua nước uống hết 6 loét",
                "trà sữa hôm qua ở công viên hết 30 loét",
                "trà đá vỉa hết hết 3,5 loét",
                "sinh tố bơ Thứ bảy chi 4 loét 3",
                "đi vincom mua nước hết 2 loét mốt",
                "nước khoáng thiên nhiên 2 loét rưỡi",
                "đi vincom mua nước hết 2 loét 40.000 đ",
                "trà sữa Mixue thứ bảy 3 loét 8 chục"
            ],
            "lốp": [
                "mua nước uống hết 6 lốp",
                "trà sữa hôm qua ở công viên hết 30 lốp",
                "trà đá vỉa hết hết 3,5 lốp",
                "sinh tố bơ Thứ bảy chi 4 lốp 3",
                "đi vincom mua nước hết 2 lốp mốt",
                "nước khoáng thiên nhiên 2 lốp rưỡi",
                "đi vincom mua nước hết 2 lốp 40.000 đ",
                "trà sữa Mixue thứ bảy 3 lốp 8 chục"
            ],
            "líp": [
                "mua nước uống hết 6 líp",
                "trà sữa hôm qua ở công viên hết 30 líp",
                "trà đá vỉa hết hết 3,5 líp",
                "sinh tố bơ Thứ bảy chi 4 líp 3",
                "đi vincom mua nước hết 2 líp mốt",
                "nước khoáng thiên nhiên 2 líp rưỡi",
                "đi vincom mua nước hết 2 líp 40.000 đ",
                "trà sữa Mixue thứ bảy 3 líp 8 chục"
            ]
        },
        "1 triệu": {
            "triệu": [
                "mua nước uống hết 6 triệu",
                "trà sữa hôm qua ở công viên hết 30 triệu",
                "trà đá vỉa hết hết 3,5 triệu",
                "sinh tố bơ Thứ bảy chi 4 triệu 3",
                "đi vincom mua nước hết 2 trệu mốt",
                "nước khoáng thiên nhiên 2 triệu rưỡi",
                "đi vincom mua nước hết 2 triệu 40.000 đ",
                "trà sữa Mixue thứ bảy 3 triệu 8 chục"
            ],
            "m": [
                "mua nước uống hết 6 m",
                "trà sữa hôm qua ở công viên hết 30 m",
                "trà đá vỉa hết hết 3,5 m",
                "sinh tố bơ Thứ bảy chi 4 m 3",
                "đi vincom mua nước hết 2 m mốt",
                "nước khoáng thiên nhiên 2 m rưỡi",
                "đi vincom mua nước hết 2 m 40.000 đ",
                "trà sữa Mixue thứ bảy 3 m 8 chục"
            ],
            "mê": [
                "mua nước uống hết 6 mê",
                "trà sữa hôm qua ở công viên hết 30 mê",
                "trà đá vỉa hết hết 3,5 mê",
                "sinh tố bơ Thứ bảy chi 4 mê 3",
                "đi vincom mua nước hết 2 mê mốt",
                "nước khoáng thiên nhiên 2 mê rưỡi",
                "đi vincom mua nước hết 2 mê 40.000 đ",
                "trà sữa Mixue thứ bảy 3 mê 8 chục"
            ],
            "củ": [
                "mua nước uống hết 6 củ",
                "trà sữa hôm qua ở công viên hết 30 củ",
                "trà đá vỉa hết hết 3,5 củ",
                "sinh tố bơ Thứ bảy chi 4 củ 3",
                "đi vincom mua nước hết 2 củ mốt",
                "nước khoáng thiên nhiên 2 củ rưỡi",
                "đi vincom mua nước hết 2 củ 40.000 đ",
                "trà sữa Mixue thứ bảy 3 củ 8 chục"
            ],
            "chai": [
                "mua nước uống hết 6 chai",
                "trà sữa hôm qua ở công viên hết 30 chai",
                "trà đá vỉa hết hết 3,5 chai",
                "sinh tố bơ Thứ bảy chi 4 chai 3",
                "đi vincom mua nước hết 2 chai mốt",
                "nước khoáng thiên nhiên 2 chai rưỡi",
                "đi vincom mua nước hết 2 chai 40.000 đ",
                "trà sữa Mixue thứ bảy 3 chai 8 chục"
            ],
            "trai": [
                "mua nước uống hết 6 trai",
                "trà sữa hôm qua ở công viên hết 30 trai",
                "trà đá vỉa hết hết 3,5 trai",
                "sinh tố bơ Thứ bảy chi 4 trai 3",
                "đi vincom mua nước hết 2 trai mốt",
                "nước khoáng thiên nhiên 2 trai rưỡi",
                "đi vincom mua nước hết 2 trai 40.000 đ",
                "trà sữa Mixue thứ bảy 3 trai 8 chục"
            ]
        },
        "1 tỷ": {
            "tỷ": [
                "mua nước uống hết 6 tỷ",
                "trà sữa hôm qua ở công viên hết 30 tỷ",
                "trà đá vỉa hết hết 3,5 tỷ",
                "sinh tố bơ Thứ bảy chi 4 tỷ 3",
                "đi vincom mua nước hết 2 tỷ mốt",
                "nước khoáng thiên nhiên 2 tỷ rưỡi",
                "chủ nhật tuần trước mua nước uống hết"
                "đi vincom mua nước hết 2 tỷ 40.000 đ",
                "trà sữa Mixue thứ bảy 3 tỷ 8 chục",
                "mua trà sữa cho công ty hết 3 tỷ 320 triệu"
            ]
        }
    },
}