from typing import Optional, Literal
from llama_index.core.bridge.pydantic import BaseModel, Field


class CashCategory(BaseModel):
    """Only exist ONE field. Field value CAN be null"""
    food: Optional[Literal[
        "Đồ uống", "Ăn sáng", "Ăn trưa", "Ăn tối", "Ăn vặt"]] = Field(
        default=None,
        description="Money used for food"
    )
    commute: Optional[Literal[
        "Xăng xe", "Gửi xe", "Bảo hiểm xe", "Thuê xê", "Sửa chữa xe"
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
        "Tiền truyền hình", "Tiền điện thoại", "Tiền siêu thị"
    ]] = Field(
        default=None,
        description="Money related to living expenses"
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
    household: Optional[Literal[
        "Đồ đạc trong nhà", "Tiền thuê nhà", "Thế chấp nhà",
        "Sửa nhà"
    ]] = Field(
        default=None,
        description="Money related to household"
    )
    treat_money: Optional[Literal[
        "Vui chơi giải trí", "Du lịch", "Phim ảnh ca nhạc",
        "Spa & Massage", "Mỹ phẩm"
    ]] = Field(
        default=None,
        description="Money used to enjoy or reward yourself"
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
        "Chứng khoán", "Vàng", "Tiền số", "Trái phiếu",
        "Nhà đất"
    ]] = Field(
        default=None,
        description="Money used in investment"
    )
