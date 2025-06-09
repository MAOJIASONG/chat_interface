import streamlit as st
import hmac  
import time

def is_private_mode():
    return st.session_state.get("private_mode", False) 


def check_password(): 
    def login_form(): 
        with st.form("Credentials"):  
            col0,col1, col2 = st.columns([0.6,0.4, 2],vertical_alignment="top")  
            with col0:  
                st.write("  ")  
            with col1:  
                # st.image("./utils/logo.png",  width=75)  
                st.text("💬")
            with col2:  
                st.markdown("## Login")  
            st.text_input("账号名称", key="username")  
            st.text_input("账号密码", type="password", key="password")  
            # 将按钮靠右放置  
            cols = st.columns([4, 1])  
            cols[1].form_submit_button("登录", on_click=password_entered)  
            # st.form_submit_button("登录", on_click=password_entered)   
    def password_entered():  
        """Checks whether a password entered by the user is correct."""  
        if st.session_state["username"] in st.secrets[  
            "passwords"  
        ] and hmac.compare_digest(  
            st.session_state["password"],  
            st.secrets.passwords[st.session_state["username"]],  
        ):  
            st.session_state["password_correct"] = True  
            del st.session_state["password"]  
            del st.session_state["username"]
            message_placeholder = st.empty()
            message_placeholder.success("登录成功！", icon="✅") 
            time.sleep(1)
            message_placeholder.empty()
        else:  
            st.session_state["password_correct"] = False
            st.error("😕 账号不存在或者密码不正确")

    # Show inputs for username + password. 
    if not st.session_state.get("password_correct", False):
        login_form()  
        if st.session_state.get("password_correct", False):  
            return True
        else: 
            return False
    else:   
        return True
    