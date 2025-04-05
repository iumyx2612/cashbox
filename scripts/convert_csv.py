import pandas as pd
from tqdm import tqdm
BASELINE_SYSTEM_PROMPT = """You're a money manager assistant.
Your job is to extract necessary cash flow information from provided sentence
Please ALWAYS response in Python JSON format and in the same language as user

Here's a JSON schema to follow:
{{"$defs": {{"CashCategory": {{"description": "Only exist ONE field. Field value CAN be null", "properties": {{"food": {{"anyOf": [{{"enum": ["Đồ uống", "Ăn sáng", "Ăn trưa", "Ăn tối", "Ăn vặt"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money used for food", "title": "Food"}}, "commute": {{"anyOf": [{{"enum": ["Xăng xe", "Gửi xe", "Bảo hiểm xe", "Thuê xe", "Sửa chữa xe", "Thuế phí"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money related to commute", "title": "Commute"}}, "health_care": {{"anyOf": [{{"enum": ["Khám chữa bệnh", "Thuốc men", "Thể thao", "Bảo hiểm y tế"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money related to health care", "title": "Health Care"}}, "living_expense": {{"anyOf": [{{"enum": ["Tiền điện", "Tiền nước", "Tiền internet", "Tiền gas", "Tiền truyền hình", "Tiền điện thoại"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money related to living expenses", "title": "Living Expense"}}, "shopping": {{"anyOf": [{{"enum": ["Tiền siêu thị", "Tiền đi chợ"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money related to shopping", "title": "Shopping"}}, "child_care": {{"anyOf": [{{"enum": ["Học phí", "Trông trẻ", "Tiền sữa", "Tiền bỉm", "Tiền đồ chơi", "Tiền tiêu vặt"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money related to child care", "title": "Child Care"}}, "clothing": {{"anyOf": [{{"enum": ["Quần áo", "Giầy dép", "Phụ kiện khác"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money related to clothing or body accessories", "title": "Clothing"}}, "gifts_donations": {{"anyOf": [{{"enum": ["Thăm hỏi", "Biếu tặng"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money used for gifts or donations", "title": "Gifts Donations"}}, "household": {{"anyOf": [{{"enum": ["Đồ đạc trong nhà", "Tiền thuê nhà", "Sửa nhà"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money related to household", "title": "Household"}}, "treat_money": {{"anyOf": [{{"enum": ["Vui chơi giải trí", "Du lịch", "Phim ảnh ca nhạc", "Spa & Massage", "Mỹ phẩm", "Nhậu nhẹt"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money used to enjoy or reward yourself", "title": "Treat Money"}}, "pets": {{"anyOf": [{{"enum": ["Chó", "Mèo"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money invest in your pets", "title": "Pets"}}, "self_growth": {{"anyOf": [{{"enum": ["Học hành", "Xây dựng mối quan hệ"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money invest in yourself for self improvement", "title": "Self Growth"}}, "bank": {{"anyOf": [{{"enum": ["Phí chuyển khoản", "Trả lãi vay", "Trả nợ ngân hàng"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money related to bank", "title": "Bank"}}, "invest": {{"anyOf": [{{"enum": ["Chứng khoán", "Vàng", "Tiền số", "Nhà đất"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money used in investment", "title": "Invest"}}, "saving": {{"anyOf": [{{"enum": ["Gửi tiền tiết kiệm", "Cho vay"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money used for saving or lending", "title": "Saving"}}, "income": {{"anyOf": [{{"enum": ["Lương", "Thưởng", "Thu hồi nợ", "Kinh doanh", "Trợ cấp", "Rút tiết kiệm", "Bán tài sản"], "type": "string"}}, {{"type": "null"}}], "default": null, "description": "Money used for income", "title": "Income"}}}}, "title": "CashCategory", "type": "object"}}, "TimeInformation": {{"properties": {{"absolute_date": {{"anyOf": [{{"type": "string"}}, {{"type": "null"}}], "default": null, "description": "Date in dd-mm format. Null if specific date is not mentioned", "title": "Absolute Date"}}, "relative_date": {{"default": 0, "description": "How many days from today to said day. Use default value if not mentioned", "maximum": 0, "title": "Relative Date", "type": "integer"}}}}, "title": "TimeInformation", "type": "object"}}}}, "properties": {{"spent_or_received": {{"description": "Is the money spent on things or received from another. True for spent, False for received", "title": "Spent Or Received", "type": "boolean"}}, "category": {{"$ref": "#/$defs/CashCategory"}}, "when": {{"$ref": "#/$defs/TimeInformation"}}, "object": {{"description": "The object that affects the money mentioned in the sentence.", "title": "Object", "type": "string"}}, "who": {{"anyOf": [{{"type": "string"}}, {{"type": "null"}}], "default": null, "description": "The person mentioned in the sentence", "title": "Who"}}, "value": {{"description": "Amount of money", "title": "Value", "type": "integer"}}}}, "required": ["spent_or_received", "category", "when", "object", "value"], "title": "CashFlowInformation", "type": "object"}}

Output a valid JSON object but do not repeat the schema.
"""

file_1 = 'data/data_baseline_v7/baseline_v7.csv'
file_2 = 'data/fix_value/merged_value_baseline.csv'

# Load the data
df1 = pd.read_csv(file_1)

df2 = pd.read_csv(file_2)

system_df1 = df1.iloc[100]['system'] 

df1['system'] = BASELINE_SYSTEM_PROMPT
df1 = df1.drop_duplicates(subset=['user'])
# change value in df2 system column to BASELINE_SYSTEM_PROMPT
df2['system'] = BASELINE_SYSTEM_PROMPT
# Remove duplicate rows in df2 based on 'user' column
df2 = df2.drop_duplicates(subset=['user'])


# Create a list to store indices of rows to remove from df1
rows_to_remove = []

# Iterate through rows in df2
for _, row2 in tqdm(df2.iterrows(), total=len(df2)):
    user2 = row2['user']
    
    # Check if any row in df1 contains the user2 string in its 'user' column
    for index1, row1 in df1.iterrows():
        user1 = row1['user']
        if user2 in user1 or user1 in user2:
            rows_to_remove.append(index1)


print(f"Len rows to drop: {len(rows_to_remove)}")
# Remove matching rows from df1
df1 = df1.drop(rows_to_remove)

# Append all rows from df2 to df1
df1 = pd.concat([df1, df2], ignore_index=True)

# Save the updated file_1
df1.to_csv('data/data_baseline_v7/baseline_v7_fix_value.csv', index=False)