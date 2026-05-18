import streamlit as st
import time

# ----------------------------------------------------------------------------
# PAGE CONFIG AND TITLE
# ----------------------------------------------------------------------------
st.set_page_config(page_title="Revive or Recycle", layout="centered")
st.title(":green[Revive or Recycle]")

# ----------------------------------------------------------------------------
# INITIALIZE SESSION STATE
# Steps:
#  1. Device Identification
#  2. Describe Condition
#  3. Processing
#  4. Verdict
# ----------------------------------------------------------------------------
if "step" not in st.session_state:
    st.session_state.step = 1
if "device_id_input" not in st.session_state:
    st.session_state.device_id_input = ""
if "condition_input" not in st.session_state:
    st.session_state.condition_input = "Select a condition"
if "verdict" not in st.session_state:
    st.session_state.verdict = ""
if "step1_response" not in st.session_state:
    st.session_state.step1_response = ""
if "step3_response" not in st.session_state:
    st.session_state.step3_response = ""

# ----------------------------------------------------------------------------
# "PROCESSING..." FUNCTIONS
# ----------------------------------------------------------------------------
def process_step1_input(device_text: str):
    """Placeholder for external processing.

    Replace this with call to device id script or API as needed. For now, it simulates a delay and returns a simple processed string.
    """
    # call to external script (uncomment and modify as needed)

    # Simulate a quick local processing placeholder for now.
    time.sleep(1.8)
    return f"Processed input: {device_text[:40]}..."


def process_verdict(device_text: str, condition: str):
    """Placeholder for final processing before verdict.

    Replace this with a call to market query engine or other processing as needed. For now, it simulates a delay and returns a simple verdict string.
    """
    # call to external script (uncomment and modify as needed)

    time.sleep(3.5)
    return f"Ready for verdict: {condition}"


# ----------------------------------------------------------------------------
# STEPS 1-2: Combined form (only one step's inputs visible at a time)
# ----------------------------------------------------------------------------
if st.session_state.step in (1, 2):
    with st.form("multi_step_form"):
        if st.session_state.step == 1:
            st.markdown("### Step 1: Device Identification")
            st.markdown("**Describe your device**")
            st.session_state.device_id_input = st.text_input(
                "Enter a brief description of your device",
                value=st.session_state.device_id_input,
                placeholder="Example: iPhone 11 with a cracked screen",
                help="Describe the device you would like to revive or recycle",
                key="device_input_field",
            )

            st.markdown("**- Or -**")
            st.markdown("**Upload a photo** *(Coming soon)*")
            st.file_uploader(
                "Choose a photo of your device",
                type=["jpg", "jpeg", "png"],
                disabled=True,
                key="photo_uploader",
            )

            next_clicked = st.form_submit_button("Next Step ->")

        elif st.session_state.step == 2:
            st.markdown("### Step 2: Describe Condition")
            st.markdown("**Your Device:**")
            st.write(f"<span style='color: grey;'>{st.session_state.device_id_input}</span>", unsafe_allow_html=True)

            # ----------------------------
            # TODO: Replace with dynamic options from step 1 processing response
            # ----------------------------
            # safe index handling for selectbox with a placeholder default
            options = ["Select a condition", "Broken Screen", "Dead Battery", "Very Used", "Other"]
            try:
                idx = options.index(st.session_state.condition_input)
            except ValueError:
                idx = 0
            st.markdown("**Your Condition: (TODO)**")
            st.session_state.condition_input = st.selectbox(
                "Choose a condition:", options, index=idx, key="condition_select"
            )
            st.markdown(">Review your inputs before proceeding to the verdict.", unsafe_allow_html=True)
            st.markdown("<br />", unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                back_clicked = st.form_submit_button("Back to Identification")
            with col2:
                next_clicked = st.form_submit_button("Next Step ->")

    # handle form button actions after the form block
    if st.session_state.step == 1 and 'next_clicked' in locals() and next_clicked:
        if st.session_state.device_id_input.strip():
            with st.spinner("Processing..."):
                st.session_state.step1_response = process_step1_input(
                    st.session_state.device_id_input
                )
            st.session_state.step = 2
            st.rerun()
        else:
            st.warning("Please enter a device description to proceed.")

    if st.session_state.step == 2:
        if 'back_clicked' in locals() and back_clicked:
            st.session_state.step = 1
            st.rerun()
        if 'next_clicked' in locals() and next_clicked:
            if st.session_state.condition_input == "Select a condition":
                st.warning("Please choose a condition before continuing.")
            else:
                st.session_state.step = 3
                st.rerun()

# ----------------------------------------------------------------------------
# Step 3: Processing
# ----------------------------------------------------------------------------
elif st.session_state.step == 3:
    st.markdown("### Step 3: Processing")
    with st.spinner("Running market query engine..."):
        st.session_state.step3_response = process_verdict(
            st.session_state.device_id_input,
            st.session_state.condition_input,
        )
    st.session_state.step = 4
    st.rerun()

# ----------------------------------------------------------------------------
# Step 4: Verdict
# ----------------------------------------------------------------------------
elif st.session_state.step == 4:
    st.markdown("### Step 4: Verdict")
    st.markdown("**Your Device:**")
    st.write(f"<span style='color: grey;'>{st.session_state.device_id_input}</span>", unsafe_allow_html=True)
    st.markdown("**Your Condition:**")
    st.markdown(
        f"<span style='color: grey;'>{st.session_state.condition_input}</span>",
        unsafe_allow_html=True,
    )

    
    # Placeholder integration point for recycle-service code.
    # Replace this with actual service logic or script call.
    if not st.session_state.verdict:
        st.session_state.verdict = "Recycle"

    st.markdown("**Verdict:**")
    st.success(st.session_state.verdict)

    # If verdict is "Recycle", show additional info (placeholder for now)
    if st.session_state.verdict == "Recycle":
        # make call to recycle-service code here and display results instead of placeholder text
        
        st.markdown("**Recycling Options:**")
        st.markdown(
            "- Option 1: ...\n- Option 2: ...\n\n*(Replace with actual options from recycle-service)*"
        )
    
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back to Condition"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("Start Over"):
            st.session_state.step = 1
            st.session_state.device_id_input = ""
            st.session_state.condition_input = "Select a condition"
            st.session_state.verdict = ""
            st.rerun()
