import streamlit as st
import os
import json
import datetime
import base64
from llm_providers import get_provider, list_providers
from utils.privacy import is_private_mode, check_password
from llm_providers.ollama_api import OllamaProvider
from llm_providers.openai_api import OpenAIProvider

# 确保sessions文件夹存在
os.makedirs("sessions", exist_ok=True)

def save_session_messages(session_name, messages):
    """保存会话消息到JSON文件，包括图片等多媒体内容"""
    session_file = os.path.join("sessions", f"{session_name}.json")
    # 处理图片等二进制内容
    processed_messages = []
    for msg in messages:
        processed_msg = msg.copy()
        if msg.get("filetype") == "image" and msg.get("file") is not None:
            # 将图片转换为base64
            file_bytes = msg["file"].getvalue()
            base64_image = base64.b64encode(file_bytes).decode()
            processed_msg["file"] = base64_image
        processed_messages.append(processed_msg)
    
    with open(session_file, "w", encoding="utf-8") as f:
        json.dump(processed_messages, f, ensure_ascii=False, indent=2)

def load_session_messages(session_name):
    """从JSON文件加载会话消息，包括图片等多媒体内容"""
    session_file = os.path.join("sessions", f"{session_name}.json")
    if os.path.exists(session_file):
        with open(session_file, "r", encoding="utf-8") as f:
            messages = json.load(f)
            # 处理base64图片
            for msg in messages:
                if msg.get("filetype") == "image" and msg.get("file") is not None:
                    # 将base64转换回图片
                    import io
                    from PIL import Image
                    image_bytes = base64.b64decode(msg["file"])
                    image = Image.open(io.BytesIO(image_bytes))
                    msg["file"] = image
            return messages
    return []

# 设置页面
st.set_page_config(page_title="多功能 LLM 聊天", page_icon="🤖", layout="wide")

if not check_password():
    st.stop()    

# 初始化会话状态
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "history" not in st.session_state:
    st.session_state["history"] = []
if "current_session" not in st.session_state:
    st.session_state["current_session"] = None
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

# 主题设置
if "theme" not in st.session_state:
    st.session_state["theme"] = "light"

# 侧边栏设置
with st.sidebar:
    st.header("设置")
    provider_name = st.selectbox("选择模型API", list_providers(), help="选择要使用的语言模型API提供商")
    
    st.toggle("隐私模式", key="private_mode", help="开启后不保存聊天记录")
    if st.session_state.private_mode != st.session_state.get("previous_private_mode", False):
        # 隐私模式状态改变时创建新会话
        new_session = f"session_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        st.session_state["sessions"][new_session] = []
        if is_private_mode():
            st.session_state["current_session"] = new_session
            st.session_state["messages"] = [
                {"role": "assistant", "content": f"👋 隐私模式已开启，聊天记录不会被保存：{new_session}"}
            ]
        else:
            st.session_state["current_session"] = None
            st.session_state["messages"] = [
                {"role": "assistant", "content": "👋 隐私模式已关闭，聊天记录将被保存。请创建新会话。"}
            ]
        st.session_state["previous_private_mode"] = st.session_state.private_mode
    
    openai_model = None
    ollama_model = None
    if provider_name == "OpenAI":
        openai_models = OpenAIProvider.get_available_models()
        openai_model = st.selectbox("OpenAI模型", openai_models, key="openai_model")
        # 检查是否为 o 系列模型
        is_o_series = openai_model is not None and openai_model.lower().startswith("o")
        if is_o_series:
            web_search_enabled = False
            st.toggle(f"联网搜索 ({openai_model} 不支持)", key="web_search", value=False, disabled=True, help=f"开启后模型可以搜索实时信息，但 {openai_model} 不支持联网搜索")
        else:
            web_search_enabled = st.toggle("联网搜索", key="web_search", value=True, help="开启后模型可以搜索实时信息")
    else:
        if provider_name == "Ollama":
            ollama_models = OllamaProvider.get_available_models()
            ollama_model = st.selectbox("Ollama模型", ollama_models, key="ollama_model")
        web_search_enabled = st.toggle("联网搜索", key="web_search", value=True, help="开启后模型可以搜索实时信息")
    search_context_size = st.selectbox("搜索上下文大小", ["low", "medium", "high"], index=1, help="控制搜索返回信息的详细程度")
    st.session_state["theme"] = st.selectbox("主题模式", ["light", "dark"], index=0 if st.session_state["theme"]=="light" else 1)
    st.markdown("---")

    # 会话管理
    st.header("会话管理")
    if "sessions" not in st.session_state:
        st.session_state["sessions"] = {}
    
    # 加载现有会话
    session_files = []
    if os.path.exists("sessions"):
        session_files = [f.replace(".json", "") for f in os.listdir("sessions") if f.endswith(".json")]
    
    # 初始化当前会话
    if st.session_state.get("current_session") is None:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "👋 欢迎！请点击下方按钮创建新会话。"}
        ]

    # 创建新会话（自动命名）
    if st.button("创建新会话"):
        new_session = f"session_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        st.session_state["sessions"][new_session] = []
        st.session_state["current_session"] = new_session
        # 初始化新会话
        st.session_state["messages"] = [
            {"role": "assistant", "content": f"👋 欢迎使用新会话：{new_session}！"}
        ]
        if not is_private_mode():
            save_session_messages(new_session, st.session_state["messages"])
        st.success(f"已创建会话：{new_session}")
        st.rerun()

    # 切换会话
    if session_files:  # 只在有会话时显示选择框
        session_name = st.selectbox("选择会话", session_files, index=session_files.index(st.session_state["current_session"]) if st.session_state["current_session"] in session_files else 0)
        if session_name != st.session_state["current_session"]:
            st.session_state["current_session"] = session_name
            if not is_private_mode():
                st.session_state["messages"] = load_session_messages(session_name)
            st.rerun()

    # 删除会话
    if st.button("删除当前会话"):
        if st.session_state["current_session"] in st.session_state["sessions"]:
            del st.session_state["sessions"][st.session_state["current_session"]]
        session_file = os.path.join("sessions", f"{st.session_state['current_session']}.json")
        if os.path.exists(session_file):
            os.remove(session_file)
        # 删除后等待用户创建新会话
        st.session_state["current_session"] = None
        st.session_state["messages"] = [
            {"role": "assistant", "content": "👋 会话已删除。请点击下方按钮创建新会话。"}
        ]
        st.success("已删除会话")
        st.rerun()
    st.markdown("---")

