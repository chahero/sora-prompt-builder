import streamlit as st
import json
from datetime import datetime

# 페이지 레이아웃 설정
st.set_page_config(layout="wide")

st.title("🎬 Advanced Sora2 JSON Prompt Generator")
st.write("탭을 이동하며 프롬프트를 완성해 보세요. 기본 샘플 데이터를 수정하거나 새 템플릿을 불러올 수 있습니다.")


# --- 템플릿 데이터 정의 ---
TEMPLATES = {
    "템플릿 선택...": {},
    "제품 광고 (10초)": {
        "video_settings": {
            "title": "AURA BUDS: 사운드를 해방하세요",
            "total_duration": "10s",
            "overall_style": "Sleek, modern, minimalist, Apple-style product commercial"
        },
        "scenes": [
            {'scene_number': 1, 'time': "0s-3s", 'visual_description': "[문제 상황] 주인공이 엉킨 유선 이어폰 때문에 불편해하는 모습을 보여준다.", 'animation_effect': "답답함을 강조하는 클로즈업", 'sound_effect': "일상 소음, 한숨 소리", 'dialogue': None},
            {'scene_number': 2, 'time': "3s-6s", 'visual_description': "[해결책 등장] 'AURA BUDS' 제품이 신비롭게 등장하며 세련된 디자인을 강조한다.", 'animation_effect': "제품을 돋보이게 하는 극적인 카메라 워크", 'sound_effect': "신비로운 사운드 효과", 'dialogue': None},
            {'scene_number': 3, 'time': "6s-10s", 'visual_description': "[행복한 결과] 제품을 사용하며 자유롭고 만족스러워하는 주인공의 모습을 보여주고, 마지막에 로고를 노출한다.", 'animation_effect': "행복한 분위기의 트래킹 샷", 'sound_effect': "경쾌한 배경 음악 시작", 'dialogue': None}
        ]
    },
    "단편 영화 예고편 (15초)": {
        "video_settings": {
            "title": "영화 제목: 운명의 서막",
            "total_duration": "15s",
            "overall_style": "Cinematic, dramatic lighting, suspenseful mood, film score"
        },
        "scenes": [
            {'scene_number': 1, 'time': "0s-5s", 'visual_description': "[배경 설정] 영화의 배경이 되는 장소와 평화로운 주인공의 일상을 보여준다.", 'animation_effect': "와이드 샷, 평화로운 분위기", 'sound_effect': "잔잔한 배경 음악", 'dialogue': None},
            {'scene_number': 2, 'time': "5s-10s", 'visual_description': "[사건 발생] 예기치 못한 사건이 발생하며 분위기가 급변한다. 주인공의 놀란 표정을 보여준다.", 'animation_effect': "빠른 컷 전환, 불안한 핸드헬드", 'sound_effect': "긴장감을 고조시키는 사운드", 'dialogue': [{'character': '주인공', 'line': '이게... 대체 무슨 일이야?', 'tone': '충격받은 목소리'}]},
            {'scene_number': 3, 'time': "10s-15s", 'visual_description': "[핵심 질문] 영화의 핵심 갈등을 암시하는 짧은 장면들을 빠르게 보여주고, 마지막에 영화 제목을 띄운다.", 'animation_effect': "빠른 몽타주, 페이드 아웃", 'sound_effect': "웅장한 음악과 함께 끝", 'dialogue': None}
        ]
    }
}


# --- ★★★ 핵심 수정 사항 ★★★ ---
# 세션 상태 초기화: st.session_state에 'scenes' 키가 없거나, 있더라도 리스트가 비어있으면 기본 템플릿을 샘플로 로드합니다.
if "scenes" not in st.session_state or not st.session_state.scenes:
    st.session_state.video_settings = TEMPLATES["제품 광고 (10초)"]["video_settings"].copy()
    st.session_state.scenes = TEMPLATES["제품 광고 (10초)"]["scenes"].copy()


# --- 탭 생성 ---
tab1, tab2, tab3 = st.tabs(["① 기본 정보 설정", "② 장면 편집기", "③ 프롬프트 생성"])

