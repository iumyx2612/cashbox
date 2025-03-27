from typing import Optional, Literal
from llama_index.core.bridge.pydantic import BaseModel, Field


class CashCategory(BaseModel):
    """Only exist ONE field. Field value CAN be null"""
    food: Optional[Literal[
        "Đồ uống", "Ăn sáng", "Ăn trưa", "Ăn tối", "Ăn vặt"
    ]] = Field(
        default=None,
        description="Money used for food"
    )
    commute: Optional[Literal[
        "Xăng xe", "Gửi xe", "Bảo hiểm xe", "Thuê xe", "Sửa chữa xe", "Thuế phí"
    ]] = Field(
        default=None,
        description="Money related to commute"
    )
    health_care: Optional[Literal[
        "Khám chữa bệnh", "Thuốc men", "Thể thao", "Bảo hiểm y tế"
    ]] = Field(
        default=None,
        description="Money related to health care"
    )
    living_expense: Optional[Literal[
        "Tiền điện", "Tiền nước", "Tiền internet", "Tiền gas",
        "Tiền truyền hình", "Tiền điện thoại"
    ]] = Field(
        default=None,
        description="Money related to living expenses"
    )
    shopping: Optional[Literal[
        "Tiền siêu thị", "Tiền đi chợ"
    ]] = Field(
        default=None,
        description="Money related to shopping"
    )
    child_care: Optional[Literal[
        "Học phí", "Trông trẻ", "Tiền sữa",
        "Tiền bỉm", "Tiền đồ chơi", "Tiền tiêu vặt"
    ]] = Field(
        default=None,
        description="Money related to child care"
    )
    clothing: Optional[Literal[
        "Quần áo", "Giầy dép", "Phụ kiện khác"
    ]] = Field(
        default=None,
        description="Money related to clothing or body accessories"
    )
    gifts_donations: Optional[Literal[
        "Thăm hỏi", "Biếu tặng"
    ]] = Field(
        default=None,
        description="Money used for gifts or donations"
    )
    household: Optional[Literal[
        "Đồ đạc trong nhà", "Tiền thuê nhà", "Sửa nhà"
    ]] = Field(
        default=None,
        description="Money related to household"
    )
    treat_money: Optional[Literal[
        "Vui chơi giải trí", "Du lịch", "Phim ảnh ca nhạc",
        "Spa & Massage", "Mỹ phẩm", "Nhậu nhẹt"
    ]] = Field(
        default=None,
        description="Money used to enjoy or reward yourself"
    )
    pets: Optional[Literal[
        "Chó", "Mèo"
    ]] = Field(
        default=None,
        description="Money invest in your pets"
    )
    self_growth: Optional[Literal[
        "Học hành", "Xây dựng mối quan hệ"
    ]] = Field(
        default=None,
        description="Money invest in yourself for self improvement"
    )
    bank: Optional[Literal[
        "Phí chuyển khoản", "Trả lãi vay", "Trả nợ ngân hàng"
    ]] = Field(
        default=None,
        description="Money related to bank"
    )
    invest: Optional[Literal[
        "Chứng khoán", "Vàng", "Tiền số", "Nhà đất"
    ]] = Field(
        default=None,
        description="Money used in investment"
    )
    saving: Optional[Literal[
        "Gửi tiền tiết kiệm", "Cho vay"
    ]] = Field(
        default=None,
        description="Money used for saving or lending"
    )
    income: Optional[Literal[
        "Lương", "Thưởng", "Thu hồi nợ", "Kinh doanh", "Trợ cấp", "Rút tiết kiệm", "Bán tài sản"
    ]] = Field(
        default=None,
        description="Money used for income"
    )