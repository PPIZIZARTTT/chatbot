import os
import streamlit as st
from openai import OpenAI
import PyPDF2

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="เเชทบอท นมรตอพ",
    page_icon="💬",
    layout="centered"
)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Set up the title and description
st.title("เเชทบอท น.ม.รตอพ")
st.markdown("สวัสดีครับผมเป็นเเชทบอทของโรงเรียนอยากให้ช่วยอะไรไหมครับ")

# Define your PDF file path
# Update this path to the correct location in your deployed environment
file_path = r'files/context.pdf'  # This should be the relative path where your PDF will be stored

# Read the PDF
@st.cache_data  # This caches the result so it's only loaded once
def read_pdf(file_path):
    text = ''
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""

# Load context once at startup
context = read_pdf(file_path)
if context:
    st.success("")
else: 
    st.error("ขออภัยตอนนี้ผมยังไม่สามารถเข้าถึงข้อมูลได้ กรุณาเเจ้งด.ช.กิตติภพ ว่องไวให้มาซ้อมด่วนๆ")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    # Ensure context has been loaded
    if not context:
        st.error("Document failed to load. Cannot process queries.")
    else:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get and display assistant response
        with st.chat_message("assistant"):
            try:
                with st.spinner("Thinking..."):
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": context},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    
                    bot_reply = response.choices[0].message.content
                    st.markdown(bot_reply)
                    
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                
            except Exception as e:
                st.error(f"An error occurred: {e}")