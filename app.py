import streamlit as st
import joblib
from lime.lime_text import LimeTextExplainer
import tensorflow as tf
import numpy as np

# Load your trained models
ml_model = joblib.load('models/ml_model.joblib')
nlp_model = tf.keras.models.load_model('models/nlp_model')

# Assuming these are your class names
class_names = ['High Rating', 'Neutral Rating', 'Low Rating']  # Adjust these as necessary

def predict_and_explain(text, model, vectorizer=None):
    processed_text = [text]  # Ensuring the input is iterable
    prediction = model.predict(processed_text)

    # Generate LIME explanation for ML model
    if vectorizer:
        explainer = LimeTextExplainer(class_names=class_names)
        exp = explainer.explain_instance(text, model.predict_proba, num_features=10)
        return prediction, exp
    return prediction, None

st.title("Text Review Classification App")

user_input = st.text_area("Enter your review text here:")

model_option = st.selectbox("Select a model to use:", ("Machine Learning Model", "Deep NLP Model"))

if st.button('Predict'):
    if model_option == "Machine Learning Model":
        prediction, exp = predict_and_explain(user_input, ml_model)
        st.write(f"Predicted Class: {class_names[np.argmax(prediction)]}")
        if exp:
            st.markdown(exp.as_html(), unsafe_allow_html=True)
    else:
        prediction = nlp_model.predict([user_input])
        predicted_class = class_names[np.argmax(prediction)]
        st.write(f"Predicted Class: {predicted_class}")
        st.write("Class probabilities:")
        for name, prob in zip(class_names, prediction[0]):
            st.write(f"{name}: {prob:.4f}")

# Optional: Include functionality to load and display training/test data
if st.checkbox("Show training data"):
    X_train, y_train = joblib.load('data/training_data.joblib')
    st.write(X_train)

if st.checkbox("Show test data"):
    X_test, y_test = joblib.load('data/testing_data.joblib')
    st.write(X_test)
