import streamlit as st
import json
from datetime import datetime
import re # 문자열 처리를 위한 re 라이브러리 추가

# --- 페이지 설정 및 기본 정보 (이전과 동일) ---
st.set_page_config(layout="wide")
st.title("🎬 Sora2 Script Builder (v2.1 - Parsing Enhanced)")
st.caption("AI 챗봇에게 물어볼 프롬프트를 생성하고, 그 결과를 가져와 전문적인 편집 도구로 완성하세요.")

# --- 세션 상태 초기화 (이전과 동일) ---
if 'scenes' not in st.session_state:
    st.session_state.scenes = []
if 'video_settings' not in st.session_state:
    st.session_state.video_settings = {'title': '샘플: 강아지 간식 광고', 'total_duration': '10s', 'overall_style': '밝고 따뜻하며 감성적인 느낌'}
    st.session_state.scenes = [{'scene_number': 1, 'time': '0s-4s', 'visual_description': '골든 리트리버 강아지가 주인을 애처롭게 쳐다본다.', 'animation_effect': '강아지의 눈망울을 클로즈업', 'sound_effect': '배경음악 시작, 강아지 낑낑 소리', 'dialogue': None}]

# --- 탭 구조 ---
tab1, tab2, tab3 = st.tabs(["① LLM 프롬프트 생성", "② 스크립트 편집", "③ 최종 결과 확인"])

# --- Tab 1: LLM 프롬프트 생성 ---
with tab1:
    st.header("1단계: LLM에게 요청할 프롬프트 생성하기")
    st.info(
        "아래 정보를 입력하고 '프롬프트 생성' 버튼을 누르세요. \n\n"
        "생성된 프롬프트를 복사하여 사용하시는 AI 챗봇(ChatGPT, Gemini 등)에게 질문하면, "
        "우리 앱이 이해할 수 있는 형식의 JSON 스크립트를 얻을 수 있습니다."
    )
    
    col1, col2 = st.columns(2)
    with col1:
        topic = st.text_input("영상의 핵심 주제는 무엇인가요?", "예: 반려견을 위한 프리미엄 수제 간식 광고")
        total_duration = st.text_input("총 영상 길이는 몇 초인가요?", "10s")
    with col2:
        overall_style = st.text_input("전체적인 스타일이나 분위기는 어떤가요?", "밝고 따뜻하며, 감성적인 느낌")
        num_scenes = st.number_input("몇 개의 장면으로 구성할까요?", min_value=1, value=3, step=1)
        
    if st.button("🤖 LLM 프롬프트 생성하기", type="primary"):
        
        # --- ▼▼▼ 여기를 수정하세요 ▼▼▼ ---
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
        st.write("아래 프롬프트를 전체 복사하여 ChatGPT, Gemini 등에 붙여넣고 결과를 받아오세요.")
        st.code(system_prompt, language="text")

# --- Tab 2: 스크립트 편집 ---
with tab2:
    st.header("2단계: 스크립트 불러오기 및 편집")
    st.subheader("📂 LLM 결과 붙여넣기")
    pasted_json = st.text_area("이곳에 AI 챗봇에게 받은 JSON 결과를 붙여넣고 '불러오기' 버튼을 누르세요.", height=150)
    
    if st.button("스크립트 불러오기"):
        if pasted_json:
            try:
                script_data = json.loads(pasted_json)
                
                # --- ★★★ 로직 개선 ★★★ ---
                # 1. video_settings 키 이름 차이 보정
                vs = script_data.get('video_settings', {})
                vs['total_duration'] = vs.pop('duration', vs.get('total_duration'))
                vs['overall_style'] = vs.pop('style', vs.get('overall_style'))
                st.session_state.video_settings = vs

                # 2. scenes의 dialogue 형식 차이 보정
                corrected_scenes = []
                for scene in script_data.get('scenes', []):
                    dialogue = scene.get('dialogue')
                    if isinstance(dialogue, str): # dialogue가 단순 텍스트인 경우
                        match = re.match(r'([^:]+):\s*"?([^"]+)"?', dialogue)
                        if match:
                            # "캐릭터: 대사" 형식을 객체로 변환
                            scene['dialogue'] = [{'character': match.group(1).strip(), 'line': match.group(2).strip(), 'tone': '자동 변환됨'}]
                        else: # 형식이 안 맞으면 그냥 대사만 넣음
                            scene['dialogue'] = [{'character': 'Unknown', 'line': dialogue, 'tone': '자동 변환됨'}]
                    corrected_scenes.append(scene)
                st.session_state.scenes = corrected_scenes

                st.success("스크립트를 성공적으로 불러왔습니다! 아래에서 내용을 편집하세요.")
                st.rerun()
            except (json.JSONDecodeError, KeyError) as e:
                st.error(f"오류: 유효한 스크립트 형식이 아닙니다. (오류: {e})")
        else:
            st.warning("먼저 텍스트 상자에 JSON 결과를 붙여넣어 주세요.")

    st.markdown("---")
    
    # --- 상세 편집 도구 UI ---
    st.subheader("🎬 장면 편집기")

    if st.button("➕ 장면 추가"):
        st.session_state.scenes.append({'scene_number': len(st.session_state.scenes) + 1})
        st.rerun()

    for i, scene in enumerate(st.session_state.scenes):
        with st.expander(f"**장면 #{i+1}** (시간: {scene.get('time', '지정 안됨')})", expanded=True):
            col1, col2 = st.columns([2, 1])
            with col1:
                scene['visual_description'] = st.text_area("시각적 묘사", scene.get('visual_description', ''), key=f"visual_{i}", height=150)
            with col2:
                scene['time'] = st.text_input("시간대", scene.get('time', ''), key=f"time_{i}")
                scene['animation_effect'] = st.text_input("애니메이션/카메라", scene.get('animation_effect', ''), key=f"anim_{i}")
                scene['sound_effect'] = st.text_input("효과음", scene.get('sound_effect', ''), key=f"sound_{i}")
            
            has_dialogue = st.checkbox("대사 추가/편집", value=scene.get('dialogue') is not None, key=f"dialogue_check_{i}")
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
            st.markdown("---")

# --- Tab 3: 최종 결과 확인 ---
with tab3:
    st.header("3단계: 최종 결과 확인 및 다운로드")
    if not st.session_state.scenes:
        st.warning("스크립트가 비어있습니다. '② 스크립트 편집' 탭에서 내용을 추가하거나 불러오세요.")
    else:
        # 현재 편집 중인 최종 결과물을 보여줌
        final_prompt = {
            "video_settings": st.session_state.video_settings,
            "scenes": st.session_state.scenes
        }
        st.json(final_prompt)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"sora_prompt_{timestamp}.json"
        
        st.download_button(
           label="📥 최종 JSON 파일 다운로드",
           data=json.dumps(final_prompt, indent=2, ensure_ascii=False),
           file_name=file_name,
           mime="application/json",
       )