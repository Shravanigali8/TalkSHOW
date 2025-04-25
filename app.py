import streamlit as st
import subprocess
import os
import uuid

# Set page title
st.title("TalkSHOW Video Generator")

# Upload audio file
audio_file = st.file_uploader("Upload an audio file (.wav)", type=["wav"])

# Select demo type
demo_type = st.selectbox("Select demo type", ["Whole Body", "Only Face", "Diversity (Multiple Samples)"])

# Optional speaker ID input (with default)
speaker_id = st.number_input("Speaker ID", min_value=0, step=1, value=0)

# Button to trigger generation
if st.button("Generate Video"):
    if audio_file is None:
        st.warning("Please upload a .wav file.")
    else:
        # Ensure demo_audio folder exists
        os.makedirs("demo_audio", exist_ok=True)

        # Save uploaded audio file with a unique name to avoid overwrites
        unique_filename = f"{uuid.uuid4().hex}_{audio_file.name}"
        audio_path = os.path.join("demo_audio", unique_filename)
        # audio_path = './demo_audio/1st-page.wav'
        with open(audio_path, "wb") as f:
            f.write(audio_file.read())

        # Construct command
        if demo_type == "Whole Body":
            cmd = f"python scripts/demo.py --config_file ./config/body_pixel.json --infer --audio_file ./demo_audio/1st-page.wav --id 0 --whole_body"
        elif demo_type == "Only Face":
            cmd = f"python scripts/demo.py --config_file ./config/body_pixel.json --infer --audio_file ./demo_audio/1st-page.wav --id 0 --only_face"
        elif demo_type == "Diversity (Multiple Samples)":
            cmd = f"python scripts/demo.py --config_file ./config/body_pixel.json --infer --audio_file ./demo_audio/1st-page.wav --id 0 --num_sample 12"

        print(audio_path)
        # Run the command
        st.info("Running the generation script...")
        log_placeholder = st.empty()
        log_text = ""

        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        for line in iter(process.stdout.readline, ''):
            log_text += line
            log_placeholder.text(log_text)

        process.stdout.close()
        process.wait()

        # Try to locate generated video
        base_name = os.path.splitext(os.path.basename(audio_path))[0]
        video_dir = os.path.join("visualise", "video", "body-pixel2", f"{base_name}.mp4")
        # video_path = os.path.join(video_dir, f"{base_name}.mp4")
        video_path = 'visualise/video/body-pixel2/style.wav/style.mp4'

        if os.path.exists(video_path):
            st.success("Video generated successfully!")
            st.video(video_path)
        else:
            st.error("Video not found. Please check the logs for errors.")