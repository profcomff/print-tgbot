use dotenv::dotenv;

// This bot throws a dice on each incoming message.

use teloxide::{prelude::*, utils::markdown::link};

#[tokio::main]
async fn main() {
    dotenv().ok();
    pretty_env_logger::init();
    log::info!("Starting throw dice bot...");

    let bot = Bot::from_env();

    teloxide::repl(bot, |bot: Bot, msg: Message| async move {
        match msg.text() {
            Some(_text) => {
                let app_link = link("https://app.profcomff.com", "Твой ФФ");
                let vk_link = link("https://vk.com/profcomff_print_bot", "бота в ВК");
                let plug = format!("Этот telegram\\-бот находится в разработке\\.\nБесплатный принтер доступен всегда в приложении {app_link} и через {vk_link}\\!");
                bot.send_message(msg.chat.id, plug).parse_mode(teloxide::types::ParseMode::MarkdownV2).await?;
            }
            None => {}
        }
        Ok(())
    })
    .await;
}
