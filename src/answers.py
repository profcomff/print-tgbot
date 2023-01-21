# Marakulin Andrey https://github.com/Annndruha
# 2023

ans = {
    'auth': '🔑 Авторизация',
    'about': '📄 Описание',
    'back': '◀️ Назад',
    'qr': '📷 Печать по QR',
    'kb_print': '⚙️ Настройки печати',
    'kb_print_copies': '📑 Копий:',
    'kb_print_side': '📎 Односторонняя печать',
    'kb_print_two_side': '🖇 Двухсторонняя печать',
    'hello': '👋🏻 Привет! Я телеграм-бот бесплатного принтера.\n'
             'Отправьте PDF файл и получите PIN для печати.',
    'help': 'Я телеграм-бот бесплатного принтера профкома студентов физического факультета МГУ!\n\n'
            '❔ Отправьте PDF файл и получите PIN для печати. '
            'Поддерживаются только <b>.pdf</b> файлы размером не более 3МБ.\n'
            'С этим PIN необходимо подойти к принтеру и ввести его в терминал печати. '
            'Либо отсканировать QR-код на принтере с помощью кнопки. После этого начнётся печать.'
            '\n\n❗️ Файлы, которые вы отправляете через бота, будут храниться в течение нескольких месяцев на сервере '
            'в Москве, а также в этом чате Telegram.\nДоступ к файлам имеет узкий круг лиц, '
            'ответственных за работоспособность сервиса печати.\n'
            'Мы <b>НЕ</b> рекомендуем использовать данный сервис для печати конфиденциальных документов!'
            '\n\n💻 Бот разработан группой программистов профкома, так же как и приложение'
            '<a href="https://app.test.profcomff.com/"> Твой ФФ!</a> '
            'В приложении вы сможете найти больше настроек печати и много других возможностей.\n'
            'Так же есть <a href="https://vk.me/profcomff_print_bot">бот для печати ВКонтакте</a>.',

    'val_fail': '⚠️ Проверка не пройдена. Удостоверьтесь что вы состоите в профсоюзе и правильно ввели данные.'
                '\n\nВведите фамилию и номер профсоюзного билета в формате:\n\nИванов\n1234567',
    'val_pass': '🥳 Поздравляю! Проверка пройдена и данные сохранены для этого телеграм-аккаунта. Можете присылать pdf.',
    'val_need': '👤 Для использования принтера необходимо авторизоваться.\n'
                'Отправьте фамилию и номер профсоюзного билета в формате:\n\nИванов\n1234567',
    'val_update_fail': 'Сообщение не распознано.\nЧтобы открыть инструкцию введите: /help\nДля того чтобы обновить '
                       'данные авторизации введите фамилию и номер'
                       'профсоюзного билета в формате:\n\nИванов\n1234567',
    'val_update_pass': '🥳 Поздравляю! Проверка пройдена и данные обновлены.',
    'val_addition': '\n\nНо для начала нужно авторизоваться. Нажмите на кнопку ниже:',
    'val_info': 'Вы авторизованы!\nВаш id в телеграм: <code>{}</code>\nФамилия: <code>{}</code>\nНомер профсоюзного '
                'билета: <code>{}</code>',

    'unknown_command': 'Неизвестная команда.\nУ бота лишь три команды: /start /help /auth',
    'only_pdf': 'Документы на печать принимаются только в формате PDF',
    'doc_not_accepted': '⚠️ Документ не принят, сначала авторизуйтесь:\n'
                        'Отправьте фамилию и номер профсоюзного билета в формате:\n\nИванов\n1234567',
    'file_size_error': '⚠️ Принимаются только файлы размером меньше 3 MB.\nФайл <b>{}</b> не принят.',
    'send_to_print': '✅ Файл <b>{}</b> успешно загружен. '
                     'Для печати подойдите к принтеру и введите PIN:\n\n<b>{}</b>\n\n'
                     'Для быстрой печати отсканируйте QR код на экране принтера.',
    'qr_print': 'https://printer.ui.test.profcomff.com/qr#{}',
    'settings_warning': '\nНастройки сохраняются автоматически.',
    'settings_change_fail': 'Что-то сломалось, настройки печати не изменены, попробуйте через пару минут.',
    'unknown_keyboard_payload': 'Видимо бот обновился, выполните команду /start',
    'im_broken': 'Глубоко внутри меня что-то сломалось...\nПопробуйте через пару минут.',
    'download_error': 'Ошибка получения файла, попробуйте позже.',
    'print_err': '❌ Ошибка сервера печати. Попробуйте позже.'
}
