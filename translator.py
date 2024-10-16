import speech_recognition as sr
from transformers import MarianMTModel, MarianTokenizer

# Mapping of language names to their codes
language_map = {
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Italian': 'it',
    'Portuguese': 'pt',
    'Chinese': 'zh',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Russian': 'ru',
    'Dutch': 'nl',
    'Swedish': 'sv',
    'Danish': 'da',
    'Norwegian': 'no',
    'Finnish': 'fi',
    'Turkish': 'tr',
    'Arabic': 'ar',
    'Hindi': 'hi',
    'Bengali': 'bn',
    'Vietnamese': 'vi',
    'Thai': 'th',
    # Add more languages as needed
}

def translate(text, target_language):
    if target_language not in language_map:
        raise ValueError(f"Unsupported language: {target_language}")
    
    language_code = language_map[target_language]
    model_name = f'Helsinki-NLP/opus-mt-en-{language_code}'
    
    # Load the tokenizer and model
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)

    # Tokenize the input text
    tokenized_text = tokenizer(text, return_tensors='pt', padding=True)

    # Perform the translation
    translated_tokens = model.generate(**tokenized_text)

    # Decode the translated tokens
    translated_text = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
    return translated_text

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please speak the text you want to translate...")
        audio = recognizer.listen(source)
    
    try:
        # Convert speech to text
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

if __name__ == "__main__":
    # Recognize speech for text to translate
    text_to_translate = recognize_speech()
    if text_to_translate is not None:
        target_language = input("Enter target language (e.g., 'Spanish', 'French', etc.): ")
        
        try:
            translated_text = translate(text_to_translate, target_language)
            print(f"Translated text: {translated_text}")
        except Exception as e:
            print(f"An error occurred: {e}")

