import streamlit as st
import json
from datetime import datetime
import re

# --- 페이지 설정 및 기본 정보 ---
st.set_page_config(layout="wide")
st.title("🎬 Sora2 Script Builder")
st.caption("AI 챗봇에게 물어볼 프롬프트를 생성하고, 그 결과를 가져와 전문적인 편집 도구로 완성하세요.")

# --- ★★★ 핵심 수정 사항 ★★★ ---
# 세션 상태 초기화: 이제 아무 데이터도 없는 '빈 상태'로 시작합니다.
if 'scenes' not in st.session_state:
    st.session_state.scenes = []
if 'video_settings' not in st.session_state:
    st.session_state.video_settings = {
        'title': '',
        'total_duration': '',
        'overall_style': ''
    }

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

# --- 이하 코드는 v2.2와 대부분 동일 ---

# --- 탭 구조 ---
tab1, tab2, tab3 = st.tabs(["① LLM 프롬프트 생성", "② 스크립트 편집", "③ 최종 결과 확인"])

# --- Tab 1: LLM 프롬프트 생성 ---
with tab1:
    st.header("1단계: LLM에게 요청할 프롬프트 생성하기")
    # ... (Tab 1 코드는 이전과 동일)
    col1, col2 = st.columns(2)
    with col1:
        topic = st.text_input("영상의 핵심 주제는 무엇인가요?", "예: 반려견을 위한 프리미엄 수제 간식 광고")
        total_duration = st.text_input("총 영상 길이는 몇 초인가요?", "10s")
    with col2:
        overall_style = st.text_input("전체적인 스타일이나 분위기는 어떤가요?", "밝고 따뜻하며, 감성적인 느낌")
        num_scenes = st.number_input("몇 개의 장면으로 구성할까요?", min_value=1, value=3, step=1)
        
    if st.button("🤖 LLM 프롬프트 생성하기", type="primary"):
        system_prompt = f"""
당신은 창의적인 비디오 스크립트 작가입니다. 사용자가 제시한 주제와 조건에 맞춰, OpenAI Sora 2가 이해할 수 있는 JSON 형식의 비디오 스크립트를 생성해야 합니다.

아래 규칙을 반드시 준수하여 응답해주세요:
1.  JSON의 최상위 키는 'video_settings'와 'scenes' 두 개만 사용합니다.
2.  'video_settings' 객체 안에는 'title', 'total_duration', 'overall_style' 키를 반드시 포함해야 합니다. 다른 키는 추가하지 마세요.
3.  'scenes' 리스트 안의 각 장면 객체는 'scene_number', 'time', 'visual_description', 'animation_effect', 'sound_effect', 'dialogue' 키를 포함해야 합니다.
4.  'dialogue' 키의 값은 아래 두 가지 형식 중 하나여야 합니다:
    - 대사가 없는 경우: `null`
    - 대사가 있는 경우: `[
        {{
            "character": "캐릭터명", 
            "line": "대사 내용", 
            "tone": "대사 톤"
        }}
    ]` 형식의 리스트. (절대로 단순 텍스트로 만들지 마세요)
5.  반드시 유효한 JSON 형식의 텍스트만 응답으로 출력해야 하며, 코드 블록 마커(`json ... `)나 다른 설명은 절대로 덧붙이지 마세요.

---
[생성 조건]
- 주제: {topic}
- 총 길이: {total_duration}
- 전체 스타일: {overall_style}
- 장면 수: {num_scenes}
---
"""
        st.subheader("✅ 프롬프트 생성 완료!")
        st.code(system_prompt, language="text")

