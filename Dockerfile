FROM rust:1.65 as builder
WORKDIR /usr/src/print-tgbot
COPY . .
RUN cargo install --path .

FROM debian:buster-slim
RUN apt-get update && apt-get install -y ca-certificates libssl1.1 && update-ca-certificates
COPY --from=builder /usr/local/cargo/bin/print-tgbot /usr/local/bin/print-tgbot
CMD ["print-tgbot"]
