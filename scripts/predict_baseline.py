from openai import OpenAI

DAY_MAPPING = {
    0: "Thứ hai",
    1: "Thứ ba",
    2: "Thứ tư",
    3: "Thứ năm",
    4: "Thứ sáu",
    5: "Thứ bảy",
    6: "Chủ nhật"
}

EXAMPLE = """giải khát công viên cùng bạn hai hôm trước tám trăm
```json
{
    "spent_or_received": true,
    "category": {
        "food": "Đồ uống"
    },
    "when": {
        "absolute_date": null,
        "relative_date": -2
    },
    "object": "giải khát",
    "who": "bạn",
    "value": 800000
}
```"""

GEN_JSON_SAVE = """You're a money manager assistant.
Your job is to extract necessary cash flow information from provided sentence
Please ALWAYS response in Python JSON format and in the same language as user

Here's a JSON schema to follow:
{{""$defs"": {{""CashCategory"": {{""description"": ""Only exist ONE field. Field value CAN be null"", ""properties"": {{""food"": {{""anyOf"": [{{""enum"": [""Đồ uống"", ""Ăn sáng"", ""Ăn trưa"", ""Ăn tối"", ""Ăn vặt""], ""type"": ""string""}}, {{""type"": ""null""}}], ""default"": null, ""description"": ""Money used for food"", ""title"": ""Food""}}, ""commute"": {{""anyOf"": [{{""enum"": [""Xăng xe"", ""Gửi xe"", ""Bảo hiểm xe"", ""Thuê xe"", ""Sửa chữa xe""], ""type"": ""string""}}, {{""type"": ""null""}}], ""default"": null, ""description"": ""Money related to commute"", ""title"": ""Commute""}}, ""health_care"": {{""anyOf"": [{{""enum"": [""Khám chữa bệnh"", ""Thuốc men"", ""Thể thao"", ""Bảo hiểm y tế""], ""type"": ""string""}}, {{""type"": ""null""}}], ""default"": null, ""description"": ""Money related to health care"", ""title"": ""Health Care""}}, ""living_expense"": {{""anyOf"": [{{""enum"": [""Tiền điện"", ""Tiền nước"", ""Tiền internet"", ""Tiền gas"", ""Tiền truyền hình"", ""Tiền điện thoại"", ""Tiền siêu thị""], ""type"": ""string""}}, {{""type"": ""null""}}], ""default"": null, ""description"": ""Money related to living expenses"", ""title"": ""Living Expense""}}, ""child_care"": {{""anyOf"": [{{""enum"": [""Học phí"", ""Trông trẻ"", ""Tiền sữa"", ""Tiền bỉm"", ""Tiền đồ chơi"", ""Tiền tiêu vặt""], ""type"": ""string""}}, {{""type"": ""null""}}], ""default"": null, ""description"": ""Money related to child care"", ""title"": ""Child Care""}}, ""clothing"": {{""anyOf"": [{{""enum"": [""Quần áo"", ""Giầy dép"", ""Phụ kiện khác""], ""type"": ""string""}}, {{""type"": ""null""}}], ""default"": null, ""description"": ""Money related to clothing or body accessories"", ""title"": ""Clothing""}}, ""household"": {{""anyOf"": [{{""enum"": [""Đồ đạc trong nhà"", ""Tiền thuê nhà"", ""Thế chấp nhà"", ""Sửa nhà""], ""type"": ""string""}}, {{""type"": ""null""}}], ""default"": null, ""description"": ""Money related to household"", ""title"": ""Household""}}, ""treat_money"": {{""anyOf"": [{{""enum"": [""Vui chơi giải trí"", ""Du lịch"", ""Phim ảnh ca nhạc"", ""Spa & Massage"", ""Mỹ phẩm""], ""type"": ""string""}}, {{""type"": ""null""}}], ""default"": null, ""description"": ""Money used to enjoy or reward yourself"", ""title"": ""Treat Money""}}, ""self_growth"": {{""anyOf"": [{{""enum"": [""Học hành"", ""Xây dựng mối quan hệ""], ""type"": ""string""}}, {{""type"": ""null""}}], ""default"": null, ""description"": ""Money invest in yourself for self improvement"", ""title"": ""Self Growth""}}, ""bank"": {{""anyOf"": [{{""enum"": [""Phí chuyển khoản"", ""Trả lãi vay"", ""Trả nợ ngân hàng""], ""type"": ""string""}}, {{""type"": ""null""}}], ""default"": null, ""description"": ""Money related to bank"", ""title"": ""Bank""}}, ""invest"": {{""anyOf"": [{{""enum"": [""Chứng khoán"", ""Vàng"", ""Tiền số"", ""Trái phiếu"", ""Nhà đất""], ""type"": ""string""}}, {{""type"": ""null""}}], ""default"": null, ""description"": ""Money used in investment"", ""title"": ""Invest""}}}}, ""title"": ""CashCategory"", ""type"": ""object""}}, ""TimeInformation"": {{""properties"": {{""absolute_date"": {{""anyOf"": [{{""type"": ""string""}}, {{""type"": ""null""}}], ""default"": null, ""description"": ""Date in dd-mm format. Null if specific date is not mentioned"", ""title"": ""Absolute Date""}}, ""relative_date"": {{""default"": 0, ""description"": ""How many days from today to said day. Use default value if not mentioned"", ""maximum"": 0, ""title"": ""Relative Date"", ""type"": ""integer""}}}}, ""title"": ""TimeInformation"", ""type"": ""object""}}}}, ""properties"": {{""spent_or_received"": {{""description"": ""Is the money spent on things or received from another. True for spent, False for received"", ""title"": ""Spent Or Received"", ""type"": ""boolean""}}, ""category"": {{""$ref"": ""#/$defs/CashCategory""}}, ""when"": {{""$ref"": ""#/$defs/TimeInformation""}}, ""object"": {{""description"": ""The object that affects the money mentioned in the sentence."", ""title"": ""Object"", ""type"": ""string""}}, ""who"": {{""anyOf"": [{{""type"": ""string""}}, {{""type"": ""null""}}], ""default"": null, ""description"": ""The person mentioned in the sentence"", ""title"": ""Who""}}, ""value"": {{""description"": ""Amount of money"", ""title"": ""Value"", ""type"": ""integer""}}}}, ""required"": [""spent_or_received"", ""category"", ""when"", ""object"", ""value""], ""title"": ""CashFlowInformation"", ""type"": ""object""}}

Output a valid JSON object but do not repeat the schema.
"""

client = OpenAI(
    base_url="http://10.0.4.239:8010/v1",
    api_key="emansieuvc"
)

sentence = "phí chuyển tiền ngân hàng 7 cành."
day = "Thứ hai"
GEN_FORMAT_USER_STR = """{sentence}\nNote that today is {day}"""


completion = client.chat.completions.create(
  model="/qwen-baseline-money-v6-1",
  messages=[
    {"role": "system", "content": GEN_JSON_SAVE},
    {"role": "user", "content": GEN_FORMAT_USER_STR.format(sentence=sentence, day=day)}
  ],
  temperature=0
)

print(completion.choices[0].message.content)    