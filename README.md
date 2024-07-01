# OpenBot

<img src="https://i.ibb.co/BLWhrcx/IMG-3141.jpg" width="400"/>

OpenBot is the first sniper and trading bot designed for the OpenGPU Network. It enables users to snipe tokens, swap tokens, and place limit orders efficiently. The bot interacts with the OpenGPU Devnet and facilitates seamless transactions through the Telegram interface.

## Features

- **Snipe Tokens**: Quickly snipe newly launched tokens.
- **Swap Tokens**: Easily swap between different tokens.
- **Limit Orders**: Place buy or sell orders at specific price limits.

## Commands

- `/begin`: Start the wallet setup process.

## Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/yourusername/OpenBot.git
   cd OpenBot
   ```

2. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

3. **Download ChromeDriver**:
   - [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)

4. **Set up environment variables**:
   Create a `.env` file in the project directory and add your Telegram bot token:
   ```env
   TOKEN=your_telegram_bot_token
   ```

## Usage

1. **Run the bot**:
   ```sh
   python main.py
   ```

2. **Interact with the bot on Telegram**:
   - Start the bot using `/start`.
   - Follow the prompts to set up your wallet or import an existing wallet.
   - Use the provided commands to snipe tokens, swap tokens, or place limit orders.

<img src="https://github.com/bayramf/openbot/assets/62951045/6be553c9-dc13-4831-b3bf-c57a685d71a8" width="400"/> <img src="https://github.com/bayramf/openbot/assets/62951045/c6898097-7d0f-4374-9278-a952ee098f90" width="400"/>

## Code Explanation

The bot is built using Python and leverages the following libraries:

- `telegram`: For interacting with the Telegram API.
- `web3`: For interacting with the OpenGPU blockchain.
- `selenium`: For web scraping and automation tasks.

### Key Functions

- **Wallet Setup**: Allows users to create or import a wallet.
- **Snipe Tokens**: Automates the process of purchasing new tokens quickly.
- **Swap Tokens**: Enables users to swap between tokens.
- **Limit Orders**: Allows users to place buy/sell orders at specific prices.

### Example Code Snippet

```python
async def snipe(update: Update, context: CallbackContext) -> None:
    user_data = context.user_data
    wallet_address = user_data['wallet_address']
    private_key = user_data['private_key']
    token_address = user_data['token_address']
    amount_to_buy = user_data['amount_to_buy']
    
    # Prepare the swap function call parameters
    buy_path = [WoGPU_address_checksum, token_address]
    amount_to_buy_for = int(amount_to_buy) * 10**18

    async def snipe_order():
        n = 1
        while True:
            driver = webdriver.Chrome(service=service, options=options)
            token_url = f"https://dex.ogpuscan.io/token/{token_address}"  # Replace with the actual URL
            driver.get(token_url)
            await asyncio.sleep(3)

            try:
                submit_button = driver.find_element(By.XPATH, "//button[text()='Buy']")  # Replace with actual XPath

                buy_tx_params = {
                    "nonce": web3.eth.get_transaction_count(wallet_address),
                    "from": wallet_address,
                    "chainId": oGPU_chain_id,
                    "gas": 500_000,
                    "maxPriorityFeePerGas": web3.eth.max_priority_fee,
                    "maxFeePerGas": 100 * 10**10,
                    "value": amount_to_buy_for,    
                }
                buy_tx = router_contract.functions.swapExactETHForTokens(
                    0,  # Min amount out
                    buy_path,
                    wallet_address,
                    int(time.time()) + 180  # Deadline now + 180 sec
                ).build_transaction(buy_tx_params)

                signed_buy_tx = web3.eth.account.sign_transaction(buy_tx, private_key)
                tx_hash = web3.eth.send_raw_transaction(signed_buy_tx.rawTransaction)
                receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
                snipe_text = (
                    f"✅ Snipe Order Executed! \n\n"
                    f"💡 Tx Hash: {Web3.to_hex(tx_hash)}"
                )
                await update.message.reply_text(snipe_text)
                await asyncio.sleep(1.5)
                driver.quit()
                break
            
            except:
                if n == 1:
                    await update.message.reply_text(f"⚠️ Snipe Order Placed!")
                n = n + 1
                driver.quit()
                pass

    asyncio.create_task(snipe_order())
    await reset_bot_state(update, context)  # Reset the bot state after the operation
```

## Contributing

We welcome contributions to improve OpenBot. Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

For any questions or support, please reach out to us on [Telegram](https://t.me/+V8UY4bGqyEAxZmQ0).
