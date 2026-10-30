import re
from schemas import QueryAnalysis, AgentState
from tools import get_order_status, process_refund

def extract_intent_regex(user_query: str) -> QueryAnalysis:
    query_lower = user_query.lower()
    
    # 1. Match Order ID (e.g., ORD-101, ORD-102)
    order_match = re.search(r'ord-\d+', query_lower)
    order_id = order_match.group(0).upper() if order_match else None
    
    # 2. Check for Refund Intent & Amount
    if "refund" in query_lower:
        amount_match = re.search(r'\$?(\d+(\.\d+)?)', user_query)
        refund_amount = float(amount_match.group(1)) if amount_match else None
        return QueryAnalysis(intent="refund_request", order_id=order_id, refund_amount=refund_amount)
    
    # 3. Check for Order Status Intent
    if "status" in query_lower or "where is" in query_lower or "track" in query_lower:
        return QueryAnalysis(intent="order_status", order_id=order_id, refund_amount=None)
        
    return QueryAnalysis(intent="general_query", order_id=None, refund_amount=None)

def process_user_query(user_query: str) -> AgentState:
    analysis = extract_intent_regex(user_query)
    
    state: AgentState = {
        "user_query": user_query,
        "intent": analysis.intent,
        "order_id": analysis.order_id,
        "refund_amount": analysis.refund_amount,
        "status_message": "",
        "requires_approval": False,
        "approved": None
    }

    if analysis.intent == "order_status":
        if analysis.order_id:
            state["status_message"] = get_order_status(analysis.order_id)
        else:
            state["status_message"] = "Could you please provide your Order ID so I can check its status?"

    elif analysis.intent == "refund_request":
        amount = analysis.refund_amount or 0.0
        order_id = analysis.order_id or "N/A"

        if amount > 50.0:
            state["requires_approval"] = True
            state["status_message"] = f"Refund request of ${amount:.2f} for Order {order_id} exceeds auto-approval limit ($50.00). Flagged for manager review."
        else:
            state["status_message"] = process_refund(order_id, amount)

    else:
        state["status_message"] = "Thank you for reaching out! How can I assist you with your orders today?"

    return state