import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from states import Form
from handlers.admin_handler import REGION_BRANCHES
from utils.vacancy_manager import get_vacancies

FIELD_LABELS = {
    "name": {"en": "Name", "uz": "Ism", "ru": "Имя"},
    "phone": {"en": "Phone", "uz": "Telefon raqam", "ru": "Телефон"},
    "region": {"en": "Region", "uz": "Hudud", "ru": "Регион"},
    "branch": {"en": "Branch", "uz": "Filial", "ru": "Филиал"},
    "vacancy": {"en": "Vacancy", "uz": "Bo‘sh ish o‘rni", "ru": "Вакансия"},
    "bio": {"en": "Bio", "uz": "Biografiya", "ru": "Биография"},
    "birth_date": {"en": "Birth Date", "uz": "Tug‘ilgan sana", "ru": "Дата рождения"},
    "live_place": {"en": "Living Place", "uz": "Yashash joyi", "ru": "Место жительства"},
    "languages": {"en": "Languages", "uz": "Tillar", "ru": "Языки"},
    "software": {"en": "Software", "uz": "Dasturlar", "ru": "Программы"},
    "family": {"en": "Family", "uz": "Oila", "ru": "Семья"},
    "last_work": {"en": "Last Work", "uz": "Oxirgi ish", "ru": "Последнее место работы"},
    "leave_reason": {"en": "Reason for Leaving", "uz": "Ketish sababi", "ru": "Причина ухода"},
    "interest": {"en": "Interest", "uz": "Qiziqish", "ru": "Интерес"},
    "source": {"en": "Source", "uz": "Manba", "ru": "Источник"},
    "personality": {"en": "Personality", "uz": "Shaxsiy fazilatlar", "ru": "Личность"},
    "books": {"en": "Books", "uz": "Kitoblar", "ru": "Книги"},
    "achievements": {"en": "Achievements", "uz": "Yutuqlar", "ru": "Достижения"},
    "position": {"en": "Desired Position", "uz": "Istalgan lavozim", "ru": "Желаемая должность"},
    "application_preview": {"en": "Application Preview","uz": "Ariza ko‘rinishi","ru": "Предпросмотр анкеты"},
    "application_received": {"en": "New Application Received", "uz": "Yangi ariza qabul qilindi","ru": "Получена новая анкета"},
    "time": {"en": "Available Time", "uz": "Ish vaqti", "ru": "Время работы"}
}


REGIONS = {
    "en": ["Tashkent", "Samarkand", "Bukhara", "Andijan", "Fergana", "Namangan", "Khorezm", "Karakalpakstan", "Jizzakh", "Navoi", "Kashkadarya", "Surkhandarya", "Sirdarya", "Tashkent Region"],
    "uz": ["Toshkent", "Samarqand", "Buxoro", "Andijon", "Farg‘ona", "Namangan", "Xorazm", "Qoraqalpog‘iston", "Jizzax", "Navoiy", "Qashqadaryo", "Surxondaryo", "Sirdaryo", "Toshkent viloyati"],
    "ru": ["Ташкент", "Самарканд", "Бухара", "Андижан", "Фергана", "Наманган", "Хорезм", "Каракалпакстан", "Джизак", "Навои", "Кашкадарья", "Сурхандарья", "Сырдарья", "Ташкентская область"]
}

