import discord
import asyncio

intents = discord.Intents.default()
intents.guilds = True
intents.members = True  # Needed to manage members like kicking bots
bot = discord.Client(intents=intents)

def get_input(prompt, is_int=False, valid_choices=None, allow_cancel=False):
    while True:
        value = input(prompt).strip()
        if allow_cancel and value.lower() == 'cancel':
            return 'cancel'
        if is_int:
            try:
                ivalue = int(value)
                if valid_choices and ivalue not in valid_choices:
                    print(f"❗ Please enter a valid option: {valid_choices}")
                elif ivalue <= 0 and not valid_choices:
                    print("❗ Please enter a positive number.")
                else:
                    return ivalue
            except ValueError:
                print("❗ Invalid input. Please enter a number.")
        else:
            if value == "":
                print("❗ Input cannot be empty.")
            else:
                return value

async def kick_all_bots(guild):
    print(f"\n🚨 Starting to kick all bots in '{guild.name}'...")
    bots = [member for member in guild.members if member.bot]
    if not bots:
        print("✅ No bots found to kick.")
        return

    for bot_member in bots:
        try:
            await bot_member.kick(reason="Kicked by management script")
            print(f"✅ Kicked bot: {bot_member.name}#{bot_member.discriminator}")
        except discord.Forbidden:
            print(f"⚠️ Permission denied to kick: {bot_member.name}#{bot_member.discriminator}")
        except Exception as e:
            print(f"❗ Failed to kick {bot_member.name}#{bot_member.discriminator}: {e}")
        await asyncio.sleep(0.2)
    print("✅ Completed kicking all bots.\n")

async def delete_all_channels(guild):
    print(f"\n🚨 Deleting all channels in '{guild.name}'...")
    channels = list(guild.channels)
    batch_size = 5
    for i in range(0, len(channels), batch_size):
        batch = channels[i:i+batch_size]
        tasks = [channel.delete() for channel in batch]
        try:
            await asyncio.gather(*tasks)
            print(f"🗑️ Deleted batch {i // batch_size + 1} of channels.")
        except discord.Forbidden as e:
            print(f"⚠️ Missing permission or error during deletion: {e}")
        except Exception as e:
            print(f"❗ Error during deletion: {e}")
        await asyncio.sleep(0.1)
    print("✅ All deletable channels have been removed.\n")

async def create_channels(guild, num):
    print(f"\n✨ Creating {num} new channels...")
    batch_size = 5
    for i in range(0, num, batch_size):
        tasks = []
        for j in range(i, min(i + batch_size, num)):
            channel_name = f"🔝｜Sundar Bau {j+1}"
            tasks.append(guild.create_text_channel(channel_name))
        try:
            created = await asyncio.gather(*tasks)
            for ch in created:
                print(f"➕ Created channel: {ch.name}")
        except Exception as e:
            print(f"❗ Error creating channels: {e}")
        await asyncio.sleep(0.1)
    print("✅ Channel creation complete.\n")

async def rename_all_channels(guild, prefix="Sundar Bau"):
    print(f"\n✏️ Renaming all text and voice channels in '{guild.name}'...")
    channels = [c for c in guild.channels if isinstance(c, (discord.TextChannel, discord.VoiceChannel))]
    batch_size = 5
    for i in range(0, len(channels), batch_size):
        tasks = []
        for j, channel in enumerate(channels[i:i+batch_size], start=i+1):
            new_name = f"{prefix} {j}"
            tasks.append(channel.edit(name=new_name))
        try:
            await asyncio.gather(*tasks)
            print(f"✅ Renamed batch {(i // batch_size) + 1}")
        except discord.Forbidden as e:
            print(f"⚠️ Permission denied or error during renaming: {e}")
        except Exception as e:
            print(f"❗ Error during renaming: {e}")
        await asyncio.sleep(0.1)
    print("✅ Channel renaming complete.\n")

@bot.event
async def on_ready():
    print(f"[+] Logged in as: {bot.user} (ID: {bot.user.id})\n")
    guild = bot.get_guild(GUILD_ID)
    if guild is None:
        print("❗ Guild not found. Please verify the server ID.")
        await bot.close()
        return

    while True:
        print("Please select an action by typing the corresponding number:")
        print("1️⃣  Create channels")
        print("2️⃣  Delete all channels")
        print("3️⃣  Rename all channels (text & voice)")
        print("4️⃣  Kick all bots")
        print("0️⃣  Exit")

        choice = get_input("Your choice: ", is_int=True, valid_choices=[0,1,2,3,4])

        if choice == 1:
            while True:
                num_input = input("How many channels would you like to create? (Type 'cancel' to return to menu): ").strip()
                if num_input.lower() == 'cancel':
                    print("Operation cancelled. Returning to main menu.\n")
                    break
                if not num_input.isdigit() or int(num_input) <= 0:
                    print("❗ Please enter a valid positive number.")
                    continue
                num = int(num_input)
                print(f"✨ Starting creation of {num} channels...")
                await create_channels(guild, num)
                print(f"🎉 Successfully created {num} channels!\n")
                break

        elif choice == 2:
            confirm = input("⚠️ Are you absolutely sure you want to DELETE ALL CHANNELS? Type 'yes' to confirm or 'cancel' to abort: ").strip().lower()
            if confirm == "yes":
                await delete_all_channels(guild)
            else:
                print("Operation cancelled.\n")

        elif choice == 3:
            prefix = get_input("Enter new channel name prefix (or type 'cancel' to abort): ", allow_cancel=True)
            if prefix == 'cancel':
                print("Operation cancelled.\n")
            else:
                await rename_all_channels(guild, prefix)

        elif choice == 4:
            confirm = input("⚠️ Are you sure you want to KICK ALL BOTS? Type 'yes' to confirm or 'cancel' to abort: ").strip().lower()
            if confirm == "yes":
                await kick_all_bots(guild)
            else:
                print("Operation cancelled.\n")

        elif choice == 0:
            print("👋 Exiting script. Goodbye!")
            break

    await bot.close()

if __name__ == "__main__":
    TOKEN = get_input("Enter your bot token: ")
    GUILD_ID = get_input("Enter your Discord server (guild) ID: ", is_int=True)
    bot.run(TOKEN)   