# --- Tab 1: 기본 정보 설정 ---
with tab1:
    st.header("영상의 전체적인 기본 정보를 입력하세요.")

    selected_template = st.selectbox(
        "새로운 템플릿을 불러올 수 있습니다.",
        options=list(TEMPLATES.keys())
    )

    if selected_template != "템플릿 선택...":
        if st.button(f"'{selected_template}' 템플릿 불러오기"):
            st.session_state.video_settings = TEMPLATES[selected_template]["video_settings"].copy()
            st.session_state.scenes = TEMPLATES[selected_template]["scenes"].copy()
            st.success(f"'{selected_template}' 템플릿을 성공적으로 불러왔습니다! '② 장면 편집기' 탭에서 내용을 수정하세요.")
            st.rerun() # 앱을 새로고침하여 변경사항을 즉시 반영

    st.markdown("---")
    
    st.session_state.video_settings['title'] = st.text_input(
        "영상의 주제/제목", st.session_state.video_settings.get('title', '')
    )
    st.session_state.video_settings['total_duration'] = st.text_input(
        "총 영상 길이 (예: 10s)", st.session_state.video_settings.get('total_duration', '')
    )
    st.session_state.video_settings['overall_style'] = st.text_area(
        "전체 스타일/분위기", st.session_state.video_settings.get('overall_style', ''), height=150
    )

# --- Tab 2: 장면 편집기 ---
with tab2:
    st.header("장면을 자유롭게 추가하고 편집하세요.")

    if st.button("➕ 장면 추가"):
        new_scene = {
            'scene_number': len(st.session_state.scenes) + 1,
            'time': "", 'visual_description': "", 'animation_effect': "",
            'sound_effect': "", 'dialogue': None
        }
        st.session_state.scenes.append(new_scene)
        st.rerun()

    for i, scene in enumerate(st.session_state.scenes):
        st.markdown("---")
        with st.expander(f"**장면 #{i+1}** (시간: {scene.get('time', '')})", expanded=True):
            col1, col2 = st.columns([2, 1])
            with col1:
                scene['visual_description'] = st.text_area("시각적 묘사", scene.get('visual_description', ''), key=f"visual_{i}", height=200)
            with col2:
                scene['time'] = st.text_input("시간대", scene.get('time', ''), key=f"time_{i}")
                scene['animation_effect'] = st.text_input("애니메이션/카메라 효과", scene.get('animation_effect', ''), key=f"anim_{i}")
                scene['sound_effect'] = st.text_input("효과음", scene.get('sound_effect', ''), key=f"sound_{i}")
            
            st.markdown("---")
            has_dialogue = st.checkbox("이 장면에 대사 추가하기", value=scene.get('dialogue') is not None, key=f"dialogue_check_{i}")
            if has_dialogue:
                if scene.get('dialogue') is None:
                     scene['dialogue'] = [{'character': '', 'line': '', 'tone': ''}]
                
                d_col1, d_col2, d_col3 = st.columns(3)
                dialogue_data = scene['dialogue'][0]
                dialogue_data['character'] = d_col1.text_input("캐릭터", dialogue_data.get('character', ''), key=f"char_{i}")
                dialogue_data['line'] = d_col2.text_input("대사", dialogue_data.get('line', ''), key=f"line_{i}")
                dialogue_data['tone'] = d_col3.text_input("톤/분위기", dialogue_data.get('tone', ''), key=f"tone_{i}")
            else:
                scene['dialogue'] = None

            if st.button("➖ 이 장면 삭제", key=f"delete_{i}"):
                st.session_state.scenes.pop(i)
                st.rerun()

# --- Tab 3: 프롬프트 생성 ---
with tab3:
    st.header("최종 JSON 프롬프트를 확인하고 다운로드하세요.")
    if not st.session_state.scenes:
        st.warning("장면 편집기 탭에서 하나 이상의 장면을 추가해주세요.")
    else:
        final_prompt = {
            "video_settings": st.session_state.video_settings,
            "scenes": st.session_state.scenes
        }
        st.json(final_prompt)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"sora_prompt_{timestamp}.json"
        
        st.download_button(
           label="📥 JSON 파일 다운로드",
           data=json.dumps(final_prompt, indent=2, ensure_ascii=False),
           file_name=file_name,
           mime="application/json",
       )