REGION_BRANCHES = {
    "Tashkent": [
        {
            "title": {
                "en": "Main Office Tashkent",
                "uz": "Toshkent Bosh Ofisi",
                "ru": "Главный офис Ташкента"
            },
            "description": {
                "en": "Head HR Office located in central Tashkent.",
                "uz": "Toshkent markazida joylashgan bosh HR ofisi.",
                "ru": "Главный HR офис в центре Ташкента."
            },
            "photo_url": "https://repost.uz/storage/uploads/887-1679714908-portal-post-material.jpeg",
            "location": {"latitude": 41.3111, "longitude": 69.2797}
        },
        {
            "title": {
                "en": "Yunusabad Branch",
                "uz": "Yunusobod Filiali",
                "ru": "Филиал в Юнусабаде"
            },
            "description": {
                "en": "Located in Yunusabad district for local HR support.",
                "uz": "Yunusobod tumanida joylashgan mahalliy HR filiali.",
                "ru": "Расположен в Юнусабадском районе для HR-поддержки."
            },
            "photo_url": "https://yunsc.uz/uzb/assets/images/gallery-19-1600x1067.jpg",
            "location": {"latitude": 41.3457, "longitude": 69.2849}
        }
    ],
    "Samarkand": [
        {
            "title": {
                "en": "Samarkand HR Branch",
                "uz": "Samarqand HR Filiali",
                "ru": "Самаркандский HR филиал"
            },
            "description": {
                "en": "Regional office for HR interviews in Samarkand.",
                "uz": "Samarqanddagi HR suhbatlari uchun mintaqaviy ofis.",
                "ru": "Региональный офис для HR-собеседований в Самарканде."
            },
            "photo_url": "https://ziyoratga.uz/media/regions/samarkandskaya_oblast/gorod_samarkand/imgonline-com-ua-exifeditxP4UkfZXBsdP.jpg",
            "location": {"latitude": 39.6585, "longitude": 66.9603}
        },
        {
            "title": {
                "en": "University Campus Branch",
                "uz": "Universitet Shaharchasi Filiali",
                "ru": "Филиал в университетском городке"
            },
            "description": {
                "en": "HR office located near the university campus.",
                "uz": "Universitet shaharchasi yaqinida joylashgan HR ofisi.",
                "ru": "HR-офис, расположенный рядом с университетским городком."
            },
            "photo_url": "https://example.com/photo4.jpg",
            "location": {"latitude": 39.6200, "longitude": 66.9650}
        }
    ],
    "Bukhara": [
        {
            "title": {
                "en": "Bukhara HR Branch",
                "uz": "Buxoro HR Filiali",
                "ru": "Бухарский HR филиал"
            },
            "description": {
                "en": "Regional office for HR interviews in Bukhara.",
                "uz": "Buxorodagi HR suhbatlari uchun mintaqaviy ofis.",
                "ru": "Региональный офис для HR-собеседований в Бухаре."
            },
            "photo_url": "https://upload.wikimedia.org/wikipedia/commons/9/99/Sample_User_Icon.png",
            "location": {"latitude": 40.6270, "longitude": 65.9749}
        },
        {
            "title": {
                "en": "University Campus Branch",
                "uz": "Universitet Shaharchasi Filiali",
                "ru": "Филиал в университетском городке"
            },
            "description": {
                "en": "HR office located near the university campus.",
                "uz": "Universitet shaharchasi yaqinida joylashgan HR ofisi.",
                "ru": "HR-офис, расположенный рядом с университетским городком."
            },
            "photo_url": "https://example.com/photo4.jpg",
            "location": {"latitude": 37.6500, "longitude": 65.9643}
        }
    ]
}


LANGUAGES = {
    "en": "English 🇬🇧",
    "uz": "O‘zbek 🇺🇿",
    "ru": "Русский 🇷🇺"
}

