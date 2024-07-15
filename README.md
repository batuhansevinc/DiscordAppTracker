# Discord App Tracker

A Discord bot designed to track the status of Android applications on the Google Play Store. The bot allows servers to set a notification channel, add/remove package names for tracking, and periodically check the status of these apps. Built with modularity and scalability in mind, adhering to OOP and SOLID principles.

## Features

- Set a notification channel for status updates.
- Add and remove package names for tracking.
- Periodically check the status of apps on the Google Play Store.
- Notify the channel when an app is published.

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/discord-app-tracker.git
    cd discord-app-tracker
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Configure the bot token:
    - Create a file named `config.json` in the root directory.
    - Add your Discord bot token to the `config.json` file as follows:
      ```json
      {
          "TOKEN": "YOUR_DISCORD_BOT_TOKEN"
      }
      ```

5. Run the bot:
    ```bash
    python main.py
    ```

## Usage

### Commands

- `/set_channel [channel]` - Sets the notification channel for this server.
- `/add_package [package_name]` - Adds a package name to the list.
- `/remove_package [package_name]` - Removes a package name from the list.
- `/list_packages` - Lists all package names in the list.
- `/check_status` - Checks the status of all package names in the list.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any changes.

## License

This project is licensed under the MIT License.
