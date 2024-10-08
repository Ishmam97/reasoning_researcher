css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #f7dc6f 
}
.chat-message.bot {
    background-color: #82e0aa 
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://llamaimodel.com/wp-content/uploads/2024/04/Llama-AI-3.webp"> 
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

import base64

with open("/Users/aatif/Downloads/IMG_6471.JPG", "rb") as img_file:
    img_base64 = base64.b64encode(img_file.read()).decode('utf-8')

user_template = f'''
<div class="chat-message user">
    <div class="avatar">
        <img src="data:image/jpeg;base64,{img_base64}">
    </div>    
    <div class="message">{{{{MSG}}}}</div>
</div>
'''

