**Twikit Discord Bot - Simplified Guide**

This guide will explain how to interact with the Twikit bot using slash commands. These commands start with a forward slash (`/`).

**Getting Help:**

* Use the **/help** command to see a list of all available commands and their descriptions.

**Managing Twitter Account Details:**

* **/set_account email password username:** This command allows you to update the email address, password, and username associated with the Twitter account the bot uses.
* **/get_account:** This command retrieves the current email address, password, and username associated with the Twitter account the bot uses.

**Controlling the Twitter Bot:**

* **/start_bot:** This command activates the Twitter bot and initiates its functionalities.
* **/stop_bot:** This command deactivates the Twitter bot and halts its functionalities.

**Managing Automatic Replies:**

* **/add_replies:** This command opens a form where you can enter a list of replies separated by semicolons (`;`). These replies will be used by the bot when it interacts with tweets.
* **/get_replies:** This command displays the current list of automatic replies configured for the bot.

**Monitoring Twitter Accounts:**

* **/watch_accounts:** This command opens a form where you can enter a list of Twitter usernames separated by semicolons (`;`). The bot will track these accounts for activity.
* **/get_watch_accounts:** This command displays the current list of Twitter accounts the bot is monitoring.

**Managing Secondary Accounts:**

* **/add_secondary_account email password username:** This command allows you to add details for secondary bots that will interact with the main bot.
* **/get_secondary_accounts:** This command displays the details (email & password) of the currently configured secondary accounts.
* **/remove_secondary_account username:** This command allows you to remove a specific secondary account identified by its username.

**Managing Secondary Account Replies:**

* **/add_secondary_replies:** This command opens a form where you can enter a list of replies separated by semicolons (`;`) for the secondary bots.
* **/get_secondary_replies:** This command displays the current list of automatic replies configured for the secondary bots.

**Important Notes:**

* This guide provides a simplified overview. Refer to the **/help** command for detailed descriptions of each command.
