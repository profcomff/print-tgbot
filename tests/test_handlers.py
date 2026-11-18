import asyncio
from io import BytesIO
from unittest.mock import AsyncMock, Mock

import pytest
from requests import HTTPError, Timeout


@pytest.fixture
def handlers(monkeypatch):
    monkeypatch.setenv('BOT_TOKEN', '123:test')
    monkeypatch.setenv('DB_DSN', 'postgresql://test@localhost/test')
    monkeypatch.setenv('MARKETING_URL', 'https://marketing.example')
    monkeypatch.setenv('PRINT_URL', 'https://print.example')
    monkeypatch.setenv('PRINT_URL_QR', 'https://print.example/qr/')
    monkeypatch.setenv('MAX_PDF_SIZE_MB', '3')
    from src import handlers

    return handlers


@pytest.fixture
def update():
    message = Mock(text=None, document=Mock(file_name='A & B.pdf'), reply_text=AsyncMock())
    return Mock(message=message, callback_query=None, effective_user=Mock(id=1, full_name='User'))


def test_upload_413_reports_the_print_limit(handlers, mocker, update):
    mocker.patch.object(handlers, '__auth', return_value=(1, 'Иванов', '123'))
    mocker.patch.object(handlers, '__get_attachments', new=AsyncMock(return_value=BytesIO(b'pdf')))
    created = Mock(status_code=200)
    created.json.return_value = {'pin': '1234'}
    post = mocker.patch.object(handlers.requests, 'post', side_effect=[created, Mock(status_code=413)])

    asyncio.run(handlers.handler_print(update, Mock()))

    assert post.call_count == 2
    update.message.reply_text.assert_awaited_once()
    assert update.message.reply_text.call_args.kwargs['text'] == handlers.ans.print_limit_error.format('A &amp; B.pdf')


def test_print_timeout_is_reported_to_the_user(handlers, mocker, update):
    mocker.patch.object(handlers, '__auth', return_value=(1, 'Иванов', '123'))
    mocker.patch.object(handlers, '__get_attachments', new=AsyncMock(return_value=BytesIO(b'pdf')))
    mocker.patch.object(handlers.requests, 'post', side_effect=Timeout())
    update.effective_message = update.message

    asyncio.run(handlers.handler_print(update, Mock()))

    update.message.reply_text.assert_awaited_once_with(handlers.ans.print_err)


def test_membership_http_error_does_not_write_to_db(handlers, mocker, update):
    update.message.text = 'Иванов\n123'
    update.effective_message = update.message
    response = Mock()
    response.raise_for_status.side_effect = HTTPError()
    response.json.return_value = {'detail': 'service unavailable'}
    mocker.patch.object(handlers.requests, 'get', return_value=response)
    session = mocker.patch.object(handlers, 'Session')

    asyncio.run(handlers.handler_register(update, Mock()))

    session.assert_not_called()
    update.message.reply_text.assert_awaited_once_with(handlers.ans.print_err)
