# Marakulin Andrey https://github.com/Annndruha
# 2023

ans = {
    'auth': '🔑 Авторизация',
    'conf': '📄 Конфиденциальность',
    'back': '◀️ Назад',
    'conf_full': 'Файлы, которые вы отправляете через бота, будут храниться в течение нескольких месяцев на хостинге '
                 'в Москве, а также в этом чате Telegram.\nДоступ к файлам имеет узкий круг лиц, '
                 'ответственных за работоспособность сервиса печати.\n'
                 'Мы НЕ рекомендуем использовать данный сервис для печати конфиденциальных документов!',
    'hello': '👋🏻 Привет! Я телеграм-бот бесплатного принтера.\n'
             'Отправьте PDF файл и получите PIN для печати.',
    'help':  'Я телеграм-бот бесплатного принтера профкома студентов физического факультета МГУ!\n\n'
             'Для использования принтера требуется авторизация по номеру профсоюзного билета. Номер Вы можете найти'
             'Отправьте PDF файл и получите PIN для печати. '
             'Поддерживаются только <b>.pdf</b> файлы размером не более 3МБ.\n'
             'С этим PIN необходимо подойти к принтеру и ввести его в терминал печати. '
             'Либо отсканировать QR-код на принтере с помощью ссылки на сканирование. После чего начнётся печать.'
             '\n\nБот разработан группой программистов профкома, так же как и приложение'
             '<a href="https://app.test.profcomff.com/"> Твой ФФ!</a> '
             'В приложении Вы сможете найти больше настроек печати и много других возможностей.\n'
             'Так же есть <a href="https://vk.me/profcomff_print_bot">бот для печати ВКонтакте</a>.',

    'val_fail': 'Проверка не пройдена. Удостоверьтесь что вы состоите в профсоюзе и правильно ввели данные.'
                '\n\nВведите фамилию и номер профсоюзного билета в формате:\n\nИванов\n1234567',
    'val_pass': '🥳 Поздравляю! Проверка пройдена и данные сохранены для этого телеграм-аккаунта. Можете присылать pdf.',
    'val_need': 'Для использования принтера необходимо авторизоваться.\n'
                'Отправьте фамилию и номер профсоюзного билета в формате:\n\nИванов\n1234567',
    'val_update_fail': 'Сообщение не распознано.\nЧтобы открыть инструкцию введите: /help\nДля того чтобы обновить '
                       'данные авторизации введите фамилию и номер'
                       'профсоюзного билета в формате:\n\nИванов\n1234567',
    'val_update_pass': 'Поздравляю! Проверка пройдена и данные обновлены.',
    'val_addition': '\n\nНо для начала нужно авторизоваться. Нажмите на кнопку ниже:',
    'val_info': 'Вы авторизованы!\nВаш id в телеграм: <code>{}</code>\nФамилия: <code>{}</code>\nНомер профсоюзного '
                'билета: <code>{}</code>',

    'history_not_implement': 'Эта функция ещё не готова.\nТут будет история печати :)',
    'unknown_command': 'Неизвестная команда.\nУ бота лишь три команды: /start /help /auth',
    'only_pdf': 'Документы на печать принимаются только в формате PDF',
    'doc_not_accepted': '❌ Документ не принят, сначала авторизуйтесь:\n'
                        'Отправьте фамилию и номер профсоюзного билета в формате:\n\nИванов\n1234567',
    'file_size_error': '❌ Принимаются только файлы размером меньше 3MB.\nФайл <b>{}</b> не принят.',
    'send_to_print': '✅ Файл <b>{}</b> успешно загружен. '
                     'Для печати подойдите к принтеру и введите PIN:\n\n<b>{}</b>\n\n'
                     'Или <a href="https://printer.ui.profcomff.com/qr#{}">отсканируйте QR код на экране '
                     'принтера.</a>\n',

    'unknown_query': 'Видимо бот обновился, выполните команду /start',
    'im_broken': 'Глубоко внутри меня что-то сломалось...\nПопробуйте через пару минут.',
    'download_error': 'Ошибка получения файла, попробуйте позже.',
    'print_err': '❌ Ошибка сервера печати. Попробуйте позже.'
}
