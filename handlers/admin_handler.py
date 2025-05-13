from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
from config import ADMIN_ID
from utils.vacancy_manager import add_vacancy, get_vacancies, delete_vacancy
from states import AdminState

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
            "photo_url": "https://upload.wikimedia.org/wikipedia/commons/9/99/Sample_User_Icon.png",
            "location": {"latitude": 41.2995, "longitude": 69.2401}
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
            "photo_url": "https://upload.wikimedia.org/wikipedia/commons/9/99/Sample_User_Icon.png",
            "location": {"latitude": 41.3445, "longitude": 69.2801}
        }
    ],
    "Samarqand": [
        {
            "title": {
                "en": "Samarkand HR Branch",
                "uz": "Samarqand HR Filiali",
                "ru": "Бухарский HR филиал"
            },
            "description": {
                "en": "Regional office for HR interviews in Samarkand.",
                "uz": "Samarqanddagi HR suhbatlari uchun mintaqaviy ofis.",
                "ru": "Региональный офис для HR-собеседований в Самарканде."
            },
            "photo_url": "https://upload.wikimedia.org/wikipedia/commons/9/99/Sample_User_Icon.png",
            "location": {"latitude": 39.6270, "longitude": 66.9749}
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
    "Buxoro": [
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


async def start_add_vacancy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return await update.message.reply_text("❌ Access denied.")

    keyboard = [
        [InlineKeyboardButton(region, callback_data=f"admin_region_{region}")]
        for region in REGION_BRANCHES
    ]
    await update.message.reply_text("📍 Select region:", reply_markup=InlineKeyboardMarkup(keyboard))
    return AdminState.SELECT_REGION


async def admin_select_region(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    region = query.data.replace("admin_region_", "")
    context.user_data["admin_region"] = region
    lang = context.user_data.get("lang", "en")
    branches = REGION_BRANCHES.get(region, [])
    keyboard = [
        [InlineKeyboardButton(branch["title"][lang], callback_data=f"admin_branch_{i}")]
        for i, branch in enumerate(branches)
    ]

    await query.edit_message_text("🏢 Select branch:", reply_markup=InlineKeyboardMarkup(keyboard))
    return AdminState.SELECT_BRANCH


async def admin_select_branch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    region = context.user_data["admin_region"]
    branch_index = int(query.data.replace("admin_branch_", ""))
    branch = REGION_BRANCHES[region][branch_index]
    context.user_data["admin_branch"] = branch

    await query.edit_message_text("🇬🇧 Enter position name in English:")
    return AdminState.ENTER_EN


async def enter_en(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["position_en"] = update.message.text.strip()
    await update.message.reply_text("🇺🇿 Lavozim nomini o‘zbek tilida kiriting:")
    return AdminState.ENTER_UZ


async def enter_uz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["position_uz"] = update.message.text.strip()
    await update.message.reply_text("🇷🇺 Введите название должности на русском языке:")
    return AdminState.ENTER_RU


async def enter_ru(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["position_ru"] = update.message.text.strip()
    region = context.user_data["admin_region"]
    branch = context.user_data["admin_branch"]

    position = {
        "en": context.user_data["position_en"],
        "uz": context.user_data["position_uz"],
        "ru": context.user_data["position_ru"],
    }

    add_vacancy(region, branch, position)
    lang = context.user_data.get("lang", "en")

    await update.message.reply_text(
        f"✅ Vacancy added to *{branch['title'][lang]}* in *{region}*:\n"
        f"- EN: {position['en']}\n"
        f"- UZ: {position['uz']}\n"
        f"- RU: {position['ru']}",
        parse_mode="Markdown"
    )
    return ConversationHandler.END


async def list_vacancies_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return await update.message.reply_text("❌ Access denied.")

    keyboard = [
        [InlineKeyboardButton(region, callback_data=f"list_region_{region}")]
        for region in REGION_BRANCHES
    ]
    await update.message.reply_text("📍 Select region to list vacancies:", reply_markup=InlineKeyboardMarkup(keyboard))
    return AdminState.LIST_REGION


async def list_select_region(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    region = query.data.replace("list_region_", "")
    context.user_data["list_region"] = region

    branches = REGION_BRANCHES[region]
    lang = context.user_data.get("lang", "en")

    keyboard = [
        [InlineKeyboardButton(branch["title"][lang], callback_data=f"list_branch_{i}")]
        for i, branch in enumerate(branches)
    ]
    await query.edit_message_text("🏢 Select branch:", reply_markup=InlineKeyboardMarkup(keyboard))
    return AdminState.LIST_BRANCH


async def list_select_branch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    region = context.user_data["list_region"]
    branch_index = int(query.data.replace("list_branch_", ""))
    branch = REGION_BRANCHES[region][branch_index]

    vacancies = get_vacancies(region, branch)
    if not vacancies:
        await query.edit_message_text("⚠️ No vacancies in this branch.")
    else:
        text = "\n".join(
            [f"{i+1}. {v.get('en', v)} / {v.get('uz', '')} / {v.get('ru', '')}" for i, v in enumerate(vacancies)]
        )
        await query.edit_message_text(f"📋 *Vacancies in {branch['title'][lang]}:*\n{text}", parse_mode="Markdown")
    return ConversationHandler.END


async def del_vacancy_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return await update.message.reply_text("❌ Access denied.")

    keyboard = [
        [InlineKeyboardButton(region, callback_data=f"del_region_{region}")]
        for region in REGION_BRANCHES
    ]
    await update.message.reply_text("📍 Select region to delete from:", reply_markup=InlineKeyboardMarkup(keyboard))
    return AdminState.DEL_REGION


async def del_select_region(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    region = query.data.replace("del_region_", "")
    context.user_data["del_region"] = region
    lang = context.user_data.get("lang", "en")

    branches = REGION_BRANCHES[region]
    keyboard = [
        [InlineKeyboardButton(branch["title"][lang], callback_data=f"del_branch_{i}")]
        for i, branch in enumerate(branches)
    ]
    await query.edit_message_text("🏢 Select branch to delete from:", reply_markup=InlineKeyboardMarkup(keyboard))
    return AdminState.DEL_BRANCH


async def del_select_branch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    region = context.user_data["del_region"]
    branch_index = int(query.data.replace("del_branch_", ""))
    branch = REGION_BRANCHES[region][branch_index]
    context.user_data["del_branch"] = branch

    vacancies = get_vacancies(region, branch)
    if not vacancies:
        await query.edit_message_text("⚠️ No vacancies to delete.")
        return ConversationHandler.END

    keyboard = [
        [InlineKeyboardButton(f"{i + 1}. {v.get('en', v)}", callback_data=f"del_index_{i}")]
        for i, v in enumerate(vacancies)
    ]
    await query.edit_message_text("❌ Select a vacancy to delete:", reply_markup=InlineKeyboardMarkup(keyboard))
    return AdminState.DEL_INDEX


async def del_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    region = context.user_data["del_region"]
    branch = context.user_data["del_branch"]
    index = int(query.data.replace("del_index_", ""))

    success = delete_vacancy(region, branch, index)
    if success:
        await query.edit_message_text("✅ Vacancy deleted successfully.")
    else:
        await query.edit_message_text("❌ Failed to delete vacancy.")
    return ConversationHandler.END
