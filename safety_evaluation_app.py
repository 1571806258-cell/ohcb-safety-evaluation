import streamlit as st
import numpy as np
import joblib
import pandas as pd

st.set_page_config(
    page_title="Safety Evaluation System",
    layout="wide"
)

# 设置页面背景颜色和文本颜色
st.markdown(
    """
    <style>
    /* 整个页面的背景颜色 */
    body {
        background-color: #F0F2F6 !important; /* 浅灰蓝色 */
        color: #333333 !important; /* 主要文本颜色 */
    }

    /* Streamlit 应用主体背景 */
    .stApp {
        background-color: #F0F2F6 !important;
    }

    /* 充分利用宽屏空间，并保持页面边距适合截图 */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
        max-width: 100%;
    }

    /* 标题颜色 */
    h1, h2, h3, h4, h5, h6 {
        color: #2C3E50 !important; /* 深蓝色 */
    }

    /* 修改输入框样式 */
    .stTextInput, .stNumberInput, .stSelectbox {
        background-color: #FFFFFF !important;
        border-radius: 10px !important;
        border: 1px solid #B0BEC5 !important;
    }

    div[data-testid="stNumberInput"] {
        margin-bottom: -0.3rem;
    }

    /* 按钮样式 */
    .stButton>button {
        background-color: #2C3E50 !important; /* 深蓝 */
        color: white !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        font-size: 16px !important;
    }

    /* 侧边栏背景颜色 */
    .css-1d391kg {
        background-color: #D3E4CD !important; /* 浅绿色 */
    }

    </style>
    """,
    unsafe_allow_html=True
)

# 载入 SVM 模型和标准化器
model = joblib.load("boiler_safety_svm.pkl")
scaler = joblib.load("scaler.pkl")

# 评价等级
safety_levels = {
    1: "Ⅰ 安全 ✅",
    2: "Ⅱ 预警 ⚠️",
    3: "Ⅲ 危险 ❌"
}

# Streamlit 页面标题
st.title("🔥 有机热载体锅炉安全评价系统 ")

# 定义 31 个指标名称，并按类别分组
安全管理 = [
    "人员持证率/ %",
    "不规范操作情况/ 次/月",
    "日常检查率/ 次/天",
    "有机热载体锅炉清洗频率/ 年",
    "锅炉房安全通道合格率/ %",
    "历史问题整改情况/ %"
]

锅炉结构 = [
    "锅炉上次检验距现在的时间/ 年",
    "工作压力/ Mpa",
    "受压部件局部失效情况/ 次",
    "燃烧（加热）设备参数配置/ %",
    "鼓风机风速/ m/s",
    "管壁积炭层厚度/ mm",
    "循环泵数量/个",
    "循环泵合格率/ %",
    "高位槽与低位槽相对位置高度/ m",
    "高位槽介质温度/ ℃",
    "管路循环流量/ Q",
    "超额热功率/ %",
    "低沸物馏出温度/ ℃",
    "低沸物含量（%）",
    "运动粘度/ mm²/s",
    "酸值/ mg/g",
    "残炭/ %",
    "闪点（闭口）/ ℃",
    "水份/ %",
    "油品选择合理性/ ℃",
    "有害气体浓度/ ppm",
    "安全附件合格率/ 年"
]

环境影响 = [
    "室内通风率/ 次/时",
    "室内温度/ ℃",
    "粉尘浓度/ mg/m³"
]

# 显式固定模型原有的 31 维特征顺序，避免布局调整影响模型输入
ordered_indicator_names = [
    "人员持证率/ %",
    "不规范操作情况/ 次/月",
    "日常检查率/ 次/天",
    "有机热载体锅炉清洗频率/ 年",
    "锅炉房安全通道合格率/ %",
    "历史问题整改情况/ %",
    "锅炉上次检验距现在的时间/ 年",
    "工作压力/ Mpa",
    "受压部件局部失效情况/ 次",
    "燃烧（加热）设备参数配置/ %",
    "鼓风机风速/ m/s",
    "管壁积炭层厚度/ mm",
    "循环泵数量/个",
    "循环泵合格率/ %",
    "高位槽与低位槽相对位置高度/ m",
    "高位槽介质温度/ ℃",
    "管路循环流量/ Q",
    "超额热功率/ %",
    "低沸物馏出温度/ ℃",
    "低沸物含量（%）",
    "运动粘度/ mm²/s",
    "酸值/ mg/g",
    "残炭/ %",
    "闪点（闭口）/ ℃",
    "水份/ %",
    "油品选择合理性/ ℃",
    "有害气体浓度/ ppm",
    "安全附件合格率/ 年",
    "室内通风率/ 次/时",
    "室内温度/ ℃",
    "粉尘浓度/ mg/m³"
]

# 使用字典存储指标值
指标值 = {}

# 创建 3 个一级分类列，锅炉结构列使用更宽的空间
main1, main2, main3 = st.columns([1, 2.2, 1])

with main1:
    st.subheader("🔒 安全管理")
    for name in 安全管理:
        指标值[name] = st.number_input(name, min_value=0.0, value=0.0)

with main2:
    st.subheader("🔧 锅炉结构")
    bcol1, bcol2 = st.columns(2)

    with bcol1:
        for name in 锅炉结构[:11]:
            指标值[name] = st.number_input(name, min_value=0.0, value=0.0)

    with bcol2:
        for name in 锅炉结构[11:]:
            指标值[name] = st.number_input(name, min_value=0.0, value=0.0)

with main3:
    st.subheader("🌍 环境影响")
    for name in 环境影响:
        指标值[name] = st.number_input(name, min_value=0.0, value=0.0)

# 上传文件进行批量评估
uploaded_file = st.file_uploader("📂 上传 Excel 数据文件（如 need data.xlsx）", type=["xlsx"])

# 评估按钮
if st.button("🚀 评估"):
    # 单个输入处理
    X_input = np.array(
        [指标值[name] for name in ordered_indicator_names]
    ).reshape(1, -1)
    X_scaled = scaler.transform(X_input)  # 归一化
    prediction = model.predict(X_scaled)[0]  # 预测

    # 显示评估结果
    st.markdown(f"### 🔍 **评估结果：{safety_levels[prediction]}**")

# 批量评估
if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # 确保数据列数匹配
    if df.shape[1] != 31:
        st.error("❌ 数据列数与 31 个指标不匹配，请检查上传文件格式！")
    else:
        X_batch = df.values
        X_batch_scaled = scaler.transform(X_batch)
        predictions = model.predict(X_batch_scaled)

        df["评估结果"] = [safety_levels[p] for p in predictions]
        st.write("📊 **批量评估结果**")
        st.dataframe(df)
