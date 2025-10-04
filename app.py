import streamlit as st
import json
from datetime import datetime

# 페이지 레이아웃을 'wide'로 설정하여 더 넓게 사용
st.set_page_config(layout="wide")

st.title("🎬 Advanced Sora2 JSON Prompt Generator")
st.write("탭을 이동하며 프롬프트를 완성해 보세요. 장면은 원하는 만큼 추가하고 편집할 수 있습니다.")

# --- 세션 상태 초기화 ---
# st.session_state: 사용자가 입력한 데이터를 앱의 다른 부분이나 재실행 시에도 기억하게 하는 저장 공간
if 'scenes' not in st.session_state:
    st.session_state.scenes = [] # 장면들을 저장할 리스트
if 'video_settings' not in st.session_state:
    st.session_state.video_settings = {
        'title': "AURA BUDS: 사운드를 해방하세요",
        'total_duration': "10s",
        'overall_style': "Sleek, modern, minimalist, Apple-style product commercial"
    }

# --- 탭 생성 ---
tab1, tab2, tab3 = st.tabs(["① 기본 정보 설정", "② 장면 편집기", "③ 프롬프트 생성"])

# --- Tab 1: 기본 정보 설정 ---
with tab1:
    st.header("영상의 전체적인 기본 정보를 입력하세요.")
    
    # st.session_state에 저장된 값을 불러와서 위젯의 기본값으로 사용
    st.session_state.video_settings['title'] = st.text_input(
        "영상의 주제/제목", st.session_state.video_settings['title']
    )
    st.session_state.video_settings['total_duration'] = st.text_input(
        "총 영상 길이 (예: 10s)", st.session_state.video_settings['total_duration']
    )
    st.session_state.video_settings['overall_style'] = st.text_area(
        "전체 스타일/분위기", st.session_state.video_settings['overall_style'], height=150
    )
    st.info("입력된 정보는 자동으로 저장됩니다. '② 장면 편집기' 탭으로 이동하세요.")

# --- Tab 2: 장면 편집기 (동적 추가/삭제) ---
with tab2:
    st.header("장면을 자유롭게 추가하고 편집하세요.")

    if st.button("➕ 장면 추가"):
        # 새 장면 템플릿
        new_scene = {
            'scene_number': len(st.session_state.scenes) + 1,
            'time': "", 'visual_description': "", 'animation_effect': "",
            'sound_effect': "", 'dialogue': None
        }
        st.session_state.scenes.append(new_scene)

    # st.session_state에 저장된 모든 장면에 대해 입력 필드를 생성
    for i, scene in enumerate(st.session_state.scenes):
        st.markdown("---")
        
        # 각 장면을 접고 펼 수 있는 expander
        with st.expander(f"**장면 #{i+1}** (시간: {scene.get('time', '')})", expanded=True):
            
            # 컬럼 생성: 왼쪽이 2배 더 넓음
            col1, col2 = st.columns([2, 1])

            with col1:
                scene['visual_description'] = st.text_area("시각적 묘사", scene.get('visual_description', ''), key=f"visual_{i}", height=200)

            with col2:
                scene['time'] = st.text_input("시간대 (예: 0s-4s)", scene.get('time', ''), key=f"time_{i}")
                scene['animation_effect'] = st.text_input("애니메이션/카메라 효과", scene.get('animation_effect', ''), key=f"anim_{i}")
                scene['sound_effect'] = st.text_input("효과음", scene.get('sound_effect', ''), key=f"sound_{i}")
            
            # 대사 추가
            st.markdown("---")
            if st.checkbox("이 장면에 대사 추가하기", key=f"dialogue_check_{i}"):
                if scene.get('dialogue') is None:
                     scene['dialogue'] = [{'character': '', 'line': '', 'tone': ''}]
                
                d_col1, d_col2, d_col3 = st.columns(3)
                scene['dialogue'][0]['character'] = d_col1.text_input("캐릭터", scene['dialogue'][0]['character'], key=f"char_{i}")
                scene['dialogue'][0]['line'] = d_col2.text_input("대사", scene['dialogue'][0]['line'], key=f"line_{i}")
                scene['dialogue'][0]['tone'] = d_col3.text_input("톤/분위기", scene['dialogue'][0]['tone'], key=f"tone_{i}")
            else:
                scene['dialogue'] = None

            # 장면 삭제 버튼
            if st.button("➖ 이 장면 삭제", key=f"delete_{i}"):
                st.session_state.scenes.pop(i)
                st.rerun() # 앱을 새로고침하여 UI에 즉시 반영

# --- Tab 3: 프롬프트 생성 ---
with tab3:
    st.header("최종 JSON 프롬프트를 확인하고 다운로드하세요.")
    
    if not st.session_state.scenes:
        st.warning("장면 편집기 탭에서 하나 이상의 장면을 추가해주세요.")
    else:
        if st.button("✨ JSON 프롬프트 생성하기"):
            # 최종 JSON 구조 만들기
            final_prompt = {
                "video_settings": st.session_state.video_settings,
                "scenes": st.session_state.scenes
            }
            
            st.success("✅ 프롬프트가 성공적으로 생성되었습니다!")
            st.json(final_prompt)
            
            # JSON 다운로드 버튼
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"sora_prompt_{timestamp}.json"
            
            st.download_button(
               label="📥 JSON 파일 다운로드",
               data=json.dumps(final_prompt, indent=2, ensure_ascii=False),
               file_name=file_name,
               mime="application/json",
           )