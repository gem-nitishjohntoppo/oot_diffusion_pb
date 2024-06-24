import base64
import os
import replicate
import streamlit as st
from streamlit_image_select import image_select
from dotenv import load_dotenv
load_dotenv()
# Set Replicate API token
os.environ['REPLICATE_API_TOKEN'] = os.environ.get('REPLICATE_API_TOKEN')
st.title('OOTDiffusion Demo')

with st.container():
    # Streamlit setup
    with st.sidebar:
        img_file_buffer = st.file_uploader('Upload a Garment', type=['png', 'jpg'])
        img_file_buffer1 = st.file_uploader('Upload a Model', type=['png', 'jpg'])

    # Define image paths
    images_men = [
        "assets/garments/TS1.jpg", "assets/garments/TS2.jpg", "assets/garments/TS3.jpg",
        "assets/garments/TS4.jpg", "assets/garments/TS5.jpg", "assets/garments/TS6.jpg",
        "assets/garments/TS7.jpg", "assets/garments/TS8.jpg", "assets/garments/TS9.jpg",
        "assets/garments/TS10.jpg", "assets/garments/TS11.jpg", "assets/garments/TS12.jpg",
        "assets/garments/TS13.jpg", "assets/garments/TS14.jpg", "assets/garments/TS15.jpg",
        "assets/garments/TS16.jpg"
    ]

    models = ["assets/models/Model1.png", "assets/models/Model2.png"]

    st.header('Clothes Collection')
    selected_image_men = image_select("Select a garment", images_men, key="selected_image_men")

    st.header('Model')
    model_select = image_select("Select a model", models, key="model_select")

    st.header('Selected')

    # Initialize variables for image URIs
    garment_image_uri = None
    model_image_uri = None

    # Convert uploaded files to URIs or use predefined paths
    if img_file_buffer is not None:
        garment_image_uri = img_file_buffer
    elif selected_image_men is not None:
        garment_image_uri = selected_image_men

    if img_file_buffer1 is not None:
        model_image_uri = img_file_buffer1
    elif model_select is not None:
        model_image_uri = model_select

    # Load image data from predefined paths and convert to base64 URIs
    if garment_image_uri is not None and isinstance(garment_image_uri, str) and garment_image_uri.startswith("assets/"):
        with open(garment_image_uri, 'rb') as file:
            data = base64.b64encode(file.read()).decode('utf-8')
            garment_image_uri = f"data:image/jpeg;base64,{data}"

    if model_image_uri is not None and isinstance(model_image_uri, str) and model_image_uri.startswith("assets/"):
        with open(model_image_uri, 'rb') as file:
            data = base64.b64encode(file.read()).decode('utf-8')
            model_image_uri = f"data:image/jpeg;base64,{data}"

    col1, col2 = st.columns(2)

    with col1:
        if model_image_uri is not None:
            st.image(model_image_uri, caption='Selected Model')

    with col2:
        if garment_image_uri is not None:
            st.image(garment_image_uri, caption='Selected Garment')

    # Process images if 'Generate' button is clicked
    if st.button('Generate'):
        # Check if both garment_image_uri and model_image_uri are set
        if garment_image_uri is not None and model_image_uri is not None:
            input_data = {
                "garment_image": garment_image_uri,
                "model_image": model_image_uri
            }

            # Call replicate.run() with URIs
            try:
                # output = replicate.run(
                #     "viktorfa/oot_diffusion:9f8fa4956970dde99689af7488157a30aa152e23953526a605df1d77598343d7",
                #     input=input_data
                # )
                output = replicate.run(
                    "viktorfa/oot_diffusion:9f8fa4956970dde99689af7488157a30aa152e23953526a605df1d77598343d7",
                    input=input_data
                )
                # Save the output URLs in session state
                st.session_state.image_urls = output
                st.session_state.index = 0

            except Exception as e:
                st.error(f"Error occurred during processing: {e}")
        else:
            st.error("Please upload both a garment image and select a model image.")

# Display images and navigation button if available in session state
if 'image_urls' in st.session_state:
    image_urls = st.session_state.image_urls

    # Function to increment the index
    def next_image():
        st.session_state.index = (st.session_state.index + 1) % len(image_urls)

    # Display the current image
    st.image(image_urls[st.session_state.index])

    # Button to go to the next image
    st.button("Next", on_click=next_image)
