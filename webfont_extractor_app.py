
import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

st.set_page_config(page_title="웹폰트 추출기", layout="centered")
st.title("🧩 웹폰트 추출기")
st.write("웹사이트 주소를 입력하면, 해당 사이트에서 사용하는 웹폰트 파일을 추출해줍니다.")

url = st.text_input("🔗 웹사이트 주소 입력", placeholder="예: https://together.kakao.com")

if st.button("🎯 추출하기") and url:
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        font_urls = set()
        font_names = set()

        for link in soup.find_all("link", {"rel": "stylesheet"}):
            href = link.get("href")
            css_url = urljoin(url, href)
            css_response = requests.get(css_url, timeout=10)
            css_text = css_response.text

            font_faces = re.findall(r"@font-face\s*{.*?}", css_text, re.DOTALL)
            for face in font_faces:
                name_match = re.search(r"font-family:\s*['\"]?(.*?)['\"]?;", face)
                if name_match:
                    font_names.add(name_match.group(1))

                urls = re.findall(r"url\(['\"]?(.*?\.(woff2?|ttf|otf))['\"]?\)", face)
                for match in urls:
                    full_font_url = urljoin(css_url, match[0])
                    font_urls.add(full_font_url)

        if font_urls:
            st.success("✅ 웹폰트 추출 성공! 다운로드 링크는 아래에 있습니다.")
            for i, font_url in enumerate(font_urls, start=1):
                st.markdown(f"{i}. [📥 {font_url.split('/')[-1]}]({font_url})")
        else:
            st.warning("⚠️ 웹폰트를 찾을 수 없거나 접근이 제한되어 있어요.")

        if font_names:
            st.markdown("---")
            st.markdown("### 🏷️ 사용된 폰트 이름")
            for name in font_names:
                st.markdown(f"- {name}")

    except Exception as e:
        st.error(f"❌ 에러가 발생했어요: {e}")
