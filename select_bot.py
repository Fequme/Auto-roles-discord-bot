import discord
from discord.ext import commands
from discord.ext.commands import Bot
import config

client: Bot = commands.Bot(command_prefix="sm!", intents=discord.Intents.all())


class RoleSelect(discord.ui.Select):
    def __init__(self, options):
        super().__init__(placeholder='Выберите роль', options=options)

    async def callback(self, interaction):
        await interaction.response.defer()
        if not self.values:
            return

        deleted_roles = []
        added_roles = []
        for id_ in self.values:
            role = discord.utils.get(interaction.guild.roles, id=int(id_))
            if role in interaction.user.roles:
                await interaction.user.remove_roles(role)
                deleted_roles.append(role.mention)
            else:
                await interaction.user.add_roles(role)
                added_roles.append(role.mention)
        message = ""
        if added_roles:
            message += f"Добавленные роли: {', '.join(added_roles)}"
        else:
            message += "Добавленные роли: нету"
        if added_roles:
            message += "\n"
        if deleted_roles:
            message += f"Удаленные роли: {', '.join(deleted_roles)}"
        else:
            message += "Удалленные роли: нету"
        await interaction.followup.send(content=message, ephemeral=True)


@client.event
async def on_ready():

    text = f'''
██████╗░██╗░░░██╗  ██████╗░██╗░░░██╗███╗░░██╗██╗░░██╗
██╔══██╗╚██╗░██╔╝  ██╔══██╗╚██╗░██╔╝████╗░██║╚██╗██╔╝
██████╦╝░╚████╔╝░  ██████╔╝░╚████╔╝░██╔██╗██║░╚███╔╝░
██╔══██╗░░╚██╔╝░░  ██╔══██╗░░╚██╔╝░░██║╚████║░██╔██╗░
██████╦╝░░░██║░░░  ██║░░██║░░░██║░░░██║░╚███║██╔╝╚██╗
╚═════╝░░░░╚═╝░░░  ╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚══╝╚═╝░░╚═╝

 GITHUB : https://github.com/Fequme | Зашёл как : {client.user}

    '''
    print(f"{text}")
    profile_channel = client.get_channel(config.BOT_INFO['PROFILE_CHANNEL_ID'])
    await profile_channel.purge()
    await profile_channel.send(embed=discord.Embed(color=discord.Color.from_str("#2f3136")).set_image(url=config.BOT_INFO['FIRST_IMAGE_URL']))
    embed1 = discord.Embed(color=discord.Color.from_str("#2f3136"),
                           title=f"Под этим постом вы можете выбрать себе роль, нажав на соответствующую роли кнопку в меню выбора.")
    embed1.description = config.BOT_INFO['EMBED1_DESCRIPTION']
    embed1.set_image(url=config.BOT_INFO['STRIP_URL'])
    embed1.set_footer(
        text='Выбором в меню вы можете взять соответствующую смайлику роль. Также повторным нажатием — роль можно снять.')
    await profile_channel.send(embed=embed1,
                               view=discord.ui.View().add_item(RoleSelect(config.BOT_INFO['SELECT_OPTIONS1'])))
    await profile_channel.send(embed=discord.Embed(color=discord.Color.from_str("#2f3136")).set_image(url=config.BOT_INFO['SECOND_IMAGE_URL']))
    embed2 = discord.Embed(color=discord.Color.from_str("#2f3136"),
                           title=f"Под этим постом вы можете выбрать себе роль, нажав на соответствующую роли кнопку в меню выбора.")
    embed2.description = config.BOT_INFO['EMBED2_DESCRIPTION']
    embed2.set_image(url=config.BOT_INFO['STRIP_URL'])
    embed2.set_footer(
        text='Выбором в меню вы можете взять соответствующую смайлику роль. Также повторным нажатием — роль можно снять.')
    await profile_channel.send(embed=embed2,
                               view=discord.ui.View().add_item(RoleSelect(config.BOT_INFO['SELECT_OPTIONS2'])))

client.run(config.BOT_INFO['TOKEN'])
