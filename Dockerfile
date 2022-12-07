FROM rust:1.65
WORKDIR /usr/src/print-tgbot
COPY . .
RUN cargo install --path .
CMD ["print-tgbot"]