provider = None
if provider_name == "OpenAI":
    provider = get_provider(provider_name, model=openai_model, web_search=web_search_enabled, search_context_size=search_context_size)
elif provider_name == "Ollama":
    provider = get_provider(provider_name, model=ollama_model)
else:
    provider = get_provider(provider_name)
    
# 聊天UI
for msg in st.session_state["messages"]:
    avatar = "🧑" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        # Markdown渲染，支持代码高亮
        st.markdown(msg["content"], unsafe_allow_html=True)
        # 图片消息支持
        if msg.get("filetype") == "image":
            st.image(msg["file"])

# 文件上传（支持图片）
uploaded_file = st.file_uploader("上传图片/文件（图片将直接显示）", type=["png", "jpg", "jpeg", "gif"], key=f"uploader_{st.session_state.uploader_key}")

if uploaded_file is not None:
    # 检查是否已有会话
    if not st.session_state.get("current_session"):
        st.warning("请先创建新会话")
    else:
        # 读取图片数据并添加到消息
        st.session_state["messages"].append({
            "role": "user",
            "content": f"上传了图片：{uploaded_file.name}",
            "file": uploaded_file,
            "filetype": "image"
        })
        # 仅在非隐私模式下保存会话
        if not is_private_mode():
            save_session_messages(st.session_state["current_session"], st.session_state["messages"])
        # 刷新页面以立即显示图片
        st.session_state.uploader_key += 1
        st.rerun()

# 输入
prompt = st.chat_input("请输入内容...")
if prompt:
    if st.session_state["current_session"] is None:
        st.warning("请先创建新会话")
    else:
        st.session_state["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑"):
            st.markdown(prompt, unsafe_allow_html=True)
        with st.chat_message("assistant", avatar="🤖"):
            response_stream = provider.stream_chat(prompt, st.session_state["messages"])
            full_response = ""
            response_box = st.empty()
            for chunk in response_stream:
                full_response += chunk
                response_box.markdown(full_response, unsafe_allow_html=True)
            st.session_state["messages"].append({"role": "assistant", "content": full_response})
        # 仅在非隐私模式下保存会话
        if not is_private_mode():
            save_session_messages(st.session_state["current_session"], st.session_state["messages"])

# 主题切换
if st.session_state["theme"] == "dark":
    st.markdown("""
        <style>
        body, .stApp { background-color: #222 !important; color: #eee !important; }
        .stChatMessage { background: #333 !important; }
        </style>
    """, unsafe_allow_html=True)