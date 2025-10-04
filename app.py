import streamlit as st
import json
from datetime import datetime
import re

# --- Page Config ---
st.set_page_config(layout="wide")
st.title("🎬 Sora2 Script Builder")
st.caption("Generate a prompt for your AI chatbot, then paste the result to finalize your script with our professional editor.")

# --- Session State Initialization ---
if 'scenes' not in st.session_state:
    st.session_state.scenes = []
if 'video_settings' not in st.session_state:
    st.session_state.video_settings = {
        'title': '',
        'total_duration': '',
        'overall_style': ''
    }

# --- Template Data Definition ---
TEMPLATES = {
    "Select a template...": {},
    "Product Ad (10s)": {
        "video_settings": {
            "title": "AURA BUDS: Liberate Your Sound",
            "total_duration": "10s",
            "overall_style": "Sleek, modern, minimalist, Apple-style product commercial"
        },
        "scenes": [
            {'scene_number': 1, 'time': "0s-3s", 'visual_description': "[Problem] Showcases a character struggling with tangled wired earphones.", 'animation_effect': "Close-up shot emphasizing frustration", 'sound_effect': "Ambient noise, a sigh", 'dialogue': None},
            {'scene_number': 2, 'time': "3s-6s", 'visual_description': "[Solution] The 'AURA BUDS' product appears mysteriously, highlighting its sleek design.", 'animation_effect': "Dramatic camera work focusing on the product", 'sound_effect': "Magical sound effect", 'dialogue': None},
            {'scene_number': 3, 'time': "6s-10s", 'visual_description': "[Result] The character is happy and free using the product, followed by the brand logo.", 'animation_effect': "Tracking shot with a happy mood", 'sound_effect': "Upbeat background music starts", 'dialogue': None}
        ]
    },
    "Short Film Trailer (15s)": {
        "video_settings": {
            "title": "Movie Title: The Beginning",
            "total_duration": "15s",
            "overall_style": "Cinematic, dramatic lighting, suspenseful mood, film score"
        },
        "scenes": [
            {'scene_number': 1, 'time': "0s-5s", 'visual_description': "[Setup] Shows the setting of the film and the protagonist's peaceful daily life.", 'animation_effect': "Wide shot, peaceful mood", 'sound_effect': "Calm background music", 'dialogue': None},
            {'scene_number': 2, 'time': "5s-10s", 'visual_description': "[Inciting Incident] An unexpected event occurs, and the mood changes drastically. Shows the protagonist's shocked expression.", 'animation_effect': "Quick cuts, shaky handheld camera", 'sound_effect': "Tense, rising sound", 'dialogue': [{'character': 'Protagonist', 'line': 'What... is happening?', 'tone': 'Shocked voice'}]},
            {'scene_number': 3, 'time': "10s-15s", 'visual_description': "[Climax] A rapid montage of short clips hinting at the core conflict, ending with the movie title.", 'animation_effect': "Fast montage, fade to black", 'sound_effect': "Epic music crescendo", 'dialogue': None}
        ]
    }
}

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["① Generate LLM Prompt", "② Edit Script", "③ Final Result"])

# --- Tab 1: Generate LLM Prompt ---
with tab1:
    st.header("Step 1: Generate a Prompt for your LLM")
    st.info(
        "Fill in the fields below and click 'Generate LLM Prompt'.\n\n"
        "Copy the generated prompt and ask your AI chatbot (ChatGPT, Gemini, etc.) to get a JSON script that our app can understand."
    )
    
    col1, col2 = st.columns(2)
    with col1:
        topic = st.text_input("What is the core topic of the video?", "e.g., Premium homemade treats for dogs")
        total_duration = st.text_input("What is the total video duration?", "10s")
    with col2:
        overall_style = st.text_input("What is the overall style or mood?", "Bright, warm, and emotional")
        num_scenes = st.number_input("How many scenes should it have?", min_value=1, value=3, step=1)
        
    if st.button("🤖 Generate LLM Prompt", type="primary"):
        system_prompt = f"""
You are a creative video scriptwriter. Based on the user's topic and conditions, you must generate a video script in JSON format that OpenAI Sora 2 can understand.

You must strictly adhere to the following rules in your response:
1. The top-level keys in the JSON must be only 'video_settings' and 'scenes'.
2. The 'video_settings' object must include the keys 'title', 'total_duration', and 'overall_style'. Do not add other keys.
3. Each scene object in the 'scenes' list must include the keys 'scene_number', 'time', 'visual_description', 'animation_effect', 'sound_effect', and 'dialogue'.
4. The value for the 'dialogue' key must be one of the following two formats:
    - If there is no dialogue: `null`
    - If there is dialogue: A list containing an object like `[
        {{
            "character": "Character Name", 
            "line": "Line of dialogue", 
            "tone": "Tone of voice"
        }}
    ]` (Never use a simple string).
5. You must output only valid JSON formatted text as a response. Do not include code block markers (```json ... ```) or any other explanations.

---
[Generation Conditions]
- Topic: {topic}
- Total Duration: {total_duration}
- Overall Style: {overall_style}
- Number of Scenes: {num_scenes}
---
"""
        st.subheader("✅ Prompt Generated Successfully!")
        st.info("Copy the entire prompt below and paste it into ChatGPT, Gemini, etc., to get your result.")
        st.code(system_prompt, language="text")

