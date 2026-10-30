from pydantic import BaseModel, Field
from typing import Optional, TypedDict

class QueryAnalysis(BaseModel):
    intent: str = Field(description="Intent of the user query, e.g., 'order_status', 'refund_request', or 'general'")
    order_id: Optional[str] = Field(default=None, description="The order ID if mentioned, e.g., '12345'")
    refund_amount: Optional[float] = Field(default=None, description="The refund amount requested if applicable")

class AgentState(TypedDict):
    user_query: str
    intent: str
    order_id: Optional[str]
    refund_amount: Optional[float]
    status_message: str
    requires_approval: bool
    approved: Optional[bool]