# app.py

import streamlit as st
from openai import OpenAI

client = OpenAI()

# 페이지 배경 색상을 설정하는 CSS 스타일
page_bg_color = """
<style>
body {
    background-color: #f0f2f6;
}
</style>
"""


st.title("기자들을 위한 GPT-4o")

article = st.text_area(label_visibility=False,placeholder="여기에 기사를 입력하세요.", height=400)

prompt = f"""
당신은 매우 유능한 기자이자 일러스트레이터입니다.
먼저 다음의 조건을 반드시 지켜주세요.

--- START OF CONDITIONS ---
- 반드시 한국어로 결과물을 생성할 것.
- 이미지는 반드시 하나 이상 생성할 것.
- 작업의 순서를 반드시 지킬 것.
--- END OF CONDITIONS ---

제출한 기사 원문의 내용을 이해하고, 순서에 따라 작업을 진행해주세요.

--- START OF TASK ---
첫 번째, 원문을 가장 잘 표현하는 이미지를 생성해주세요.
두 번째, 원문 전체를 요약해주세요.
세 번째, 키워드 5개를 중요한 순서대로 추출해주세요.
네 번째, 원문의 각 문단별 중제목을 추출해 주세요.
다섯 번째, 원문에서 보완할 점 세 가지를 정리해주세요.
--- END OF TASK ---

--- START OF ARTICLE ---
{article}
--- END OF ARTICLE ---
"""

if st.button("Submit"):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    st.write(completion.choices[0].message.content)