# --- Tab 2: Edit Script ---
with tab2:
    st.header("Step 2: Edit & Manage Your Script")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📂 Load from Template")
        selected_template = st.selectbox("Start with a template", options=list(TEMPLATES.keys()))
        if selected_template != "Select a template...":
            if st.button(f"Apply '{selected_template}' Template"):
                st.session_state.video_settings = TEMPLATES[selected_template]["video_settings"].copy()
                st.session_state.scenes = TEMPLATES[selected_template]["scenes"].copy()
                st.success(f"Successfully applied the '{selected_template}' template.")
                st.rerun()
    with col2:
        st.subheader("📥 Paste LLM Result")
        pasted_json = st.text_area("Paste the JSON result from your AI chatbot here.", height=100)
        if st.button("Apply Pasted Script"):
            if pasted_json:
                try:
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
                        new_scene = {'scene_number': scene_data.get('scene_number', i + 1), 'time': scene_data.get('time', ''), 'visual_description': scene_data.get('visual_description', ''), 'animation_effect': scene_data.get('animation_effect', ''),'sound_effect': scene_data.get('sound_effect', ''),'dialogue': scene_data.get('dialogue')}
                        if isinstance(new_scene['dialogue'], str):
                            match = re.match(r'([^:]+):\s*"?([^"]+)"?', new_scene['dialogue'])
                            if match: new_scene['dialogue'] = [{'character': match.group(1).strip(), 'line': match.group(2).strip(), 'tone': 'Auto-converted'}]
                            else: new_scene['dialogue'] = [{'character': 'Unknown', 'line': new_scene['dialogue'], 'tone': 'Auto-converted'}]
                        new_scenes.append(new_scene)
                    st.session_state.scenes = new_scenes
                    st.success("Successfully applied the script.")
                    st.rerun()
                except (json.JSONDecodeError, KeyError) as e:
                    st.error(f"Error: Invalid JSON format. (Details: {e})")
            else:
                st.warning("Please paste the JSON result into the text box first.")

    st.markdown("---")
    
    st.header("🎬 Scene Editor")
    st.write("You can edit video information and add, edit, or delete scenes.")

    with st.expander("Edit Video Information", expanded=True):
        st.session_state.video_settings['title'] = st.text_input("Video Title", st.session_state.video_settings.get('title', ''))
        col1, col2 = st.columns(2)
        st.session_state.video_settings['total_duration'] = col1.text_input("Total Duration", st.session_state.video_settings.get('total_duration', ''))
        st.session_state.video_settings['overall_style'] = col2.text_input("Overall Style", st.session_state.video_settings.get('overall_style', ''))

    st.markdown("#### Scene List")
    if st.button("➕ Add New Scene"):
        st.session_state.scenes.append({'scene_number': len(st.session_state.scenes) + 1})
        st.rerun()

    if not st.session_state.scenes:
        st.info("No scenes available. Add a new scene or load a script from above.")
    
    for i, scene in enumerate(st.session_state.scenes):
        with st.container(border=True):
            col_main, col_delete = st.columns([10, 1])
            with col_main:
                st.subheader(f"Scene #{i+1}")
            with col_delete:
                if st.button("🗑️", key=f"delete_{i}", help="Delete this scene."):
                    st.session_state.scenes.pop(i)
                    st.rerun()

            col1, col2 = st.columns([2, 1])
            with col1: scene['visual_description'] = st.text_area("Visual Description", scene.get('visual_description', ''), key=f"visual_{i}", height=150)
            with col2:
                scene['time'] = st.text_input("Time", scene.get('time', ''), key=f"time_{i}")
                scene['animation_effect'] = st.text_input("Animation/Camera", scene.get('animation_effect', ''), key=f"anim_{i}")
                scene['sound_effect'] = st.text_input("Sound Effect", scene.get('sound_effect', ''), key=f"sound_{i}")
            has_dialogue = st.checkbox("Add/Edit Dialogue", value=scene.get('dialogue') is not None, key=f"dialogue_check_{i}")
            if has_dialogue:
                if scene.get('dialogue') is None: scene['dialogue'] = [{'character': '', 'line': '', 'tone': ''}]
                d_col1, d_col2, d_col3 = st.columns(3)
                dialogue_data = scene['dialogue'][0]
                dialogue_data['character'] = d_col1.text_input("Character", dialogue_data.get('character', ''), key=f"char_{i}")
                dialogue_data['line'] = d_col2.text_input("Line", dialogue_data.get('line', ''), key=f"line_{i}")
                dialogue_data['tone'] = d_col3.text_input("Tone/Mood", dialogue_data.get('tone', ''), key=f"tone_{i}")
            else: scene['dialogue'] = None


# --- Tab 3: Final Result ---
with tab3:
    st.header("Step 3: Review Final Result & Download")
    if not st.session_state.scenes:
        st.warning("The script is empty. Please add or load scenes in the '② Edit Script' tab.")
    else:
        final_prompt = {"video_settings": st.session_state.video_settings,"scenes": st.session_state.scenes}
        st.json(final_prompt)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"sora_prompt_{timestamp}.json"
        st.download_button(label="📥 Download Final JSON File", data=json.dumps(final_prompt, indent=2, ensure_ascii=False),file_name=file_name,mime="application/json")