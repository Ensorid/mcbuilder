import os
import time
import wget
import requests
import pyfiglet

from pystyle import Write, Colors, Center


def checkUpdate():
    api_url = f'https://api.github.com/repos/ensorid/mcbuilder/releases/latest'
    version = '1.0'
    try:
        response = requests.get(api_url)

        if response.status_code == 200:
            latest_release = response.json()
            latest_version = latest_release['tag_name']

            if latest_version > version:
                return Colors.yellow + f'\nA new version ({latest_version}) is available! https://github.com/ensorid/mcbuilder'
            else:
                return Colors.green + f'\nYou are using the latest version.'
        else:
            return Colors.red + f'\nError: {response.status_code} - Unable to fetch release data.'
    except Exception as e:
        return Colors.red + f'\nError: {str(e)} - Unable to check for updates.'


print(Center.XCenter(Colors.cyan + pyfiglet.figlet_format("MCBUILDER")))
print(checkUpdate())

time.sleep(1)

correct_server = False
correct_version = False

spigot = {
    "1.7": "https://cdn.getbukkit.org/spigot/spigot-1.7.10-SNAPSHOT-b1657.jar",
    "1.8": "https://cdn.getbukkit.org/spigot/spigot-1.8.8-R0.1-SNAPSHOT-latest.jar",
    "1.9": "https://cdn.getbukkit.org/spigot/spigot-1.9.4-R0.1-SNAPSHOT-latest.jar",
    "1.10": "https://cdn.getbukkit.org/spigot/spigot-1.10.2-R0.1-SNAPSHOT-latest.jar",
    "1.11": "https://cdn.getbukkit.org/spigot/spigot-1.11.2.jar",
    "1.12": "https://cdn.getbukkit.org/spigot/spigot-1.12.2.jar",
    "1.13": "https://cdn.getbukkit.org/spigot/spigot-1.13.2.jar",
    "1.14": "https://cdn.getbukkit.org/spigot/spigot-1.14.4.jar",
    "1.15": "https://cdn.getbukkit.org/spigot/spigot-1.15.2.jar",
    "1.16": "https://cdn.getbukkit.org/spigot/spigot-1.16.5.jar",
    "1.17": "https://download.getbukkit.org/spigot/spigot-1.17.1.jar",
    "1.18": "https://download.getbukkit.org/spigot/spigot-1.18.2.jar",
    "1.19": "https://download.getbukkit.org/spigot/spigot-1.19.4.jar",
    "1.20": "https://download.getbukkit.org/spigot/spigot-1.20.1.jar"
}

while not correct_version:
    Write.Print("Available version : 1.7, 1.8, 1.9, 1.10, 1.11, 1.12, 1.13, 1.14, 1.15, 1.16, 1.17, 1.18, 1.19, 1.20\n",
                Colors.yellow_to_green, interval=0.01)
    mcversion = Write.Input("What version do you want to install ? : ", Colors.blue_to_green, interval=0.01)

    if mcversion == "1.7" or mcversion == "1.8" or mcversion == "1.9" or mcversion == "1.10" or mcversion == "1.11" or mcversion == "1.12" or mcversion == "1.13" or mcversion == "1.14" or mcversion == "1.15" or mcversion == "1.16" or mcversion == "1.17" or mcversion == "1.18" or mcversion == "1.19" or mcversion == "1.20":
        correct_version = True

print()

while not correct_server:
    Write.Print(f"Available server : Spigot\n", Colors.yellow_to_green, interval=0.01)
    mcserver = Write.Input("What server do you want to install ? : ", Colors.blue_to_green, interval=0.01).lower()

    if mcserver == "spigot":
        correct_server = True
        user_directory = os.getcwd()
        filename = "server.jar"
        subfolder_name = "server"
        subfolder_path = os.path.join(user_directory, subfolder_name)
        output_file = os.path.join(subfolder_path, filename)
        os.makedirs(subfolder_path, exist_ok=True)
        wget.download(spigot[mcversion], out=output_file)

        with open("server/eula.txt", "w") as file:
            file.write(f"eula=true")

        port = Write.Input(f"\nEnter the port you want to use for your server ? (default : 25565) : ",
                           Colors.blue_to_green, interval=0.01)
        if port:
            with open("server/server.properties", "a") as file:
                file.write(f"server-port={port}\n")

        online = Write.Input(f"\nDo you want to verify user authentication ? (true/false) : ",
                             Colors.blue_to_green, interval=0.01).lower()
        if online:
            with open("server/server.properties", "a") as file:
                file.write(f"online-mode={online}\n")

        players = Write.Input(f"\nHow many players can join the server simultaneous ?: ",
                             Colors.blue_to_green, interval=0.01)
        if players:
            with open("server/server.properties", "a") as file:
                file.write(f"max-players={players}\n")

        whitelist = Write.Input(f"\nDo you want to enable the whitelist ? (true/false) : ",
                              Colors.blue_to_green, interval=0.01).lower()
        if whitelist:
            with open("server/server.properties", "a") as file:
                file.write(f"white-list={whitelist}\n")

        ram = Write.Input(f"\nEnter the MB of RAM you want to allow for your server : ", Colors.blue_to_green,
                          interval=0.01)

        with open("server/start.bat", "w") as file:
            file.write(f"@echo off\njava -jar -Xmx{ram}M server.jar\n")

        Write.Print(f"\nThe server will start in 5 seconds. Once the server is fully ready, please write stop into "
                    f"the console", Colors.blue_to_white, interval=0.01)
        time.sleep(5)
        os.system("cls & cd server & start.bat")
        Write.Print(f"\nYour server is ready! Don't forget to move the server folder to the desired location!", Colors.blue_to_white, interval=0.01)
