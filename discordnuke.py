import discord
import asyncio
from colorama import Fore, Style, init

init(autoreset=True)

GREEN = Fore.LIGHTGREEN_EX
YELLOW = Fore.YELLOW
RED = Fore.LIGHTRED_EX
CYAN = Fore.CYAN
RESET = Style.RESET_ALL

SUCCESS = f"{GREEN}[\u2713]{RESET}"
ERROR = f"{RED}[\u2717]{RESET}"
INFO = f"{CYAN}[i]{RESET}"
WARN = f"{YELLOW}[!]{RESET}"
ACTION = f"{GREEN}[>>]{RESET}"

INVITE_LINK = "https://discord.gg/Y4cknD6V5r"
NUKE_MESSAGE = f"@everyone NUKED BY {INVITE_LINK}"

DONE_ASCII = r"""
           ______
        .-"      "-.
       /            \
      |              |
      |,  .-.  .-.  ,|
      | )(__/  \__)( |
      |/     /\     \|
      (_     ^^     _)
       \__|IIIIII|__/
        | \IIIIII/ |
        \          /
         `--------`
          ____   ___  _   _ _____ 
|  _ \ / _ \| \ | | ____|
| | | | | | |  \| |  _|  
| |_| | |_| | |\  | |___ 
|____/ \___/|_| \_|_____|
"""

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
    print(f"{SUCCESS} Done kicking bots.\n{DONE_ASCII}")

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
    print(f"{SUCCESS} Done deleting channels.\n{DONE_ASCII}")

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
    print(f"{SUCCESS} Created all channels.\n{DONE_ASCII}")

async def rename_all_channels(guild, prefix):
    print(f"{ACTION} Renaming channels...")
    channels = [ch for ch in guild.channels if isinstance(ch, (discord.TextChannel, discord.VoiceChannel))]
    if not channels:
        print(f"{WARN} No channels to rename.")
        return
    for i, ch in enumerate(channels, start=1):
        old_name = ch.name
        try:
            await ch.edit(name=f"{prefix} {i}")
            print(f"{SUCCESS} Renamed {old_name} to {prefix} {i}")
        except Exception as e:
            print(f"{ERROR} Failed renaming {old_name}: {e}")
        await asyncio.sleep(DELAY)
    print(f"{SUCCESS} Renaming done.\n{DONE_ASCII}")

async def create_roles(guild, count):
    print(f"{ACTION} Creating {count} roles...")
    for i in range(count):
        try:
            await guild.create_role(name=f"🔥 S*x {i+1}")
            print(f"{SUCCESS} Created role Sex {i+1}")
        except Exception as e:
            print(f"{ERROR} Failed creating role: {e}")
        await asyncio.sleep(DELAY)
    print(f"{SUCCESS} Created all roles.\n{DONE_ASCII}")

async def rename_all_roles(guild, prefix):
    print(f"{ACTION} Renaming roles...")
    roles = [r for r in guild.roles if not r.is_default()]
    if not roles:
        print(f"{WARN} No roles to rename.")
        return
    for i, role in enumerate(roles, start=1):
        old_name = role.name
        try:
            await role.edit(name=f"{prefix} {i}")
            print(f"{SUCCESS} Renamed {old_name} to {prefix} {i}")
        except Exception as e:
            print(f"{ERROR} Failed renaming {old_name}: {e}")
        await asyncio.sleep(DELAY)
    print(f"{SUCCESS} Role renaming done.\n{DONE_ASCII}")

async def ban_user(guild):
    user_input = input(f"{GREEN}Enter the user ID or mention to ban:{RESET} ").strip()
    
    # Extract user ID from mention if needed
    if user_input.startswith('<@') and user_input.endswith('>'):
        user_id = user_input.replace('<@!', '').replace('<@', '').replace('>', '')
    else:
        user_id = user_input
    
    try:
        user_id = int(user_id)
    except ValueError:
        print(f"{ERROR} Invalid user ID.")
        return
    
    try:
        user = await bot.fetch_user(user_id)
        await guild.ban(user, reason="Banned by bot command")
        print(f"{SUCCESS} Banned user {user} ({user_id})")
    except discord.NotFound:
        print(f"{ERROR} User not found.")
    except discord.Forbidden:
        print(f"{WARN} Missing permissions to ban user.")
    except Exception as e:
        print(f"{ERROR} Error banning user: {e}")

