import streamlit as st
import time
import datetime
import random

# --- 1. 初始化数据存储 ---
# 使用 Streamlit 的 session_state 来存储心跳历史，确保在页面刷新时数据不会丢失
if 'heartbeat_history' not in st.session_state:
    st.session_state.heartbeat_history = []
if 'last_heartbeat_time' not in st.session_state:
    st.session_state.last_heartbeat_time = time.time() # 初始化为当前时间
if 'current_sequence' not in st.session_state:
    st.session_state.current_sequence = 0

# --- 2. 定义模拟心跳的函数 ---
def simulate_heartbeat():
    current_time = time.time()
    current_sequence = st.session_state.current_sequence
    last_heartbeat_time = st.session_state.last_heartbeat_time

    # 检查是否超时 (3秒内未收到心跳)
    if current_time - last_heartbeat_time > 3:
        timeout_entry = {
            "序号": "N/A",
            "时间": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "状态": "超时",
            "详情": f"超过3秒未收到心跳 (上次收到于 {datetime.datetime.fromtimestamp(last_heartbeat_time).strftime('%H:%M:%S')})"
        }
        st.session_state.heartbeat_history.append(timeout_entry)
        # 超时后，将上次心跳时间更新为当前时间，以防止连续报超时
        st.session_state.last_heartbeat_time = current_time
    else:
        # 模拟心跳数据
        # 为了演示超时功能，我们随机让心跳丢失或延迟
        # 80%的概率成功，20%的概率丢失
        if random.random() < 0.8:
            heartbeat_entry = {
                "序号": current_sequence,
                "时间": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "状态": "正常",
                "详情": "心跳正常接收"
            }
            st.session_state.heartbeat_history.append(heartbeat_entry)
            st.session_state.last_heartbeat_time = current_time # 更新最后心跳时间
            st.session_state.current_sequence += 1
        else:
            # 模拟心跳丢失
            lost_entry = {
                "序号": current_sequence,
                "时间": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "状态": "丢失",
                "详情": "模拟心跳丢失"
            }
            st.session_state.heartbeat_history.append(lost_entry)
            # 心跳丢失，不更新 last_heartbeat_time，以便触发超时

# --- 3. 构建 Streamlit 应用界面 ---
st.title("无人心跳自收发模拟器")
st.markdown("这是一个模拟心跳数据的Streamlit应用，每秒更新一次。")

# 使用 st.empty() 创建一个占位符，用于动态更新表格
placeholder = st.empty()

# 使用一个无限循环来模拟持续的心跳
# 注意：在Streamlit中，循环会阻塞UI，但因为有 time.sleep(1)，
# UI仍然可以响应，但主要逻辑是同步的。
while True:
    simulate_heartbeat()
    
    # 将历史数据列表反转，以便最新数据在最上面显示
    display_data = st.session_state.heartbeat_history[::-1]
    
    # 使用占位符更新显示的表格
    placeholder.dataframe(display_data, height=400) # 设置高度，方便滚动

    # 每秒执行一次
    time.sleep(1)