WELCOME_MESSAGES = {
    "en": "Welcome to the HR Application Bot!",
    "uz": "HR botiga xush kelibsiz!",
    "ru": "Добро пожаловать в HR бот!"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(text, callback_data=f"lang_{code}")]
        for code, text in LANGUAGES.items()
    ]
    await update.message.reply_text(
        "Please select your language / Iltimos tilni tanlang / Пожалуйста, выберите язык:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return Form.LANGUAGE


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Operation cancelled. To start again, send /start")
    context.user_data.clear()
    return ConversationHandler.END

async def select_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang_code = query.data.split("_")[1]
    context.user_data["lang"] = lang_code
    await query.edit_message_text(WELCOME_MESSAGES[lang_code])

    # Show region selection
    return await show_main_menu(update, context)

async def handle_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get("lang", "en")
    option = query.data.replace("menu_", "")

    if option == "back":
        return await show_main_menu(update, context)

    if option == "vacancies":
        return await show_regions(update, context, next_action="vacancy")

    elif option == "branches":
        return await show_regions(update, context, next_action="branchinfo")

    # Content dictionary
    content = {
        "about": {
            "en": "🧑‍💼 We are a leading HR company in Uzbekistan, committed to connecting talented individuals with top employers. Our mission is to streamline the recruitment process, ensuring the best fit for both candidates and companies. 🌟",
            "uz": "🧑‍💼 Biz O‘zbekistondagi yetakchi HR kompaniyamiz, iste’dodli insonlarni eng yaxshi ish beruvchilar bilan bog‘lashga sodiqmiz. Bizning maqsadimiz ishga qabul qilish jarayonini soddalashtirish, nomzodlar va kompaniyalar uchun eng yaxshi moslikni ta’minlash. 🌟",
            "ru": "🧑‍💼 Мы ведущая HR-компания в Узбекистане, стремящаяся связать талантливых людей с ведущими работодателями. Наша миссия — упростить процесс набора сотрудников, обеспечив наилучшее соответствие для кандидатов и компаний. 🌟"
        },
        "branches": {
            "en": "🏢 We have branches in major cities...",
            "uz": "🏢 Bizning filiallarimiz yirik shaharlarda joylashgan...",
            "ru": "🏢 У нас есть филиалы в крупных городах..."
        },
        "contacts": {
            "en": "📞 Have questions?\nReach out to us at\n📧 hr@example.com\n📱 +998 90 123 45 67",
            "uz": "📞 Savollar bormi?\nBiz bilan bog‘laning:\n📧 hr@example.com\n📱 +998 90 123 45 67",
            "ru": "📞 Есть вопросы?\nСвяжитесь с нами по:\n📧 hr@example.com\n📱 +998 90 123 45 67"
        }

    }
    #"about": "https://havepakken.dk/cdn/shop/products/Untitled.png",
    images = {
        "about": "https://drive.google.com/file/d/1ZL0gkRriiG1ZIl_aQ6_78QauKksshOHa/view?usp=drivesdk",
        "branches": "https://upload.wikimedia.org/wikipedia/commons/b/b6/Image_created_with_a_mobile_phone.png",
        "contacts": "https://gilb.com.np/wp-content/uploads/2024/02/Contact-us.jpg"
    }

    text = content.get(option, {}).get(lang)
    image_url = images.get(option)

    back_button = [[
        InlineKeyboardButton(
            {"en": "🔙 Back", "uz": "🔙 Orqaga", "ru": "🔙 Назад"}[lang], callback_data="menu_back"
        )
    ]]

    if text and image_url:
        await query.message.chat.send_photo(
            photo=image_url,
            caption=text,
            reply_markup=InlineKeyboardMarkup(back_button)
        )
    else:
        await query.edit_message_text(
            text="ℹ️ No information available.",
            reply_markup=InlineKeyboardMarkup(back_button)
        )

    return Form.LANGUAGE




async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")

    keyboard = [
        [InlineKeyboardButton({"en": "🏢 About Company", "uz": "🏢 Kompaniya haqida", "ru": "🏢 О компании"}[lang],
                              callback_data="menu_about")],
        [InlineKeyboardButton({"en": "📍 Branches", "uz": "📍 Filiallar", "ru": "📍 Филиалы"}[lang],
                              callback_data="menu_branches")],
        [InlineKeyboardButton({"en": "💼 Vacancies", "uz": "💼 Bo‘sh ish o‘rinlari", "ru": "💼 Вакансии"}[lang],
                              callback_data="menu_vacancies")],
        [InlineKeyboardButton({"en": "☎️ Contacts", "uz": "☎️ Kontaktlar", "ru": "☎️ Контакты"}[lang],
                              callback_data="menu_contacts")]
    ]

    text = {
        "en": "🏠 Main Menu:",
        "uz": "🏠 Asosiy menyu:",
        "ru": "🏠 Главное меню:"
    }[lang]

    try:
        if update.callback_query:
            await update.callback_query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    except telegram.error.BadRequest as e:
        # fallback to send_message if message was photo/location
        await update.callback_query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    return Form.LANGUAGE



async def show_regions(update: Update, context: ContextTypes.DEFAULT_TYPE, next_action="vacancy"):
    context.user_data["next_action"] = next_action
    lang = context.user_data.get("lang", "en")
    region_buttons = [[InlineKeyboardButton(region, callback_data=f"region_{region}")] for region in REGIONS[lang]]
    await update.callback_query.edit_message_text(
        text={
            "en": "Please select your region:",
            "uz": "Iltimos, hududingizni tanlang:",
            "ru": "Пожалуйста, выберите ваш регион:"
        }[lang],
        reply_markup=InlineKeyboardMarkup(region_buttons)
    )
    return Form.REGION

async def select_region(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get("lang", "en")

    region_name_localized = query.data.replace("region_", "")
    region_key = get_region_key(region_name_localized, lang)  # 🔁 convert to English key
    context.user_data["region"] = region_key  # ✅ use English region key always

    if context.user_data.get("next_action") == "branchinfo":
        return await show_branches_info(update, context)
    else:
        return await show_branches(update, context)


async def select_branch_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get("lang", "en")
    branch_index = int(query.data.split("_")[1])
    branch = context.user_data["branches"][branch_index]

    # Show photo and description
    await query.message.chat.send_photo(
        photo=branch["photo_url"],
        caption=f"📄 {branch['title'][lang]}\n\n{branch['description'][lang]}"
    )

    # Show location
    await query.message.chat.send_location(
        latitude=branch["location"]["latitude"],
        longitude=branch["location"]["longitude"]
    )

    # Back to region selection
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="menu_branches")]]
    await query.message.reply_text({
        "en": "🔙 Back to branch list",
        "uz": "🔙 Filiallar ro‘yxatiga qaytish",
        "ru": "🔙 Назад к списку филиалов"
    }[lang], reply_markup=InlineKeyboardMarkup(keyboard))

    return Form.LANGUAGE