# --- Tab 2: 스크립트 편집 ---
with tab2:
    st.header("2단계: 스크립트 편집 및 관리")
    
    # --- 상단 컨트롤 섹션 ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📂 스크립트 불러오기")
        # 템플릿 불러오기
        selected_template = st.selectbox("템플릿으로 시작하기", options=list(TEMPLATES.keys()))
        if selected_template != "템플릿 선택...":
            if st.button(f"'{selected_template}' 템플릿 적용하기"):
                st.session_state.video_settings = TEMPLATES[selected_template]["video_settings"].copy()
                st.session_state.scenes = TEMPLATES[selected_template]["scenes"].copy()
                st.success(f"'{selected_template}' 템플릿을 적용했습니다.")
                st.rerun()
    with col2:
        # JSON 붙여넣기
        st.subheader("📥 LLM 결과 붙여넣기")
        pasted_json = st.text_area("이곳에 AI 챗봇에게 받은 JSON 결과를 붙여넣으세요.", height=100)
        if st.button("붙여넣은 스크립트 적용하기"):
            if pasted_json:
                try:
                    # ... (v2.2의 안정적인 파싱 로직은 그대로 유지)
                    script_data = json.loads(pasted_json)
                    loaded_vs = script_data.get('video_settings', {})
                    new_video_settings = {
                        'title': loaded_vs.get('title', ''),
                        'total_duration': loaded_vs.get('total_duration') or loaded_vs.get('duration', ''),
                        'overall_style': loaded_vs.get('overall_style') or loaded_vs.get('style', '')
                    }
                    st.session_state.video_settings = new_video_settings
                    new_scenes = []
                    for i, scene_data in enumerate(script_data.get('scenes', [])):
                        # ... (이하 파싱 로직 동일)
                        new_scene = {'scene_number': scene_data.get('scene_number', i + 1), 'time': scene_data.get('time', ''), 'visual_description': scene_data.get('visual_description', ''), 'animation_effect': scene_data.get('animation_effect', ''),'sound_effect': scene_data.get('sound_effect', ''),'dialogue': scene_data.get('dialogue')}
                        if isinstance(new_scene['dialogue'], str):
                            match = re.match(r'([^:]+):\s*"?([^"]+)"?', new_scene['dialogue'])
                            if match: new_scene['dialogue'] = [{'character': match.group(1).strip(), 'line': match.group(2).strip(), 'tone': '자동 변환됨'}]
                            else: new_scene['dialogue'] = [{'character': 'Unknown', 'line': new_scene['dialogue'], 'tone': '자동 변환됨'}]
                        new_scenes.append(new_scene)
                    st.session_state.scenes = new_scenes
                    st.success("스크립트를 성공적으로 적용했습니다.")
                    st.rerun()
                except (json.JSONDecodeError, KeyError) as e:
                    st.error(f"오류: 유효한 스크립트 형식이 아닙니다. (오류: {e})")
            else:
                st.warning("먼저 텍스트 상자에 JSON 결과를 붙여넣어 주세요.")

    st.markdown("---")
    
    # --- 상세 편집 도구 UI ---
    st.header("🎬 장면 편집기")
    st.write("영상 정보를 수정하고, 장면을 추가, 편집, 삭제할 수 있습니다.")

    # 기본 정보 수정
    with st.expander("영상 기본 정보 수정하기", expanded=True):
        st.session_state.video_settings['title'] = st.text_input("영상 제목", st.session_state.video_settings.get('title', ''))
        col1, col2 = st.columns(2)
        st.session_state.video_settings['total_duration'] = col1.text_input("총 길이", st.session_state.video_settings.get('total_duration', ''))
        st.session_state.video_settings['overall_style'] = col2.text_input("전체 스타일", st.session_state.video_settings.get('overall_style', ''))

    st.markdown("#### 장면 목록")
    if st.button("➕ 새 장면 추가"):
        st.session_state.scenes.append({'scene_number': len(st.session_state.scenes) + 1})
        st.rerun()

    if not st.session_state.scenes:
        st.info("장면이 없습니다. '새 장면 추가' 버튼을 누르거나, 상단에서 스크립트를 불러오세요.")
    
    for i, scene in enumerate(st.session_state.scenes):
        with st.container(border=True): # 각 장면을 컨테이너로 묶어 UI 개선
            col_main, col_delete = st.columns([10, 1])
            with col_main:
                st.subheader(f"장면 #{i+1}")
            with col_delete:
                if st.button("🗑️", key=f"delete_{i}", help="이 장면을 삭제합니다."):
                    st.session_state.scenes.pop(i)
                    st.rerun()

            # ... (이하 편집기 UI는 이전과 동일)
            col1, col2 = st.columns([2, 1])
            with col1: scene['visual_description'] = st.text_area("시각적 묘사", scene.get('visual_description', ''), key=f"visual_{i}", height=150)
            with col2:
                scene['time'] = st.text_input("시간대", scene.get('time', ''), key=f"time_{i}")
                scene['animation_effect'] = st.text_input("애니메이션/카메라", scene.get('animation_effect', ''), key=f"anim_{i}")
                scene['sound_effect'] = st.text_input("효과음", scene.get('sound_effect', ''), key=f"sound_{i}")
            has_dialogue = st.checkbox("대사 추가/편집", value=scene.get('dialogue') is not None, key=f"dialogue_check_{i}")
            if has_dialogue:
                if scene.get('dialogue') is None: scene['dialogue'] = [{'character': '', 'line': '', 'tone': ''}]
                d_col1, d_col2, d_col3 = st.columns(3)
                dialogue_data = scene['dialogue'][0]
                dialogue_data['character'] = d_col1.text_input("캐릭터", dialogue_data.get('character', ''), key=f"char_{i}")
                dialogue_data['line'] = d_col2.text_input("대사", dialogue_data.get('line', ''), key=f"line_{i}")
                dialogue_data['tone'] = d_col3.text_input("톤/분위기", dialogue_data.get('tone', ''), key=f"tone_{i}")
            else: scene['dialogue'] = None


# --- Tab 3: 최종 결과 확인 ---
with tab3:
    st.header("3단계: 최종 결과 확인 및 다운로드")
    if not st.session_state.scenes:
        st.warning("스크립트가 비어있습니다. '② 스크립트 편집' 탭에서 내용을 추가하거나 불러오세요.")
    else:
        final_prompt = {"video_settings": st.session_state.video_settings,"scenes": st.session_state.scenes}
        st.json(final_prompt)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"sora_prompt_{timestamp}.json"
        st.download_button(label="📥 최종 JSON 파일 다운로드",data=json.dumps(final_prompt, indent=2, ensure_ascii=False),file_name=file_name,mime="application/json")