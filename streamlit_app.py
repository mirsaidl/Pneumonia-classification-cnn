import streamlit_app as st
from fastai.vision.all import *
from PIL import Image
import numpy as np
import pathlib

model_path = Path("model.pkl")
learn = load_learner(model_path)
xray_model_path = Path("xraydet.pkl")
learn_xray = load_learner(xray_model_path)

def process_image(image):
    try: 
        img = image.resize((224, 224))
        img_fastai = Image.fromarray(np.array(img))
        pred_xray, _, _ = learn_xray.predict(image)
        
        if pred_xray == '1':
            pred, pred_id, probs = learn.predict(img_fastai)
            
            return pred, pred_id, probs
        else:
            pred, pred_id, probs = -1,-1,-1
            return pred, pred_id, probs
    except Exception:
        pred, pred_id, probs = -1,-1,-1
        return pred, pred_id, probs

# Main function to run the Streamlit app
def main():
    st.title('X-ray Pneumonia Detector by Mirsaid')
    st.markdown("""
    ##### Connect with Me
    - [GitHub](https://github.com/mirsaidl)
    - [LinkedIn](https://www.linkedin.com/in/mirsaid-abdurasulov-83b0242b2/)
    """)
    # Upload image
    uploaded_image = st.file_uploader('Upload X-ray Image', type=['jpg', 'jpeg', 'png'])

    if uploaded_image is not None:
        # Display the uploaded image
        image = Image.open(uploaded_image)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        # Process the image and display the result
        pred, prob_id, prob = process_image(image)
        if pred != -1:
            st.success(f"Prediction: {pred}")
            st.info(f"Probability: {prob[prob_id]*100:.1f}%")
        else:
            st.error("""Please send only lung x-ray pictures in clear format because it may affect result. Apart from this bot may not recognise picture. Try again""")
    st.markdown("""
    ## About Dataset
    Pneumonia is a serious infection that causes inflammation of the air sacs in the lungs, affecting millions of people worldwide. It is especially concerning for children under five years old, as it is a leading cause of death in this age group, surpassing other infectious diseases like HIV infection, malaria, or tuberculosis. Diagnosis of pneumonia often relies on symptoms and physical examinations, with chest X-rays playing a crucial role in confirming the presence of the disease.
    This dataset contains 5,856 validated Chest X-Ray images, meticulously labeled with the respective disease status: NORMAL, BACTERIA, or VIRUS, followed by a randomized patient ID and the image number of a patient. These images are valuable resources for researchers and healthcare professionals studying pneumonia and its impact on pediatric patients.
    The images, taken in the anterior-posterior view, were carefully selected from retrospective cohorts of pediatric patients aged one to five years old at the Guangzhou Women and Children’s Medical Center in Guangzhou. Each image represents a unique case, contributing to a comprehensive dataset for the study and analysis of pneumonia.
    Researchers and machine learning practitioners can use this dataset to develop and test algorithms for automated pneumonia detection, aiding in early diagnosis and treatment. Understanding the patterns and features in these X-ray images is crucial for improving healthcare outcomes and reducing the burden of pneumonia on vulnerable populations.
    For more details on the data collection methodology and comprehensive description, please refer to the referenced paper below.
    """)


if __name__ == '__main__':
    main()
