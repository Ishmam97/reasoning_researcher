import streamlit as st
import PyPDF2

# Set page layout to wide for better display
# st.set_page_config(layout="wide")

# ----------------------------------------------------------------------

# Set the title of the app
st.write("## Upload a PDF")

# Add a file uploader to upload PDF files
uploaded_pdf = st.file_uploader("Choose a PDF file", type="pdf")

# Function to extract text from the PDF
def extract_text_from_pdf(pdf_file):
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    # Loop through all the pages and extract text
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

# Check if a file is uploaded
if uploaded_pdf is not None:
    # Display the file name
    st.write(f"Uploaded file: {uploaded_pdf.name}")
    
    # Extract and display PDF text
    st.subheader("Extracted Text from PDF:")
    pdf_text = extract_text_from_pdf(uploaded_pdf)
    st.text_area("PDF Content", pdf_text, height=300)


# ----------------------------------------------------------------------


# Initialize the session state to keep track of messages
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Function to simulate backend processing (replace with actual backend logic)
def send_to_backend(user_message):
    # Here we simply reverse the user's message for demo purposes
    return f"Backend Response: {user_message[::-1]}"


# style for text input 
st.markdown("""
            <style>
            .input_placeholder::placeholder {
                background-color: #C2CFDB;
                opacity: 1;
            }
            </style>
            """, unsafe_allow_html=True)


# Input area for the user to type their message
with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_area("Input your prompt:", placeholder="your prompt...", height=150, key="user_input")
    submit_button = st.form_submit_button(label='Submit')

# If the user submits the form
if submit_button and user_input:
    # Send the user's message to the backend
    bot_response = send_to_backend(user_input)
    
    # Save the conversation in session state
    st.session_state['messages'].append(("You", user_input))
    st.session_state['messages'].append(("Bot", bot_response))


# ---------------------------------------------------------------------------------------
# Response

st.markdown("""
    <style>
    .scrollable-markdown {
        height: 300px;
        overflow-y: scroll;
        border: 1px solid #ddd;
        padding: 10px;
        border-radius: 5px;
        background-color: #f9f9f9;
    }
    </style>
    """, unsafe_allow_html=True)

for sender, message in st.session_state['messages']:
    # Process the input into markdown format
    # processed_text = process_input_to_markdown(user_input)
    
    # Display the processed markdown in an output text area
    st.markdown('<div class="scrollable-markdown">', unsafe_allow_html=True)
    if sender == 'You':
        st.markdown(f"<div style='background-color:")
    st.markdown('<div class="scrollable-markdown">', unsafe_allow_html=True)
    st.subheader("Output (Markdown):")
    if sender == 'Bot':
        st.markdown(f"<div style='background-color:")


# ---------------------------------------------------------------------------------------

# Display chat history -------------------------------------------------------------------
# st.write("## Chat History")

# st.markdown("""
#     <style>
#     .scrollable-markdown {
#         height: 300px;
#         overflow-y: scroll;
#         border: 1px solid #ddd;
#         padding: 10px;
#         border-radius: 5px;
#         background-color: #f9f9f9;
#     }
#     </style>
#     """, unsafe_allow_html=True)

# st.markdown('<div class="scrollable-markdown">', unsafe_allow_html=True)

# for sender, message in st.session_state['messages']:
#    st.markdown(message)
    


# ----------------------------------------------------------------------






# ----------------------------------------------------------------------



st.markdown(
    """
    <style>
    .flex-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px;
        background-color: #f0f0f0;
        border-radius: 10px;
        margin-bottom: 20px;
    }

    .box {
        background-color: #fff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        text-align: center;
        width: 30%;
        border: 3px solid #4e4e4e;
    }

    .flex-row {
        display: flex;
        flex-direction: row;
        gap: 10px;
        justify-content: center;
    }

    .flex-column {
        display: flex;
        flex-direction: column;
        gap: 10px;
        align-items: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# with st.container():

#     col1, col2, col3 = st.columns(3)

#     with col1:
#         st.markdown('<div class="box">Box 1</div>', unsafe_allow_html=True)
#     with col2:
#         st.markdown('<div class="box">Box 2</div>', unsafe_allow_html=True)
#     with col3: 
#         st.markdown('<div class="box">Box 3</div>', unsafe_allow_html=True)

#     col1, col2 = st.columns([2, 1])

#     with col1:
#         st.markdown('<div class="box">Box 1</div>', unsafe_allow_html=True)
#     with col2:
#         st.markdown('<div class="box">Box 2</div>', unsafe_allow_html=True)

#-----------------------------------------------------------------------------------------

# st.markdown('<div class="flex-container">', unsafe_allow_html=True)

# # Add three boxes inside the flex container
# st.markdown('<div class="box">Box 1: Flexbox Layout</div>', unsafe_allow_html=True)
# st.markdown('<div class="box">Box 2: Flexbox Layout</div>', unsafe_allow_html=True)
# st.markdown('<div class="box">Box 3: Flexbox Layout</div>', unsafe_allow_html=True)

# st.markdown('</div>', unsafe_allow_html=True)

# # Another example of a row flex layout
# st.markdown('<div class="flex-row">', unsafe_allow_html=True)
# st.markdown('<div class="box">Item 1</div>', unsafe_allow_html=True)
# st.markdown('<div class="box">Item 2</div>', unsafe_allow_html=True)
# st.markdown('</div>', unsafe_allow_html=True)

# # Column flex example
# st.markdown('<div class="flex-column">', unsafe_allow_html=True)
# st.markdown('<div class="box">Column Item 1</div>', unsafe_allow_html=True)
# st.markdown('<div class="box">Column Item 2</div>', unsafe_allow_html=True)
# st.markdown('</div>', unsafe_allow_html=True)