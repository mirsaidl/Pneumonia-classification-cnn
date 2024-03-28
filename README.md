# X-ray Pneumonia Detector

Deployed in 2 appllication:
1 [Telegram Bot](https://t.me/xray_pneumonia_bot)
2 [Streamlit (Hugging Face)](https://huggingface.co/spaces/mirsaid5455/X-ray-Pneumonia-Detector)

Contact me:
[Github](https://github.com/mirsaidl)
[Linkedin](https://www.linkedin.com/feed/update/urn:li:activity:7178428435713650690/)

Watch Demo Videos:
![Telegram Bot](Screen_Recording_20240327_005417_Telegram.gif)
![Streamlit (Hugging Face)](video_2024-03-29_07-10-38.gif)
Note: More on Linkedin Posts


###
### **How I Developed this Telegram Bot and Streamlit App:**

1. **Dataset from Kaggle:** Initially, I gathered a comprehensive dataset from Kaggle, which served as the foundation for training our models.

2. **CNN Training without Transfer Learning:** We began by training the dataset using Convolutional Neural Networks (CNN) without transfer learning, achieving an impressive accuracy of 90%.

3. **Transfer Learning with TensorFlow and Fastai:** Next, we employed Transfer Learning techniques with both TensorFlow and Fastai, fine-tuning the models. The results were remarkable, with accuracies of 97% and 98% respectively.

4. **Telegram Bot Deployment:** I deployed the model on Telegram Bot, incorporating features such as multilingual support.

5. **Enhanced Image Detection:** To ensure robustness, we expanded our dataset with more than 5000 additional X-ray images. This allowed us to train a separate model with 100% accuracy to distinguish between X-ray and non-X-ray images.

6. **Continuous Improvement:** Ongoing debugging and refinements were made to ensure the bot's efficiency and accuracy.

7. **Streamlit App Deployment:** I deployed Streamlit app through Hugging Face repository


### **🌟 Purpose:**
Our bot is designed to empower medical professionals and individuals with rapid and accurate lung condition diagnosis using X-ray images.

### **🧠 Two Powerful Models:**
- **X-ray Image Detection (Accuracy: 100%):** The first model ensures the uploaded image is a valid X-ray scan, guaranteeing the right data for analysis.
- **Pneumonia Detection (Accuracy: 98%):** The second model specializes in detecting pneumonia within these X-ray images, providing reliable diagnoses.

### **🔍 ResNet Transfer Learning CNN:**
Our bot is built on ResNet transfer learning convolutional neural network (CNN). Trained on a vast dataset, it can identify patterns associated with lung diseases, particularly pneumonia.

### **⚙️ How It Works:**
- **Upload an X-ray Image:** Simply upload an X-ray image to the bot.
- **Automated Analysis:** The bot verifies if it's a valid X-ray scan, then meticulously examines the image to detect signs of pneumonia.
- **Instant Results:** Fast and reliable results are provided, indicating the patient's lung condition.


### **🚀 Let's Connect:**
Note: I haven't deployed it to server yet. If you want to use bot, please reach out to me on Telegram (@mirsaidAI) or through LinkedIn.

### Dataset
Context
Pneumonia is an infection that inflames the air sacs in one or both lungs. It kills more children younger than 5 years old each year than any other infectious disease, such as HIV infection, malaria, or tuberculosis. Diagnosis is often based on symptoms and physical examination. Chest X-rays may help confirm the diagnosis.

Content
This dataset contains 5,856 validated Chest X-Ray images. Images are labeled as (disease:NORMAL/BACTERIA/VIRUS)-(randomized patient ID)-(image number of a patient). For details of the data collection and description, see the referenced paper below.

According to the paper, the images (anterior-posterior) were selected from retrospective cohorts of pediatric patients of one to five years old from Guangzhou Women and Children’s Medical Center, Guangzhou.
