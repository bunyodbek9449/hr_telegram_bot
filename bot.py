import logging
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    filters,
)
from config import BOT_TOKEN
from handlers import start_handler
from states import Form, AdminState
from handlers.start_handler import (
    start, select_language, select_region, select_branch,
    show_vacancies, select_vacancy, ask_phone, save_phone,
    save_bio, save_birth_date, save_live_place, save_languages,
    save_software, save_family, save_last_work, save_leave_reason,
    save_interest, save_source, save_personality, save_books,
    save_achievements, save_position, save_time, save_photo, cancel, handle_main_menu, show_main_menu,
    select_branch_info
)
from handlers.admin_handler import (
    start_add_vacancy, admin_select_region, admin_select_branch,
    enter_en, enter_uz, enter_ru,
    list_vacancies_command, list_select_region, list_select_branch,
    del_vacancy_command, del_select_region, del_select_branch, del_confirm, admin_select_region
)
logging.basicConfig(level=logging.INFO)

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # ✅ Candidate Application Flow
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            Form.LANGUAGE: [
                CallbackQueryHandler(select_language, pattern="^lang_"),
                CallbackQueryHandler(handle_main_menu, pattern="^menu_"),
                CallbackQueryHandler(show_main_menu, pattern="^menu_back$")
            ],

            Form.REGION: [
                CallbackQueryHandler(select_region, pattern="^region_")
            ],
            Form.BRANCH: [
                CallbackQueryHandler(select_branch, pattern="^branch_"),
                CallbackQueryHandler(select_branch_info, pattern="^branchinfo_"),
                CallbackQueryHandler(handle_main_menu, pattern="^menu_back$")
            ],
            Form.VACANCY: [
                CallbackQueryHandler(show_vacancies, pattern="^apply_branch$"),
                CallbackQueryHandler(select_vacancy, pattern="^vacancy_"),
            ],
            Form.PHONE: [MessageHandler(filters.CONTACT, save_phone)],
            Form.BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_bio)],
            Form.BIRTH_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_birth_date)],
            Form.LIVE_PLACE: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_live_place)],
            Form.LANGUAGES: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_languages)],
            Form.SOFTWARE: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_software)],
            Form.FAMILY: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_family)],
            Form.LAST_WORK: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_last_work)],
            Form.LEAVE_REASON: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_leave_reason)],
            Form.INTEREST: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_interest)],
            Form.SOURCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_source)],
            Form.PERSONALITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_personality)],
            Form.BOOKS: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_books)],
            Form.ACHIEVEMENTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_achievements)],
            Form.POSITION: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_position)],
            Form.TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_time)],
            Form.PHOTO: [MessageHandler(filters.PHOTO, save_photo)],
            Form.CONFIRM: [CallbackQueryHandler(start_handler.confirm_application)],
        },
        fallbacks=[
            CommandHandler("cancel", cancel)
        ],
    )

    # ✅ Admin Vacancy Management FSM (Multilingual input)
    admin_conv = ConversationHandler(
        entry_points=[CommandHandler("addvacancy", start_add_vacancy)],
        states={
            AdminState.SELECT_REGION: [CallbackQueryHandler(admin_select_region, pattern="^admin_region_")],
            AdminState.SELECT_BRANCH: [CallbackQueryHandler(admin_select_branch, pattern="^admin_branch_")],
            AdminState.ENTER_EN: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_en)],
            AdminState.ENTER_UZ: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_uz)],
            AdminState.ENTER_RU: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_ru)],
            AdminState.LIST_REGION: [CallbackQueryHandler(list_select_region, pattern="^list_region_")],
            AdminState.LIST_BRANCH: [CallbackQueryHandler(list_select_branch, pattern="^list_branch_")],
            AdminState.DEL_REGION: [CallbackQueryHandler(del_select_region, pattern="^del_region_")],
            AdminState.DEL_BRANCH: [CallbackQueryHandler(del_select_branch, pattern="^del_branch_")],
            AdminState.DEL_INDEX: [CallbackQueryHandler(del_confirm, pattern="^del_index_")],

        },
        fallbacks=[],
        allow_reentry=True,
    )

    application.add_handler(conv_handler)
    application.add_handler(admin_conv)
    application.add_handler(CommandHandler("listvacancies", list_vacancies_command))
    application.add_handler(CommandHandler("delvacancy", del_vacancy_command))

    application.run_polling()

if __name__ == "__main__":
    main()
