import telebot
from fastai.vision.all import *
from io import BytesIO
from PIL import Image
from telebot import types
import pathlib

# Temporary fix for pathlib.PosixPath on Windows
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

# Initialize the Telegram bot
bot = telebot.TeleBot('6206650641:AAF1HQt0PdJDV-r0-3ihbkKrWwHpYg8AwRU')

# Load the Fastai Learner model
learn = load_learner('model.pkl')

# Define language constants
UZBEK = 'uz'
ENGLISH = 'en'
RUSSIAN = 'ru'

uz_welcome='''- Assalomu alaykum, Men dasturchi Abdrurasulov Mirsaid tomonidan tarbiyalangan sun'iy intellektman. 

- Bemorning o'pka rengin rasmiga qarab, bemorda o'pka yallig'lanishi bor yoki yo'q ekanligini aniqlab beraman.

- Mening aniqliligim 98 %. Men tarbiyalangan rasmlar,  malakalik shifokorlar tomonidan ko'rib chiqilgan va tasdiqlangan.

- Muhim: Men test rejimida ishlamoqdaman, iltimos, menga ishonib hulosa qilmang, malakalik shifokorga murojat qiling.

Boshlash uchun, iltimos bemor o'pkasining rengin rasmini yuboring. Muhim: rasm ko'rinishida, file emas.'''

en_welcome='''- Hello, I am a trained artificial intelligence by developer Abdurasulov Mirsaid.

- Looking at the picture of the patient's lungs, I can determine whether the patient has pneumonia or not.

- My model accuracy is 98 %. I was trained with pictures, carefully reviewed and approved by professional doctors.

- Important: I am working in test mode, please do not have a conclusion based on my responce, consult a qualified doctor.

To begin, please send the XRay image of the patient's lungs. Note: as a picture, not a file. '''

rus_welcome='''- Здравствуйте, я обученный искусственный интеллект от разработчика Мирсаидa.

- Глядя на снимок легких больного, я могу определить, есть ли у больного туберкулез или нет.

- У меня действительно высокая точность (98 %). Меня обучали фотографиям, тщательно просмотренным и одобренным профессиональными врачами.

- Важно: я работаю в тестовом режиме, пожалуйста, не делайте вывод по моему ответу, обратитесь к квалифицированному врачу. 

Для начала отправьте рентгеновский снимок легких пациента. Примечание: как изображение, а не файл.'''


# Define welcome messages
WELCOME_MESSAGES = {
    UZBEK: uz_welcome,
    ENGLISH: en_welcome,
    RUSSIAN: rus_welcome,
}

user_data = {}

# Handler function for the language selection buttons
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Create the keyboard markup with the language selection buttons
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(
        types.KeyboardButton(text='🇺🇿 O\'zbek'),
        types.KeyboardButton(text='🇬🇧 English'),
        types.KeyboardButton(text='🇷🇺 Русский')
    )
    
    # Send the welcome message with the language selection buttons
    msg = bot.send_message(message.chat.id, 'Tilni tanlang / Please select your language / Выберите язык', reply_markup=markup)
    
    # Store the selected language in the user data for future use
    bot.register_next_step_handler(msg, process_language_selection)

# Handler function for processing the language selection
def process_language_selection(message):
    try:
        # Get the selected language from the button text
        flag_emoji, language_name = message.text.split()
        selected_language = {
            '🇺🇿': UZBEK,
            '🇬🇧': ENGLISH,
            '🇷🇺': RUSSIAN
        }[flag_emoji]

        # Store the selected language in the user data for future use
        user_data[message.chat.id] = {'language': selected_language}

        # Send the welcome message in the selected language
        welcome_message = WELCOME_MESSAGES[selected_language]
        markup = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(message.chat.id, welcome_message, reply_markup=markup)
    except:
        # If an error occurs, ask the user to select a language
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(
            types.KeyboardButton(text='🇺🇿 O\'zbek'),
            types.KeyboardButton(text='🇬🇧 English'),
            types.KeyboardButton(text='🇷🇺 Русский')
        )
        msg = bot.send_message(message.chat.id, 'Tilni tanlang / Please select your language / Выберите язык', reply_markup=markup)
        bot.register_next_step_handler(msg, process_language_selection)


# Define the message handler
@bot.message_handler(content_types=['photo'])
def handle_image(message):
    try:
        # Get the image file ID
        file_id = message.photo[-1].file_id

        # Download the image
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Convert the image to PIL format
        img = Image.open(BytesIO(downloaded_file))

        if img is None:
            bot.reply_to(message, "Error: Unable to open the image.")
            return

        # Handle different image formats
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # Resize image to match model input shape
        img = img.resize((224, 224))

        # Convert the image to a Fastai Image object
        img_fastai = Image.fromarray(np.array(img))

        # Make a prediction
        pred, pred_id, probs = learn.predict(img_fastai)
        
        CLASS_NAMES = {
        UZBEK: {
        'healthy': f"Sog'lom, Ehtimollik: {probs[pred_id]*100:.1f}%",
        'sick': f'Bemorda pnevnomaniya mavjud,  Ehtimollik: {probs[pred_id]*100:.1f}%',
        },
        ENGLISH: {
        'healthy': f"Healthy, Probability: {probs[pred_id]*100:.1f}%",
        'sick': f'The patient has pneumonia, Probability: {probs[pred_id]*100:.1f}%',
        },
        RUSSIAN: {
        'healthy': f"Здоровый, Bероятность: {probs[pred_id]*100:.1f}%",
        'sick': f"У пневмония, Bероятность: {probs[pred_id]*100:.1f}%"
        },
        }
        
        bot.send_chat_action(message.chat.id, 'typing')
        selected_language = user_data[message.chat.id]['language']
        class_names = CLASS_NAMES[selected_language]
        
        if pred == 'NORMAL':
            class_name = class_names['healthy']
        else:
            class_name = class_names['sick']

        bot.reply_to(message, class_name)

    except Exception as e:
        errors = {
            ENGLISH : """Please send only x-ray pictures in clear format because it may affect result. Apart from this bot may not recognise picture. Try again""",
            UZBEK : """Iltimos, faqat rentgen rasmlarini tiniq qilib yuboring, chunki bu natijaga ta'sir qilishi mumkin. Bundan tashqari, bot rasmni tanimasligi mumkin. Qayta urinib ko'ring""",
            RUSSIAN : """Пожалуйста, присылайте только четкие рентгеновские снимки, поскольку это может повлиять на результат. Также бот может не распознать изображение. Попробуйте еще раз"""
        }
        bot.reply_to(message, errors[selected_language])
# Polling to keep the bot alive
bot.polling()


