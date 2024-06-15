# app.py

import streamlit as st
from openai import OpenAI
from streamlit_option_menu import option_menu
import ast


def get_sequence_label(count):
    labels = ["첫 번째", "두 번째", "세 번째", "네 번째", "다섯 번째", "다음"]
    return labels[count - 1] if count <= len(labels) else "다음"


client = OpenAI()

st.markdown(
    """
    <style>
    @import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable.min.css");
    body {
        font-family: 'Pretendard Variable', sans-serif !important;
    }
    p, h1, h2, h3, h4, h5, div, span {
        font-family: 'Pretendard Variable', sans-serif !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <style>
    .toast-container {
        visibility: hidden;
        min-width: 250px;
        margin-left: -125px;
        background-color: #333;
        color: #fff;
        text-align: center;
        border-radius: 2px;
        padding: 16px;
        position: fixed;
        z-index: 1;
        left: 50%;
        bottom: 30px;
        font-size: 17px;
    }
    .show {
        visibility: visible;
        -webkit-animation: fadein 0.5s, fadeout 0.5s 2.5s;
        animation: fadein 0.5s, fadeout 0.5s 2.5s;
    }
    @-webkit-keyframes fadein {
        from {bottom: 0; opacity: 0;}
        to {bottom: 30px; opacity: 1;}
    }
    @keyframes fadein {
        from {bottom: 0; opacity: 0;}
        to {bottom: 30px; opacity: 1;}
    }
    @-webkit-keyframes fadeout {
        from {bottom: 30px; opacity: 1;}
        to {bottom: 0; opacity: 0;}
    }
    @keyframes fadeout {
        from {bottom: 30px; opacity: 1;}
        to {bottom: 0; opacity: 0;}
    }
    </style>
    <script>
    function showToast(message) {
        var toast = document.getElementById("toast");
        toast.className = "show";
        toast.innerHTML = message;
        setTimeout(function(){ toast.className = toast.className.replace("show", ""); }, 3000);
    }
    </script>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div id="toast" class="toast-container">
        This is a toast message!
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <style>
    .nav-pills .nav-link.active {
        background-color: #0F4B39 !important;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

selected = option_menu(
    menu_title=None,
    options=["Home", "Chat", "About"],
    icons=["house", "chat", "info-circle"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "20px", "display": "none"},
        "nav-link": {
            "font-size": "16px",
            "text-align": "center",
            "margin": "0px",
            "--hover-color": "#eee",
        },
        "nav-link-selected": {"background-color": "#686868", "color": "white"},
    },
)

if selected == "Home":
    st.markdown("<div style='width:100%;height:60px;'></div>", unsafe_allow_html=True)
    st.image("images/pulitzer.png")
    st.markdown(
        "<div style='width:100%;display:flex;justify-content:center;font-size: 24px; color:#686868;'>Just Submit Your Article. We'll Do the Rest.</div>",
        unsafe_allow_html=True,
    )
    st.image("images/main-bottom.png")
elif selected == "Chat":
    st.title("퓰리쳐와 대화하기")

    mode = st.selectbox("모드 선택", ["데스크 모드", "일반기자 모드"])

    st.markdown(
        """
    <style>
    .horizontal-checkboxes {
        display: flex;
        flex-direction: row;
    }
    .horizontal-checkboxes > div {
        margin-right: 20px;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    options = [
        "이미지 생성",
        "헤드라인 생성",
        "요약 생성",
        "키워드 추출",
        "중제목 추출",
    ]
    selected_options = []

    st.markdown('<div class="horizontal-checkboxes">', unsafe_allow_html=True)
    for option in options:
        if st.checkbox(option):
            selected_options.append(option)
    st.markdown("</div>", unsafe_allow_html=True)

    article = st.text_area(
        placeholder="여기에 기사를 입력하세요.", height=400, label="기사 입력창"
    )

    system_prompt = """
    당신은 매우 유능한 기자이자 일러스트레이터입니다.

    다음 조건을 반드시 준수하세요.

    --- START OF CONDITIONS ---
    - 반드시 한국어로 결과물을 생성할 것.
    - 작업 순서를 반드시 지킬 것.
    --- END OF CONDITIONS ---

    이제 제출한 기사 원문의 내용을 이해하고, 순서에 따라 작업을 진행해주세요.
    """

    user_prompt = f"""
    기사 원문:

    --- START OF ARTICLE ---
    {article}
    --- END OF ARTICLE ---
    """

    if st.button("제출하기"):
        if article == "":
            st.warning("기사를 입력해주세요.")
            st.stop()

        if len(selected_options) < 3:
            st.warning("적어도 세개의 옵션을 선택해주세요.")
            st.stop()

        system_prompt += """
        --- START OF TASK ---
        빈 배열이 주어집니다. 이 배열에는 다음의 내용을 순서대로 담아주세요.
        """

        count = 1
        result_array = []

        for option in selected_options:
            if option == "헤드라인 생성":
                system_prompt += f"""
                {get_sequence_label(count)}, 원문에 가장 적합한 헤드라인을 생성하고 배열에 담아 제공해주세요.
                """
                count += 1
            elif option == "요약 생성":
                system_prompt += f"""
                {get_sequence_label(count)}, 원문 전체를 요약하고 배열에 담아 제공해주세요.
                """
                count += 1
            elif option == "키워드 추출":
                system_prompt += f"""
                {get_sequence_label(count)}, 중요한 순서대로 추출하여 키워드 5개 추출하고 하나의 배열에 담아 제공해주세요. 단, 단어는 중복되지 않고 음절로 나누지 않습니다.
                """
                count += 1
            elif option == "중제목 추출":
                system_prompt += f"""
                {get_sequence_label(count)}, 원문의 각 문단별 중제목을 추출하고 하나의 배열에 담아 제공해주세요.
                """
                count += 1

            if option != "이미지 생성":
                result_array.append(option)

        system_prompt += """
        마지막으로 배열 외에는 아무것도 추가하지 말고, 제출해주세요.
        --- END OF TASK ---
        """

        try:

            with st.spinner("열심히 작업 중이에요... 🕒"):
                completion = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                )

                st.markdown(
                    "<script>showToast('작업이 완료되었어요!')</script>",
                    unsafe_allow_html=True,
                )

                parsed_data = ast.literal_eval(completion.choices[0].message.content)

                headline = ""
                news_content = ""
                keywords = []
                topics = []

                for idx, val in enumerate(result_array):
                    if val == "헤드라인 생성":
                        headline = parsed_data[idx]
                    elif val == "요약 생성":
                        news_content = parsed_data[idx]
                    elif val == "키워드 추출":
                        keywords = parsed_data[idx]
                    elif val == "중제목 추출":
                        topics = parsed_data[idx]

                if "헤드라인 생성" in selected_options:
                    st.markdown(
                        "<h1 style='font-size: 24px;'>기사의 헤드라인을 생성했어요 📰</h1>",
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f"<i style='font-size: 20px;'>{headline}</i>",
                        unsafe_allow_html=True,
                    )

                if "요약 생성" in selected_options:
                    st.markdown(
                        "<h1 style='font-size: 24px;'>기사의 요약을 생성했어요 📰</h1>",
                        unsafe_allow_html=True,
                    )
                    st.write(f"{news_content}")

                if "키워드 추출" in selected_options:
                    keywords_html_content = "<div style='display:flex;justify-contents:flex-start;align-items:center;'>"

                    st.markdown(
                        "<h1 style='font-size: 24px;'>중요한 키워드 5개를 추출했어요 🧐</h1>",
                        unsafe_allow_html=True,
                    )
                    for keyword in keywords:
                        keywords_html_content += f"<div style='background-color: #00BB67; color: white; padding: 5px 10px; margin: 5px; border-radius: 10px;'>{keyword}</div>"

                    if len(keywords) == 0:
                        keywords_html_content += "<div style='background-color: #00BB67; color: white; padding: 5px 10px; margin: 5px; border-radius: 10px;'>키워드가 없어요</div>"

                    keywords_html_content += "</div>"
                    st.markdown(keywords_html_content, unsafe_allow_html=True)

                if "중제목 추출" in selected_options:
                    topics_html_content = "<div style='display:flex;justify-contents:flex-start;align-items:center;flex-wrap:wrap;'>"

                    st.markdown(
                        "<h1 style='font-size: 24px;'>기사의 중제목을 추출했어요 📝</h1>",
                        unsafe_allow_html=True,
                    )
                    for topic in topics:
                        topics_html_content += f"<div style='background-color: #00BB67; color: white; padding: 5px 10px; margin: 5px; border-radius: 10px;'>{topic}</div>"

                    topics_html_content += "</div>"
                    st.markdown(topics_html_content, unsafe_allow_html=True)

            if "이미지 생성" in selected_options:
                st.markdown(
                    "<div style='width:100%;height:60px;'></div>",
                    unsafe_allow_html=True,
                )
                with st.spinner("이미지 생성 중이에요... 🖼"):
                    user_image_prompt = f"""
                    Please understand the original article and express the most important parts with images. Don't add text, just create an image.

                    --- START OF ARTICLE ---
                    {article}
                    --- END OF ARTICLE ---
                    """

                    response = client.images.generate(
                        model="dall-e-3",
                        prompt=user_image_prompt,
                        size="1024x1024",
                        n=1,
                    )

                    st.markdown(
                        "<script>showToast('이미지가 생성되었어요!🩷')</script>",
                        unsafe_allow_html=True,
                    )

                    image_url = response.data[0].url
                    image_placeholder = st.empty()
                    image_placeholder.markdown(
                        f"<div style='width:100%;display:flex;justify-content:center;align-items:center;'>"
                        f"<img src='{image_url}' style='width:100%;height:auto;'>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )

                    # # Initialize image_edit_key
                    # image_edit_key = 0

                    # # Create an input field for the prompt
                    # image_edit_prompt = st.text_input(
                    #     label="이미지 편집 프롬프트",
                    #     placeholder="프롬프트를 입력해주세요.",
                    #     key=f"image_edit_{image_edit_key}",
                    # )

                    # # Create a button to update the image
                    # if st.button(
                    #     "이미지 업데이트", key=f"image_update_button_{image_edit_key}"
                    # ):
                    #     response = client.images.edit(
                    #         model="dall-e-3",
                    #         prompt=image_edit_prompt,
                    #         size="1024x1024",
                    #         n=1,
                    #     )
                    #     image_url = response.data[0].url
                    #     image_placeholder.markdown(
                    #         f"<div style='width:100%;display:flex;justify-content:center;align-items:center;'>"
                    #         f"<img src='{image_url}' style='width:100%;height:auto;'>"
                    #         f"</div>",
                    #         unsafe_allow_html=True,
                    #     )
                    #     # Increment the key for the next input (if needed)
                    #     image_edit_key += 1
        except Exception as e:
            st.error(f"오류가 발생했어요...ㅜㅜ 🤣 다시 시도해주세요.")

elif selected == "About":
    st.markdown(
        """
    <style>
    .about-container {
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
        font-size: 36px;
        font-weight: bold;
        padding: 16px 0;
    }
    .about-container > div {
        margin-right: 20px;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div class="about-container">
        기사 작성에만 집중하세요. 나머지는 AI가 할게요
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
    기사 원문만 등록하세요. 사진 생성부터 원문 요약까지 AI!
    기사에 적확한 보도 사진 자동 생성 및 기사 내용 효율적으로 요약해주는 기자용 AI 프로그램입니다.
    해당 서비스는 기자의 업무 효율을 최대 15% 높여줍니다.
    """
    )


# 기사 작성에만 집중하세요. 나머지는 AI가 할게요

# 기사 원문만 등록하세요. 사진 생성부터 원문 요약까지 AI!
# 기사에 적확한 보도 사진 자동 생성 및 기사 내용 효율적으로 요약해주는 기자용 AI 프로그램입니다.
# 해당 서비스는 기자의 업무 효율을 최대 15% 높여줍니다.
