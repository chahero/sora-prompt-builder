import streamlit as st
import json
from datetime import datetime

# Streamlit 앱의 제목 설정
st.title("🎬 Sora2 JSON 프롬프트 생성기")
st.write("아래 필드를 채워 Sora 2를 위한 완벽한 JSON 프롬프트를 생성해 보세요.")

# --- 1. 영상 기본 정보 입력 (사이드바) ---
with st.sidebar:
    st.header("1. 영상 기본 정보")
    video_title = st.text_input("영상의 주제/제목", "예: AURA BUDS 광고")
    total_duration = st.text_input("총 영상 길이 (예: 10s)", "10s")
    overall_style = st.text_area("전체 스타일/분위기", "Sleek, modern, minimalist, Apple-style product commercial")
    num_scenes = st.number_input("구성할 장면의 수", min_value=1, value=2, step=1)

# --- 2. 장면별 상세 정보 입력 ---
st.header("2. 장면별 상세 정보")

# 각 장면의 데이터를 저장할 리스트 초기화
# st.session_state를 사용해 사용자가 입력한 값을 앱이 재실행되어도 유지
if 'scenes_data' not in st.session_state:
    st.session_state.scenes_data = [{}] * num_scenes

scenes = []
for i in range(num_scenes):
    st.subheader(f"장면 #{i+1}")
    
    # st.expander를 사용해 각 장면을 접고 펼 수 있게 만듦
    with st.expander(f"장면 #{i+1} 설정하기", expanded=i==0):
        scene = {}
        scene['scene_number'] = i + 1
        scene['time'] = st.text_input(f"시간대 (예: 0s-4s)", key=f"time_{i}")
        scene['visual_description'] = st.text_area(f"시각적 묘사", key=f"visual_{i}")
        scene['animation_effect'] = st.text_input(f"애니메이션/카메라 효과", key=f"anim_{i}")
        scene['sound_effect'] = st.text_input(f"효과음", key=f"sound_{i}")
        
        # 대사 추가 기능
        if st.checkbox("이 장면에 대사 추가하기", key=f"dialogue_check_{i}"):
            dialogue = {}
            dialogue['character'] = st.text_input("캐릭터", key=f"char_{i}")
            dialogue['line'] = st.text_input("대사", key=f"line_{i}")
            dialogue['tone'] = st.text_input("톤/분위기", key=f"tone_{i}")
            scene['dialogue'] = [dialogue] # 여러 대사를 위해 리스트로 감쌈
        else:
            scene['dialogue'] = None
            
        scenes.append(scene)

# --- 3. JSON 생성 및 다운로드 ---
st.header("3. 프롬프트 생성")

if st.button("✨ JSON 프롬프트 생성하기"):
    # 최종 JSON 구조 만들기
    final_prompt = {
        "video_settings": {
            "title": video_title,
            "total_duration": total_duration,
            "format": "Horizontal",
            "aspect_ratio": "16:9",
            "resolution": "1920x1080",
            "overall_style": overall_style
        },
        "scenes": scenes
    }
    
    # 생성된 JSON 화면에 보여주기
    st.success("✅ 프롬프트가 성공적으로 생성되었습니다!")
    st.json(final_prompt)
    
    # JSON 다운로드 버튼 만들기
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"sora_prompt_{timestamp}.json"
    
    st.download_button(
       label="📥 JSON 파일 다운로드",
       data=json.dumps(final_prompt, indent=2, ensure_ascii=False),
       file_name=file_name,
       mime="application/json",
   )