async def ban_all_users(guild):
    print(f"{ACTION} Banning all members (except bots, owner, and bot itself)...")
    members = [m for m in guild.members if not m.bot and m != guild.owner and m != bot.user]
    if not members:
        print(f"{WARN} No members to ban.")
        return
    for m in members:
        try:
            await guild.ban(m, reason="Mass ban by bot command")
            print(f"{SUCCESS} Banned {m}")
        except discord.Forbidden:
            print(f"{WARN} Missing permission to ban {m}")
        except Exception as e:
            print(f"{ERROR} Error banning {m}: {e}")
        await asyncio.sleep(DELAY)
    print(f"{SUCCESS} Completed mass ban.\n{DONE_ASCII}")

async def kick_user(guild):
    user_input = input(f"{GREEN}Enter the user ID or mention to kick:{RESET} ").strip()
    
    # Extract user ID from mention if needed
    if user_input.startswith('<@') and user_input.endswith('>'):
        user_id = user_input.replace('<@!', '').replace('<@', '').replace('>', '')
    else:
        user_id = user_input
    
    try:
        user_id = int(user_id)
    except ValueError:
        print(f"{ERROR} Invalid user ID.")
        return
    
    try:
        member = guild.get_member(user_id)
        if member is None:
            print(f"{ERROR} Member not found in the guild.")
            return
        
        if member == guild.owner:
            print(f"{WARN} Cannot kick the server owner.")
            return
        
        if member.bot:
            print(f"{WARN} Cannot kick a bot with this option.")
            return

        await member.kick(reason="Kicked by bot command")
        print(f"{SUCCESS} Kicked user {member} ({user_id})")
    except discord.Forbidden:
        print(f"{WARN} Missing permissions to kick user.")
    except Exception as e:
        print(f"{ERROR} Error kicking user: {e}")

async def kick_all_users(guild):
    print(f"{ACTION} Kicking all members (except bots, owner, and bot itself)...")
    members = [m for m in guild.members if not m.bot and m != guild.owner and m != bot.user]
    if not members:
        print(f"{WARN} No members to kick.")
        return
    for m in members:
        try:
            await m.kick(reason="Mass kick by bot command")
            print(f"{SUCCESS} Kicked {m}")
        except discord.Forbidden:
            print(f"{WARN} Missing permission to kick {m}")
        except Exception as e:
            print(f"{ERROR} Error kicking {m}: {e}")
        await asyncio.sleep(DELAY)
    print(f"{SUCCESS} Completed mass kick.\n{DONE_ASCII}")

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
        print("1\ufe0f\ufe0f Create Channels")
        print("2\ufe0f\ufe0f Delete All Channels")
        print("3\ufe0f\ufe0f Rename All Channels")
        print("4\ufe0f\ufe0f Kick All Bots")
        print("5\ufe0f\ufe0f Create Roles")
        print("6\ufe0f\ufe0f Rename All Roles")
        print("7\ufe0f\ufe0f Ban a User")
        print("8\ufe0f\ufe0f Ban All Users")
        print("9\ufe0f\ufe0f Kick All Users")
        print("10\ufe0f\ufe0f Exit\n")

        choice = get_input("Select option:", is_int=True, valid_choices=[0,1,2,3,4,6,7,8,9,10,11])

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

        elif choice == 6:
            c = get_input("Number of roles to create:", is_int=True)
            await create_roles(guild, c)

        elif choice == 7:
            prefix = get_input("New role prefix:", allow_cancel=True)
            if prefix != "cancel":
                await rename_all_roles(guild, prefix)
            else:
                print(f"{INFO} Cancelled.")

        elif choice == 8:
            await ban_user(guild)

        elif choice == 9:
            if input(f"{WARN} Confirm ban all users? This is destructive! (yes/cancel): ").lower() == "yes":
                await ban_all_users(guild)
            else:
                print(f"{INFO} Cancelled.")

        elif choice == 10:
            await kick_user(guild)

        elif choice == 11:
            if input(f"{WARN} Confirm kick all users? This is destructive! (yes/cancel): ").lower() == "yes":
                await kick_all_users(guild)
            else:
                print(f"{INFO} Cancelled.")

        elif choice == 0:
            print(f"{INFO} Bye \ud83d\udc4b")
            break

    await bot.close()

if __name__ == "__main__":
    TOKEN = get_input("Enter your bot token:")
    GUILD_ID = get_input("Enter your server (guild) ID:", is_int=True)
    bot.run(TOKEN)
