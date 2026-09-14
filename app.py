import streamlit as st
import anthropic

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.markdown("""
<style>
.main {
    background-color: #f7f7f8;
}
.chat-title {
    text-align: center;
    font-size: 35px;
    font-weight: 700;
    margin-bottom: 5px;
}
.chat-subtitle {
    text-align: center;
    color: #666;
    margin-bottom: 30px;
}
footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="chat-title">🤖 AI Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="chat-subtitle">Powered by Claude AI</div>', unsafe_allow_html=True)

with st.sidebar:
    st.title("🤖 AI Assistant")
    st.write("Welcome to your AI chatbot!")
    st.divider()
    st.write("### Features")
    st.write("💬 AI Conversation")
    st.write("🧠 Intelligent Answers")
    st.write("⚡ Fast Responses")
    st.write("📱 Mobile Friendly")
    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
except Exception:
    st.error(
        "Anthropic API key is not configured. "
        "Please add ANTHROPIC_API_KEY to Streamlit Secrets."
    )
    st.stop()

client = anthropic.Anthropic(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Ask me anything...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.messages.create(
                    model="claude-sonnet-5",
                    max_tokens=1024,
                    system="""You are a helpful and friendly AI assistant.

Give clear and accurate answers.
Explain technical topics in simple language.

Help students with:
- Python
- Java
- SQL
- Databases
- Artificial Intelligence
- Machine Learning
- Projects
- Programming
- General questions

Keep answers well structured and easy to understand.""",
                    messages=st.session_state.messages
                )

                assistant_response = ""

                for block in response.content:
                    if block.type == "text":
                        assistant_response += block.text

                st.markdown(assistant_response)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_response
                })

            except Exception as e:
                st.error(f"Sorry, something went wrong: {str(e)}")
