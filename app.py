import streamlit as st
from agent import process_user_query
from tools import process_refund

st.set_page_config(page_title="AI Agent Support System", layout="wide")
st.title("🤖 Customer Support Agent with HITL Safety Rules")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_state" not in st.session_state:
    st.session_state.last_state = None

col1, col2 = st.columns([2, 1])

# Left Panel: Customer Chat
with col1:
    st.subheader("Customer Chat Window")
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    user_input = st.chat_input("Type your request (e.g., 'Check status of ORD-101' or 'I want a $120 refund for ORD-102')...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Process through agent
        state = process_user_query(user_input)
        st.session_state.last_state = state
        
        st.session_state.messages.append({"role": "assistant", "content": state["status_message"]})
        st.rerun()

# Right Panel: Agent Internal State & Manager HITL
with col2:
    st.subheader("⚙️ Agent State Inspector")
    state = st.session_state.last_state
    
    if state:
        st.json({
            "Intent": state["intent"],
            "Extracted Order ID": state["order_id"],
            "Extracted Refund Amount": state["refund_amount"],
            "Requires Manager Approval": state["requires_approval"]
        })
        
        if state["requires_approval"]:
            st.warning(f"⚠️ Approval Pending: ${state['refund_amount']} Refund")
            col_a, col_b = st.columns(2)
            
            if col_a.button("✅ Approve Refund"):
                res = process_refund(state["order_id"] or "N/A", state["refund_amount"] or 0.0)
                st.session_state.messages.append({"role": "assistant", "content": f"[MANAGER APPROVED]: {res}"})
                st.session_state.last_state["requires_approval"] = False
                st.rerun()
                
            if col_b.button("❌ Reject Refund"):
                st.session_state.messages.append({"role": "assistant", "content": "[MANAGER REJECTED]: Refund request was denied per policy limits."})
                st.session_state.last_state["requires_approval"] = False
                st.rerun()
    else:
        st.info("Agent execution state logs will appear here live when you send a message.")