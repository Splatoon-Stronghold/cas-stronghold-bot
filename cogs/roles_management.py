from discord import Interaction, app_commands
from discord.ext import commands, tasks

from utils import config, env, google_auth, gsheet


class RoleManager(commands.Cog):
    """Cog for managing Discord roles based on Google Sheets data."""

    def __init__(self, bot: commands.Bot):
        """Initialize RoleManager cog."""
        self.bot: commands.Bot = bot
        self.SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
        self.creds = google_auth.get_authentication(self.SCOPES)
        self.flow = None
        self.id = config.get_config("google_sheet_id")
        self.sheet_name = config.get_config("google_sheet_name")
        self.service = gsheet.get_service(self.creds) if self.creds else None
        self.perm_guild_ids = [env.get_guild_id()]  # config info
        self.team_guild_ids = [env.get_guild_id()]  # config info

        self.main_guild_id = env.get_guild_id()

        self.logging_channel_name = env.get_logging_channel_name()
        self.logging_channels = {}

        for guild in bot.guilds:
            for channel in guild.channels:
                if channel.name == self.logging_channel_name:
                    self.logging_channels[guild.id] = channel

        self.discord_id_col = config.get_config("google_sheet_discordID_column")
        self.perm_role_col = config.get_config("google_sheet_position_role_column")
        self.team_role_col = config.get_config("google_sheet_team_role_column")

    def cog_unload(self) -> None:
        """Unload method. Called when Cog unloads."""
        try:
            self.update_roles.cancel()
        except Exception as e:
            print(f"Stopping the role updating failed - error: {e}")

    def cog_load(self) -> None:
        """Load method. Called when Cog loads."""
        try:
            self.update_roles.start()
        except Exception as e:
            print(f"Starting the role updating failed - error: {e}")

    # should make a start command or smth

    @app_commands.command(
        name="gsheet-auth",
        description="Authenticate the bot to access Stronghold google sheets - only the bot can see the auth token.",
    )
    @app_commands.checks.has_any_role("Admin")
    @app_commands.guilds(env.get_guild_id())
    @app_commands.guild_only()
    async def gsheet_auth(self, interaction: Interaction, code: str = "") -> None:
        """Authenticate the bot with Google Sheets."""
        response = interaction.response

        creds = google_auth.get_authentication(self.SCOPES)

        if creds:
            await response.send_message(
                content="You are already authenticated!",
                ephemeral=True,
            )
            self.service = gsheet.get_service(creds)
            return
        else:
            if code:
                try:
                    creds = google_auth.get_new_auth(self.flow, code)
                    self.service = gsheet.get_service(creds)
                    self.creds = creds
                    await response.send_message(
                        content="Successfully authenticated!",
                        ephemeral=True,
                    )
                    return
                except Exception as e:
                    await response.send_message(
                        content="Unknown error with authentication - please try again with a new link",
                        ephemeral=True,
                    )
                    print(e)
                    return
            else:
                try:
                    auth_link, self.flow = google_auth.get_authentication_link(self.SCOPES)
                except Exception as e:
                    print(e)
                    await response.send_message(
                        content="Unknown error with authentication - please contact the tech team and check logs",
                        ephemeral=True,
                    )
                    return

                await response.send_message(
                    content=(
                        "Please visit the following link and copy / note the access token given."
                        "\nPlease re-run this command, with that code as the input"
                        f"\nLink: {auth_link}"
                    ),
                    ephemeral=True,
                )
                return

    @app_commands.command(
        name="roles-sheet-select",
        description="Configure the google sheet to be used for role assignment.",
    )
    @app_commands.checks.has_any_role("Admin")
    @app_commands.guilds(env.get_guild_id())
    @app_commands.guild_only()
    @app_commands.describe(
        id="The ID of the Google Sheet that the bot should pull roles data from",
        sheet_name="The name of the tab / sheet within the Google Document (generally at the bottom)",
    )
    async def gsheet_select(self, interaction: Interaction, id: str = "", sheet_name: str = "") -> None:
        """Configure the Google Sheet for role assignment."""
        response = interaction.response
        if not self.service:
            await response.send_message(content="Update failed - please authenticate first", ephemeral=True)
            return

        if id and not sheet_name:
            await response.send_message(
                content="Update failed - please input a sheet id as well as name", ephemeral=True
            )
            return
        elif id:
            try:
                gsheet.get_sheet_data(self.service, id, sheet_name, roles=True)
                self.id = id
                self.sheet_name = sheet_name
                config.update_config("google_sheet_id", id)
                config.update_config("google_sheet_name", sheet_name)
                await response.send_message(
                    content=f"Success! - the new ID is: {id} and the new sheet name is: {sheet_name}", ephemeral=True
                )
                return

            except Exception as e:
                print(e)
                await response.send_message(
                    content="Update failed - please ensure sheet id and name are correct and match (can check logs).",
                    ephemeral=True,
                )
                return
        elif sheet_name:
            try:
                gsheet.get_sheet_data(self.service, self.id, sheet_name, roles=True)
                self.sheet_name = sheet_name
                config.update_config("google_sheet_name", sheet_name)
                await response.send_message(content=f"Success! - the new sheet name is: {sheet_name}", ephemeral=True)
                return

            except Exception as e:
                print(e)
                await response.send_message(
                    content="Update failed - please ensure sheet id and name are correct and match (can check logs).",
                    ephemeral=True,
                )
                return
        else:
            await response.send_message(
                content="Update failed - please enter a sheet id and / or sheet name.", ephemeral=True
            )
            return

    @app_commands.command(
        name="roles-sheet-config",
        description="Set the right columns for data in the roles sheet.",
    )
    @app_commands.checks.has_any_role("Admin")
    @app_commands.guilds(env.get_guild_id())
    @app_commands.guild_only()
    @app_commands.describe(
        discord_id_col_number="Convert the column for Discord IDs to a number (A = 1, B = 2, etc)",
        position_col_number="Convert the column for position role (e.g. staff) to a number (A = 1, B = 2, etc)",
        team_col_number="Convert the column for team roles to a number (A = 1, B = 2, etc)",
    )
    async def gsheet_config(
        self,
        interaction: Interaction,
        discord_id_col_number: int = -1,
        position_col_number: int = -1,
        team_col_number: int = -1,
    ) -> None:
        """Set the columns for Discord ID, position, and team roles."""
        response = interaction.response
        if not self.service:
            await response.send_message(content="Update failed - please authenticate first", ephemeral=True)
            return

        self.discord_id_col = self.discord_id_col if discord_id_col_number == -1 else discord_id_col_number - 1
        self.perm_role_col = self.perm_role_col if position_col_number == -1 else position_col_number - 1
        self.team_role_col = self.team_role_col if team_col_number == -1 else team_col_number - 1

        data = gsheet.get_sheet_data(self.service, self.id, self.sheet_name, roles=True)

        msg = ""

        try:
            perm_roles, team_roles, perm_strs, team_strs = await self.get_all_roles(
                data, self.perm_guild_ids, self.team_guild_ids
            )
            unfound_perm, unfound_team = self.get_unfound_roles(perm_roles), self.get_unfound_roles(team_roles)

            if unfound_perm or unfound_team:
                msg = (
                    f"Unfound position servers / roles: {unfound_perm}\n"
                    f"Unfound team servers / roles: {unfound_team}"
                )
                raise Exception("Unfound roles - see error message in Discord channel")

        except Exception as e:
            print(e)
            if msg:
                msg = (
                    "Error - values could not be updated due to unfound roles - please ensure they were typed correctly"
                    + "\n"
                    + msg
                )
                await response.send_message(content=msg, ephemeral=True)
            else:
                await response.send_message(content="Unknown error - please see logs", ephemeral=True)

            self.discord_id_col = config.get_config("google_sheet_discordID_column")
            self.perm_role_col = config.get_config("google_sheet_position_role_column")
            self.team_role_col = config.get_config("google_sheet_team_role_column")

            return

        self.discord_id_col = config.update_config("google_sheet_discordID_column", self.discord_id_col)
        self.perm_role_col = config.update_config("google_sheet_position_role_column", self.perm_role_col)
        self.team_role_col = config.update_config("google_sheet_team_role_column", self.team_role_col)

        await response.send_message(
            content=(
                f"Success! The sheet column values were updated to the following:\n"
                f"discordID column: {self.discord_id_col + 1}, "
                f"position role column: {self.perm_role_col + 1}, "
                f"team role column: {self.team_role_col + 1}"
            ),
            ephemeral=True,
        )

    @app_commands.command(
        name="roles-reset",
        description="Removes roles in the sheet (position and team) for the guilds in the environment",
    )
    @app_commands.checks.has_any_role("Admin")
    @app_commands.guilds(env.get_guild_id())
    @app_commands.guild_only()
    async def reset_roles(self, interaction: Interaction) -> None:
        """Remove all roles listed in the sheet for the configured guilds."""
        response = interaction.response
        if not self.service:
            await response.send_message(content="Update failed - please authenticate first", ephemeral=True)
            return
        data = gsheet.get_sheet_data(self.service, self.id, self.sheet_name, roles=True)

        perm_roles, team_roles, perm_strs, team_strs = await self.get_all_roles(
            data, self.perm_guild_ids, self.team_guild_ids
        )

        unfound_perm, unfound_team = self.get_unfound_roles(perm_roles), self.get_unfound_roles(team_roles)

        if unfound_perm or unfound_team:
            # Error probably - check what should be done here --> halt completely or remove what has been found
            await response.send_message(
                content=(
                    "Reset roles failed. Could not find the roles listed in the google sheet, in the following servers."
                    "\n"
                    "Please ensure the spelling and formatting of the sheet is correct and "
                    "matches the name of the discord roles."
                    f"\nUnfound position servers / roles: {unfound_perm}"
                    f"\nUnfound team servers / roles: {unfound_team}"
                ),
                ephemeral=True,
            )
            return

        await self.remove_roles(perm_roles)
        await self.remove_roles(team_roles)

        await response.send_message(
            content=(
                "Successfully reset roles!"
                f'\nRemoved the following position roles: {",".join(perm_strs)}'
                f'\n  In the following servers: {",".join([(self.bot.get_guild(v)).name for v in self.perm_guild_ids])}'
                f'\nRemoved the following team roles: {",".join(team_strs)}'
                f'\n  In the following servers: {",".join([(self.bot.get_guild(v)).name for v in self.team_guild_ids])}'
            ),
            ephemeral=True,
        )
        return

    @tasks.loop(minutes=1.0)
    async def update_roles(self) -> None:
        """Update roles for all users based on the Google Sheet."""
        if not self.service:
            await self.logging_channels[self.main_guild_id].send(
                content="Error - Google Sheets need to be authenticated before role update"
            )
            return
        data = gsheet.get_sheet_data(self.service, self.id, self.sheet_name, roles=True)

        perm_roles, team_roles, perm_strs, team_strs = await self.get_all_roles(
            data, self.perm_guild_ids, self.team_guild_ids
        )

        unfound_perm, unfound_team = self.get_unfound_roles(perm_roles), self.get_unfound_roles(team_roles)

        if unfound_perm or unfound_team:
            await self.logging_channels[self.main_guild_id].send(
                content=f"Unfound roles - position : {unfound_perm} and team : {unfound_team}"
            )
            return

        perm_completed, perm_errors = await self.add_roles(data, self.perm_role_col, perm_roles)
        team_completed, team_errors = await self.add_roles(data, self.team_role_col, team_roles)

        if not perm_errors and not team_errors:
            await self.logging_channels[self.main_guild_id].send(
                content=(
                    "Successfully updated all roles!"
                    "\nThe following roles were updated:\n"
                    + "\n".join([f"Guild: {v[0]} | Member: {v[1]} | Role: {v[2]}" for v in perm_completed])
                    + "\n"
                    + "\n".join([f"Guild: {v[0]} | Member: {v[1]} | Role: {v[2]}" for v in team_completed])
                )
            )
            return
        else:
            await self.logging_channels[self.main_guild_id].send(
                content=(
                    "Successfully updated some roles."
                    "\nThe following roles were updated:\n"
                    + "\n".join([f"Guild: {v[0]} | Member: {v[1]} | Role: {v[2]}" for v in perm_completed])
                    + "\n".join([f"Guild: {v[0]} | Member: {v[1]} | Role: {v[2]}" for v in team_completed])
                    + "\nThe following updates could not be made - see logs:"
                    + "\n".join([f"Guild: {v[0]} | Member: {v[1]} | Role: {v[2]}" for v in perm_errors])
                    + "\n".join([f"Guild: {v[0]} | Member: {v[1]} | Role: {v[2]}" for v in team_errors])
                )
            )
            return

    async def get_roles(self, role_set: set, guild_id: int) -> tuple[dict, dict]:
        """Get the roles by str from the sheet for a given guild."""
        guild = self.bot.get_guild(guild_id)
        roles = guild.roles
        found_roles = {}

        for role in roles:
            if role.name in role_set:
                found_roles[role.name] = role.id

        unfound = role_set - set(found_roles.keys())
        unfound_roles = {v: "" for v in unfound}

        return found_roles, unfound_roles

    def get_unique_roles(self, data: list, col: int) -> set:
        """Get unique roles from a column in the sheet data."""
        role_set = set()
        for row in data:
            for role_str in row[col].split(","):
                role_set.add(role_str.strip())
        role_set.discard("")
        return role_set

    async def get_all_roles(self, data: list, perm_guilds: list, team_guilds: list) -> tuple[dict, dict, set, set]:
        """Get all found and unfound roles for all inputted guilds."""
        perm_roles = {}
        perm_role_set = self.get_unique_roles(data, self.perm_role_col)
        team_role_set = self.get_unique_roles(data, self.team_role_col)

        for guild_id in perm_guilds:
            found_roles, unfound_roles = await self.get_roles(perm_role_set, guild_id)
            perm_roles[guild_id] = {
                "found": found_roles,
                "unfound": unfound_roles,
            }

        team_roles = {}
        for guild_id in team_guilds:
            found_roles, unfound_roles = await self.get_roles(team_role_set, guild_id)
            team_roles[guild_id] = {
                "found": found_roles,
                "unfound": unfound_roles,
            }

        return perm_roles, team_roles, perm_role_set, team_role_set

    def get_unfound_roles(self, roles_dict: dict) -> dict:
        """Return a dict of unfound roles for each guild."""
        unfound = {}
        for guild_id, roles in roles_dict.items():
            if roles["unfound"].values():
                unfound[guild_id] = roles["unfound"]
        return unfound

    async def remove_roles(self, roles_dict: dict) -> None:
        """Remove roles from all members for the given roles."""
        for guild_id in roles_dict.keys():
            guild = self.bot.get_guild(guild_id)
            roles = [guild.get_role(role_id) for role_id in roles_dict[guild_id]["found"].values()]
            for role in roles:
                for member in role.members:
                    await member.remove_roles(role)

    async def add_roles(self, data: list, col: int, roles_dict: dict) -> tuple[list, list]:
        """Add roles to members based on the sheet data."""
        completed = []  # each item is: (guild_id, member_id, role_name)
        # should it log unchanged roles?
        errors = []
        for row in data:
            member_id = row[self.discord_id_col]
            roles = row[col].split(",")

            for role_name in roles:
                for guild_id in roles_dict.keys():
                    try:
                        guild = self.bot.get_guild(guild_id)
                        member = await guild.fetch_member(member_id)
                        role_id = roles_dict[guild_id]["found"][role_name.strip()]
                        role = guild.get_role(role_id)

                        if role not in member.roles:
                            await member.add_roles(role)
                            completed.append((guild_id, member_id, role_name))
                    except Exception as e:
                        print(e)
                        errors.append((guild_id, member_id, role_name))
        return completed, errors