async def show_branches_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")
    query = update.callback_query
    await query.answer()

    selected_region = context.user_data.get("region")
    region_key = get_region_key(selected_region, lang)  # ✅ fixed mapping
    branches = REGION_BRANCHES.get(region_key, [])

    if not branches:
        await query.edit_message_text({
            "en": "🚫 No branches found for this region.",
            "uz": "🚫 Bu hudud uchun filiallar topilmadi.",
            "ru": "🚫 В этом регионе филиалов не найдено."
        }[lang])
        return ConversationHandler.END

    buttons = [
        [InlineKeyboardButton(branch["title"][lang], callback_data=f"branchinfo_{i}")]
        for i, branch in enumerate(branches)
    ]
    buttons.append([InlineKeyboardButton("🔙 Back", callback_data="menu_back")])

    await query.edit_message_text(
        text={
            "en": "🏢 Select a branch to view details:",
            "uz": "🏢 Filialni tanlang (ma’lumot uchun):",
            "ru": "🏢 Выберите филиал, чтобы посмотреть информацию:"
        }[lang],
        reply_markup=InlineKeyboardMarkup(buttons)
    )

    context.user_data["branches"] = branches
    return Form.BRANCH



async def show_branches(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")
    query = update.callback_query
    await query.answer()

    selected_region = context.user_data.get("region")
    region_key = get_region_key(selected_region, lang)  # ✅ fix here

    branches = REGION_BRANCHES.get(region_key, [])
    if not branches:
        await query.edit_message_text({
            "en": "🚫 No branches found for this region.",
            "uz": "🚫 Bu hudud uchun filiallar topilmadi.",
            "ru": "🚫 В этом регионе филиалов не найдено."
        }[lang])
        return ConversationHandler.END

    buttons = [[InlineKeyboardButton(branch["title"][lang], callback_data=f"branch_{i}")]
               for i, branch in enumerate(branches)]
    await query.edit_message_text(
        {
            "en": "Select a branch:",
            "uz": "Filialni tanlang:",
            "ru": "Выберите филиал:"
        }[lang],
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    context.user_data["branches"] = branches
    return Form.BRANCH


def get_region_key(user_region: str, lang: str) -> str:
    """Map localized region name back to English key used in REGION_BRANCHES"""
    for i, region in enumerate(REGIONS[lang]):
        if region == user_region:
            return REGIONS["en"][i]
    return user_region  # fallback


async def select_branch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get("lang", "en")
    branch_index = int(query.data.split("_")[1])
    branch = context.user_data["branches"][branch_index]
    context.user_data["selected_branch"] = branch


    # Send photo
    # await query.message.delete()
    await update.callback_query.message.chat.send_photo(
        photo=branch["photo_url"],
        caption = f"📄 {branch['title'][lang]}\n\n{branch['description'][lang]}"
    )

    # Send location
    await update.callback_query.message.chat.send_location(
        latitude=branch["location"]["latitude"],
        longitude=branch["location"]["longitude"]
    )

    # Show apply button
    # Show apply button
    keyboard = [[InlineKeyboardButton({
          "en": "Apply to this branch",
          "uz": "Ushbu filialga ariza berish",
          "ru": "Подать заявку в этот филиал"
      }[lang], callback_data="apply_branch")]]

    await update.callback_query.message.chat.send_message(
        text={
            "en": "Would you like to apply?",
            "uz": "Ariza bermoqchimisiz?",
            "ru": "Хотите подать заявку?"
        }[lang],
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    return Form.VACANCY


async def show_vacancies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get("lang", "en")
    branch = context.user_data["selected_branch"]
    region = context.user_data["region"]
    branch_title = branch["title"]["en"]
    vacancies = get_vacancies(region, branch_title)

    if not vacancies:
        await query.message.edit_text({
            "en": "🚫 No vacancies available at this branch.",
            "uz": "🚫 Ushbu filialda bo‘sh ish o‘rinlari yo‘q.",
            "ru": "🚫 В этом филиале нет вакансий."
        }[lang])
        return ConversationHandler.END

    buttons = [
        [InlineKeyboardButton(vacancy.get(lang, str(vacancy)), callback_data=f"vacancy_{i}")]
        for i, vacancy in enumerate(vacancies)
    ]

    await query.message.edit_text(
        {
            "en": "Please select a vacancy:",
            "uz": "Bo‘sh ish o‘rnini tanlang:",
            "ru": "Выберите вакансию:"
        }[lang],
        reply_markup=InlineKeyboardMarkup(buttons)
    )

    context.user_data["vacancies"] = vacancies
    return Form.VACANCY


async def select_vacancy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get("lang", "en")
    vacancy_index = int(query.data.split("_")[1])
    selected_vacancy = context.user_data["vacancies"][vacancy_index]
    context.user_data["selected_vacancy"] = selected_vacancy

    await query.edit_message_text(
        {
            "en": f"✅ You selected: {selected_vacancy['en']}\nLet's begin your application...",
            "uz": f"✅ Siz tanladingiz: {selected_vacancy['uz']}\nKeling, arizangizni to‘ldirishni boshlaymiz...",
            "ru": f"✅ Вы выбрали: {selected_vacancy['ru']}\nНачнем оформление заявки..."
        }[lang]
    )

    # Next: Ask for phone number
    return await ask_phone(update, context)



from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

async def ask_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")

    contact_button = KeyboardButton(
        text={
            "en": "📞 Share Phone Number",
            "uz": "📞 Telefon raqamni yuborish",
            "ru": "📞 Отправить номер телефона"
        }[lang],
        request_contact=True
    )

    reply_markup = ReplyKeyboardMarkup([[contact_button]], resize_keyboard=True, one_time_keyboard=True)

    await update.callback_query.message.reply_text(
        {
            "en": "Please share your phone number:",
            "uz": "Iltimos, telefon raqamingizni yuboring:",
            "ru": "Пожалуйста, отправьте ваш номер телефона:"
        }[lang],
        reply_markup=reply_markup
    )
    return Form.PHONE


async def save_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")

    contact = update.message.contact
    if not contact:
        await update.message.reply_text(
            {
                "en": "Please use the button to share your phone number.",
                "uz": "Iltimos, raqamni yuborish tugmasidan foydalaning.",
                "ru": "Пожалуйста, используйте кнопку для отправки номера."
            }[lang]
        )
        return Form.PHONE

    context.user_data["phone"] = contact.phone_number

    await update.message.reply_text(
        {
            "en": "✅ Phone number received. Now write a short biography about yourself:",
            "uz": "✅ Telefon raqamingiz qabul qilindi. Endi o‘zingiz haqingizda qisqacha yozing:",
            "ru": "✅ Номер получен. Теперь напишите кратко о себе:"
        }[lang],
        reply_markup=ReplyKeyboardRemove()
    )
    return Form.BIO


async def save_bio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")
    bio = update.message.text.strip()

    context.user_data["bio"] = bio

    await update.message.reply_text(
        {
            "en": "📅 Now enter your birth date (e.g. 02.01.1998):",
            "uz": "📅 Tug‘ilgan sanangizni kiriting (masalan: 02.01.1998):",
            "ru": "📅 Введите вашу дату рождения (например: 02.01.1998):"
        }[lang]
    )
    return Form.BIRTH_DATE


import re

async def save_birth_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")
    birth_date = update.message.text.strip()

    if not re.match(r"\d{2}.\d{2}.\d{4}", birth_date):
        await update.message.reply_text(
            {
                "en": "❗ Invalid format. Please enter as DD.MM.YYYY.",
                "uz": "❗ Noto‘g‘ri format. Iltimos, DD.MM.YYYY shaklida kiriting.",
                "ru": "❗ Неверный формат. Введите в формате ДД.ММ.ГГГГ."
            }[lang]
        )
        return Form.BIRTH_DATE

    context.user_data["birth_date"] = birth_date

    await update.message.reply_text(
        {
            "en": "🏠 Where do you currently live?",
            "uz": "🏠 Hozir qayerda yashaysiz?",
            "ru": "🏠 Где вы сейчас живете?"
        }[lang]
    )
    return Form.LIVE_PLACE

async def save_live_place(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")
    context.user_data["live_place"] = update.message.text.strip()

    await update.message.reply_text({
        "en": "🌐 Which languages do you speak?",
        "uz": "🌐 Qaysi tillarni bilasiz?",
        "ru": "🌐 На каких языках вы говорите?"
    }[lang])
    return Form.LANGUAGES


async def save_languages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")
    context.user_data["languages"] = update.message.text.strip()

    await update.message.reply_text({
        "en": "🖥️ Which software can you use? (e.g., Excel, Word, 1C)",
        "uz": "🖥️ Qaysi dasturlar bilan ishlay olasiz? (masalan: Excel, Word, 1C)",
        "ru": "🖥️ Какими программами вы владеете? (например: Excel, Word, 1C)"
    }[lang])
    return Form.SOFTWARE


async def save_software(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")
    context.user_data["software"] = update.message.text.strip()

    await update.message.reply_text({
        "en": "👨‍👩‍👧 Tell us about your family:",
        "uz": "👨‍👩‍👧 Oilangiz haqida ma'lumot bering:",
        "ru": "👨‍👩‍👧 Расскажите о своей семье:"
    }[lang])
    return Form.FAMILY


async def save_family(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")
    context.user_data["family"] = update.message.text.strip()

    await update.message.reply_text({
        "en": "🏢 Where did you last work?",
        "uz": "🏢 Oxirgi ishlagan joyingiz qayerda?",
        "ru": "🏢 Где вы работали ранее?"
    }[lang])
    return Form.LAST_WORK


async def save_last_work(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")
    context.user_data["last_work"] = update.message.text.strip()

    await update.message.reply_text({
        "en": "❓ Why did you leave your last job?",
        "uz": "❓ Nima sababdan oxirgi ish joyingizdan ketdingiz?",
        "ru": "❓ Почему вы покинули предыдущее место работы?"
    }[lang])
    return Form.LEAVE_REASON

async def save_leave_reason(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")
    context.user_data["leave_reason"] = update.message.text.strip()

    await update.message.reply_text({
        "en": "🎯 Why are you interested in this vacancy?",
        "uz": "🎯 Nega aynan ushbu bo‘sh ish o‘rni sizni qiziqtirdi?",
        "ru": "🎯 Почему вас заинтересовала эта вакансия?"
    }[lang])
    return Form.INTEREST


async def save_interest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")
    context.user_data["interest"] = update.message.text.strip()

    await update.message.reply_text({
        "en": "📢 Where did you hear about this vacancy?",
        "uz": "📢 Ushbu bo‘sh ish o‘rni haqida qayerdan bildingiz?",
        "ru": "📢 Где вы узнали об этой вакансии?"
    }[lang])
    return Form.SOURCE


async def save_source(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")
    context.user_data["source"] = update.message.text.strip()

    await update.message.reply_text({
        "en": "👤 Describe your personality and personal traits:",
        "uz": "👤 Xarakteringiz va shaxsiy fazilatlaringiz haqida yozing:",
        "ru": "👤 Расскажите о вашем характере и личных качествах:"
    }[lang])
    return Form.PERSONALITY



async def save_personality(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")
    context.user_data["personality"] = update.message.text.strip()

    await update.message.reply_text({
        "en": "📚 What books have you read recently?",
        "uz": "📚 Yaqinda qanday kitoblarni o‘qidingiz?",
        "ru": "📚 Какие книги вы читали недавно?"
    }[lang])
    return Form.BOOKS


async def save_books(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")
    context.user_data["books"] = update.message.text.strip()

    await update.message.reply_text({
        "en": "🏅 Please describe your achievements:",
        "uz": "🏅 Erishgan yutuqlaringiz haqida yozing:",
        "ru": "🏅 Опишите свои достижения:"
    }[lang])
    return Form.ACHIEVEMENTS


async def save_achievements(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")
    context.user_data["achievements"] = update.message.text.strip()

    await update.message.reply_text({
        "en": "🧑‍💼 Which position are you applying for?",
        "uz": "🧑‍💼 Qaysi lavozimga ariza bermoqchisiz?",
        "ru": "🧑‍💼 На какую должность вы подаете заявку?"
    }[lang])
    return Form.POSITION

async def save_position(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")
    context.user_data["position"] = update.message.text.strip()

    await update.message.reply_text({
        "en": "⏰ What time can you work? (e.g., 09:00–18:00)",
        "uz": "⏰ Qaysi vaqtlarda ishlay olasiz? (masalan: 09:00–18:00)",
        "ru": "⏰ В какое время вы можете работать? (например: 09:00–18:00)"
    }[lang])
    return Form.TIME



async def save_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")
    context.user_data["time"] = update.message.text.strip()

    await update.message.reply_text({
        "en": "📸 Please upload your photo for the application (send as a photo):",
        "uz": "📸 Iltimos, ariza uchun surat yuboring (rasm sifatida jo‘nating):",
        "ru": "📸 Пожалуйста, отправьте свое фото для анкеты (как фотографию):"
    }[lang])
    return Form.PHOTO  # ✅ wait for photo next



from config import GROUP_ID

def t(key, lang):
    return FIELD_LABELS.get(key, {}).get(lang, key)

async def save_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")

    if not update.message.photo:
        await update.message.reply_text({
            "en": "❗ Please send a valid photo.",
            "uz": "❗ Iltimos, haqiqiy rasm yuboring.",
            "ru": "❗ Пожалуйста, отправьте действительное фото."
        }[lang])
        return Form.PHOTO  # Stay in same state

    photo_file_id = update.message.photo[-1].file_id
    context.user_data["photo"] = photo_file_id
    user = update.message.from_user
    context.user_data["name"] = user.full_name

    data = context.user_data

    summary = f"""
*{t('application_preview', lang)}*

👤 *{t('name', lang)}*: {data.get("name")}
📞 *{t('phone', lang)}*: {data.get("phone")}
📍 *{t('region', lang)}*: {data.get("region")}
🏢 *{t('branch', lang)}*: {data.get("selected_branch", {}).get("title", {}).get(lang, "")}
📌 *{t('vacancy', lang)}*: {data.get("selected_vacancy", {}).get(lang, "")}
📖 *{t('bio', lang)}*: {data.get("bio")}
🎂 *{t('birth_date', lang)}*: {data.get("birth_date")}
🏠 *{t('live_place', lang)}*: {data.get("live_place")}
🌐 *{t('languages', lang)}*: {data.get("languages")}
🖥 *{t('software', lang)}*: {data.get("software")}
👨‍👩‍👧 *{t('family', lang)}*: {data.get("family")}
🏢 *{t('last_work', lang)}*: {data.get("last_work")}
❌ *{t('leave_reason', lang)}*: {data.get("leave_reason")}
🎯 *{t('interest', lang)}*: {data.get("interest")}
📢 *{t('source', lang)}*: {data.get("source")}
👤 *{t('personality', lang)}*: {data.get("personality")}
📚 *{t('books', lang)}*: {data.get("books")}
🏅 *{t('achievements', lang)}*: {data.get("achievements")}
💼 *{t('position', lang)}*: {data.get("position")}
⏰ *{t('time', lang)}*: {data.get("time")}
""".strip()

    keyboard = [
        [
            InlineKeyboardButton({"en": "✅ Submit", "uz": "✅ Yuborish", "ru": "✅ Отправить"}[lang], callback_data="confirm_submit"),
            InlineKeyboardButton({"en": "❌ Cancel", "uz": "❌ Bekor qilish", "ru": "❌ Отменить"}[lang], callback_data="confirm_cancel")
        ]
    ]

    await update.message.reply_photo(
        photo=photo_file_id,
        caption=summary,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    return Form.CONFIRM


async def confirm_application(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get("lang", "en")
    user = query.from_user
    data = context.user_data

    if query.data == "confirm_submit":
        msg = f"""
*{t('application_received', lang)}*

👤 *{t("name", lang)}*: {user.full_name}
📞 *{t("phone", lang)}*: {data.get('phone')}
📍 *{t("region", lang)}*: {data.get('region')}
🏢 *{t("branch", lang)}*: {data.get('selected_branch', {}).get('title', {}).get(lang, '')}
📌 *{t("vacancy", lang)}*: {data.get('selected_vacancy', {}).get(lang, '')}
📖 *{t("bio", lang)}*: {data.get('bio')}
🎂 *{t("birth_date", lang)}*: {data.get('birth_date')}
🏠 *{t("live_place", lang)}*: {data.get('live_place')}
🌐 *{t("languages", lang)}*: {data.get('languages')}
🖥 *{t("software", lang)}*: {data.get('software')}
👨‍👩‍👧 *{t("family", lang)}*: {data.get('family')}
🏢 *{t("last_work", lang)}*: {data.get('last_work')}
❌ *{t("leave_reason", lang)}*: {data.get('leave_reason')}
🎯 *{t("interest", lang)}*: {data.get('interest')}
📢 *{t("source", lang)}*: {data.get('source')}
👤 *{t("personality", lang)}*: {data.get('personality')}
📚 *{t("books", lang)}*: {data.get('books')}
🏅 *{t("achievements", lang)}*: {data.get('achievements')}
💼 *{t("position", lang)}*: {data.get('position')}
⏰ *{t("time", lang)}*: {data.get('time')}
""".strip()

        await context.bot.send_photo(
            chat_id=GROUP_ID,
            photo=data.get("photo"),
            caption=msg,
            parse_mode="Markdown"
        )

        await query.edit_message_caption({
            "en": "✅ Your application has been submitted. Thank you!",
            "uz": "✅ Arizangiz yuborildi. Rahmat!",
            "ru": "✅ Ваша анкета отправлена. Спасибо!"
        }[lang])

    else:
        await query.edit_message_caption({
            "en": "❌ Application cancelled.",
            "uz": "❌ Ariza bekor qilindi.",
            "ru": "❌ Анкета отменена."
        }[lang])

    context.user_data.clear()
    return ConversationHandler.END

