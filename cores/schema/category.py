from typing import Optional, Literal, Union
from llama_index.core.bridge.pydantic import BaseModel, Field
from pydantic import field_validator


class CashCategory(BaseModel):
    """Only exist ONE field. Field value CAN be null"""
    food: Optional[Union[Literal[
        "Đồ uống", "Ăn sáng", "Ăn trưa", "Ăn tối", "Ăn vặt"
    ], str]] = Field(
        default=None,
        description="Money used for food"
    )
    commute: Optional[Union[Literal[
        "Xăng xe", "Gửi xe", "Bảo hiểm xe", "Thuê xe", "Sửa chữa xe", "Thuế phí"
    ], str]] = Field(
        default=None,
        description="Money related to commute"
    )
    health_care: Optional[Union[Literal[
        "Khám chữa bệnh", "Thuốc men", "Thể thao", "Bảo hiểm y tế"
    ], str]] = Field(
        default=None,
        description="Money related to health care"
    )
    living_expense: Optional[Union[Literal[
        "Tiền điện", "Tiền nước", "Tiền internet", "Tiền gas",
        "Tiền truyền hình", "Tiền điện thoại"
    ], str]] = Field(
        default=None,
        description="Money related to living expenses"
    )
    shopping: Optional[Union[Literal[
        "Tiền siêu thị", "Tiền đi chợ"
    ], str]] = Field(
        default=None,
        description="Money related to shopping"
    )
    child_care: Optional[Union[Literal[
        "Học phí", "Trông trẻ", "Tiền sữa",
        "Tiền bỉm", "Tiền đồ chơi", "Tiền tiêu vặt"
    ], str]] = Field(
        default=None,
        description="Money related to child care"
    )
    clothing: Optional[Union[Literal[
        "Quần áo", "Giầy dép", "Phụ kiện khác"
    ], str]] = Field(
        default=None,
        description="Money related to clothing or body accessories"
    )
    gifts_donations: Optional[Union[Literal[
        "Thăm hỏi", "Biếu tặng"
    ], str]] = Field(
        default=None,
        description="Money used for gifts or donations"
    )
    household: Optional[Union[Literal[
        "Đồ đạc trong nhà", "Tiền thuê nhà", "Sửa nhà"
    ], str]] = Field(
        default=None,
        description="Money related to household"
    )
    treat_money: Optional[Union[Literal[
        "Vui chơi giải trí", "Du lịch", "Phim ảnh ca nhạc",
        "Spa & Massage", "Mỹ phẩm", "Nhậu nhẹt"
    ], str]] = Field(
        default=None,
        description="Money used to enjoy or reward yourself"
    )
    pets: Optional[Union[Literal[
        "Chó", "Mèo"
    ], str]] = Field(
        default=None,
        description="Money invest in your pets"
    )
    self_growth: Optional[Union[Literal[
        "Học hành", "Xây dựng mối quan hệ"
    ], str]] = Field(
        default=None,
        description="Money invest in yourself for self improvement"
    )
    bank: Optional[Union[Literal[
        "Phí chuyển khoản", "Trả lãi vay", "Trả nợ ngân hàng"
    ], str]] = Field(
        default=None,
        description="Money related to bank"
    )
    invest: Optional[Union[Literal[
        "Chứng khoán", "Vàng", "Tiền số", "Nhà đất"
    ], str]] = Field(
        default=None,
        description="Money used in investment"
    )
    saving: Optional[Union[Literal[
        "Gửi tiền tiết kiệm", "Cho vay"
    ], str]] = Field(
        default=None,
        description="Money used for saving or lending"
    )
    income: Optional[Union[Literal[
        "Lương", "Thưởng", "Thu hồi nợ", "Kinh doanh", "Trợ cấp", "Rút tiết kiệm", "Bán tài sản"
    ], str]] = Field(
        default=None,
        description="Money used for income"
    )

    @field_validator('*', mode='before')
    @classmethod
    def validate_category(cls, v, info):
        if v is None:
            return None
        
        field_name = info.field_name
        if field_name in ['food', 'commute', 'health_care', 'living_expense', 'shopping', 
                         'child_care', 'clothing', 'gifts_donations', 'household', 
                         'treat_money', 'pets', 'self_growth', 'bank', 'invest', 
                         'saving', 'income']:
            # Get the field's type annotation from the model
            field_type = cls.model_fields[field_name].annotation
            if hasattr(field_type, '__args__'):
                # Get the Literal type from Union
                literal_type = field_type.__args__[0]
                if hasattr(literal_type, '__args__'):
                    allowed_values = literal_type.__args__
                    if v not in allowed_values:
                        return field_name
        return v