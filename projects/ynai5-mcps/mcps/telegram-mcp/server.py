import os, asyncio
from fastmcp import FastMCP
from telethon import TelegramClient
from telethon.tl.functions.messages import SendMessageRequest
from telethon.tl.types import InputPeerChannel
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("telegram")

API_ID   = int(os.getenv("TELEGRAM_API_ID", "0"))
API_HASH = os.getenv("TELEGRAM_API_HASH", "")
SESSION  = os.getenv("TELEGRAM_SESSION_STRING", "")
SESSION_NAME = os.getenv("TELEGRAM_SESSION_NAME", "anon")

def get_client():
    if SESSION:
        from telethon.sessions import StringSession
        return TelegramClient(StringSession(SESSION), API_ID, API_HASH)
    return TelegramClient(SESSION_NAME, API_ID, API_HASH)

@mcp.tool()
def send_message(chat_id: str, message: str, parse_mode: str = "md") -> str:
    """Send a message to any Telegram chat, channel, or group by username or ID."""
    async def _run():
        async with get_client() as client:
            entity = await client.get_entity(chat_id)
            await client.send_message(entity, message, parse_mode=parse_mode if parse_mode != "md" else "markdown")
            return f"Message sent to {chat_id}"
    return asyncio.get_event_loop().run_until_complete(_run())

@mcp.tool()
def send_block_syndicate_signal(channel: str, asset: str, direction: str,
                                 entry_low: str, entry_high: str,
                                 target1: str, target2: str,
                                 stop_loss: str, thesis: str,
                                 risk_level: str = "MEDIUM", vip: bool = False) -> str:
    """Send a formatted Block Syndicate trading signal to a Telegram channel."""
    if vip:
        msg = f"""🔐 **BLOCK SYNDICATE VIP**

📊 **Asset:** ${asset}
📈 **Direction:** {direction}

📍 **ENTRY ZONE**
${entry_low} – ${entry_high}

🎯 **TARGETS**
T1: ${target1}
T2: ${target2}

🛑 **STOP LOSS:** ${stop_loss}

📝 **THESIS**
{thesis}

⚠️ Risk Level: {risk_level}
_Not financial advice. Always size responsibly._

#BlockSyndicate #YNAI5 #{asset}"""
    else:
        msg = f"""🚨 **BLOCK SYNDICATE**

📊 ${asset} | {direction}
💵 Entry: ${entry_low} – ${entry_high}
🎯 T1: ${target1} | T2: ${target2}
🛑 Stop: ${stop_loss}

⚡ {thesis}

⚠️ NFA
#BlockSyndicate #{asset}"""

    async def _run():
        async with get_client() as client:
            entity = await client.get_entity(channel)
            await client.send_message(entity, msg, parse_mode="markdown")
            return f"Signal sent to {channel}"
    return asyncio.get_event_loop().run_until_complete(_run())

@mcp.tool()
def get_chats(limit: int = 20) -> str:
    """List your Telegram chats and channels."""
    async def _run():
        async with get_client() as client:
            dialogs = await client.get_dialogs(limit=limit)
            result = []
            for d in dialogs:
                result.append(f"Name: {d.name} | ID: {d.id} | Type: {'Channel' if d.is_channel else 'Group' if d.is_group else 'User'}")
            return "\n".join(result)
    return asyncio.get_event_loop().run_until_complete(_run())

@mcp.tool()
def get_messages(chat_id: str, limit: int = 10) -> str:
    """Get recent messages from a chat or channel."""
    async def _run():
        async with get_client() as client:
            entity = await client.get_entity(chat_id)
            messages = await client.get_messages(entity, limit=limit)
            result = []
            for m in messages:
                result.append(f"[{m.date}] {m.sender_id}: {m.text[:200] if m.text else '[media]'}")
            return "\n".join(result)
    return asyncio.get_event_loop().run_until_complete(_run())

@mcp.tool()
def pin_message(chat_id: str, message_id: int) -> str:
    """Pin a message in a chat or channel."""
    async def _run():
        async with get_client() as client:
            entity = await client.get_entity(chat_id)
            await client.pin_message(entity, message_id)
            return f"Message {message_id} pinned in {chat_id}"
    return asyncio.get_event_loop().run_until_complete(_run())

@mcp.tool()
def send_to_multiple(channels: str, message: str) -> str:
    """Send the same message to multiple channels at once. channels = comma-separated list."""
    channel_list = [c.strip() for c in channels.split(",")]
    async def _run():
        results = []
        async with get_client() as client:
            for ch in channel_list:
                try:
                    entity = await client.get_entity(ch)
                    await client.send_message(entity, message, parse_mode="markdown")
                    results.append(f"✅ Sent to {ch}")
                except Exception as e:
                    results.append(f"❌ Failed {ch}: {e}")
        return "\n".join(results)
    return asyncio.get_event_loop().run_until_complete(_run())

@mcp.tool()
def get_channel_info(channel: str) -> str:
    """Get info about a Telegram channel — member count, description, etc."""
    async def _run():
        async with get_client() as client:
            entity = await client.get_entity(channel)
            full = await client.get_entity(entity)
            return f"Title: {full.title}\nID: {full.id}\nUsername: @{getattr(full, 'username', 'N/A')}"
    return asyncio.get_event_loop().run_until_complete(_run())

if __name__ == "__main__":
    mcp.run()
