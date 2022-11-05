import os

def install_requirements():
    try:
        os.system("python3 install_requirements.py")
    except Exception as e:
        print(e)


def write_start_bash_file(cwd):
    with open(os.path.join(cwd, 'start.bash'), 'w') as start_script:
        start_script.write(
            f"#! /bin/bash -\n\n"

            f"cd {cwd}\n"
            f"source venv/bin/activate\n"
            f"python3 launch.py\n"
        )


def chmod_start_bash_file(cwd):
    cmd = f"sudo chmod 744 {os.path.join(cwd, 'start.bash')}"
    os.system(cmd)


def write_systemd_service_file(cwd):
    with open(os.path.join(cwd, 'motioneyebot-discord.service'), 'w') as service_file:
        service_file.write(
            f"Description=Motioneyebot Discord implementation\n\n"

            f"After=network-online.target\n"
            f"Wants=network-online.target systemd-networkd-wait-online.service\n\n"

            f"StartLimitIntervalSec=500\n"
            f"StartLimitBurst=5\n\n"

            f"[Service]\n"
            f"ExecStart={os.path.join(cwd, 'start.bash')}\n"
            f"Restart=on-failure\n"
            f"RestartSec=20s\n\n"

            f"[Install]\n"
            f"WantedBy=multi-user.target\n"
        )


def cp_systemd_service_file_to_sys(cwd):
    cmd = f"sudo cp {os.path.join(cwd, 'motioneyebot-discord.service')} /etc/systemd/system/"
    os.system(cmd)


def enable_systemd_service_file():
    os.system("sudo systemctl enable motioneyebot-discord.service")


def setup_tts():
    print("\nUse simple_google_tts to alert over speaker when motion detected?")
    print("\nRequires installing simple_google_tts (https://github.com/glutanimate/simple-google-tts).")
    use_tts = input("e to enable, d to disable (e/d) >>").lower()

    simple_google_tts_path = ""
    language = "en"

    if use_tts == 'e':
        satisfied = False
        while not satisfied:
            print_section("Specify the absolute path to the simple_google_tts")
            print("\n E.g., /home/pi/simple-google-tts")
            tts_path = input("\nAbsolute path (no filename) >>")
            s = input("Satisfied with your path (y/n)? >>").lower()
            satisfied = True if s == 'y' else False
        simple_google_tts_path = tts_path

        print_section("TTS: Use Pico (offline) or Google (online)?")
        
        use_offline = input("\np for Pico, g for Google (p/g)>>").lower()
        offline_selected = True if use_offline == 'p' else False

        satisfied = False
        while not satisfied:
            print_section("Enter the language code for TTS")
            lang_code = input("\nLanguage code (default is en) >>")
            s = input("Satisfied with your language code (y/n)? >>").lower()
            satisfied = True if s == 'y' else False
        language = lang_code

        message = ""
        satisfied = False
        while not satisfied:
            print_section("Enter the message you want spoken when a motion alert is received")
            message = input("\nYour message >>")
            s = input("Satisfied with your message (y/n)? >>").lower()
            satisfied = True if s == 'y' else False
        
        with open('tts_config.py', 'w') as tts_config:
            tts_config.write(
                f"use_simple_google_tts = True\n"
                f"simple_google_tts_path = \"{os.path.join(simple_google_tts_path, 'simple_google_tts')}\"\n"
                f"shell = '/usr/bin/bash'\n"
                f"use_offline = {offline_selected}\n"
                f"offline_language_code = '{language}'\n"
                f"motion_message = \"\"\"{message}\"\"\"\n"
            )
    else:
        with open('tts_config.py', 'w') as tts_config:
            tts_config.write(
                f"use_simple_google_tts = False\n"
                f"simple_google_tts_path = \"\"\n"
                f"shell = '/usr/bin/bash'\n"
                f"use_offline = True\n"
                f"offline_language_code = '{language}'\n"
                f"motion_message = 'Motion has been detected at the front door.'\n"
            )


def print_section(text):
    print(f"\n\n{text}..\n", end='='*40)


def main():
    cwd = os.getcwd()
    print_section("Installing requirements")
    install_requirements()
    print_section("Writing start.bash file")
    write_start_bash_file(cwd)
    #print_section("Applying execute permission")
    #chmod_start_bash_file(cwd)
    #print_section("Writing systemd service file")
    #write_systemd_service_file(cwd)
    #print_section("Copying service file to system folder")
    #cp_systemd_service_file_to_sys(cwd)
    #print_section("Enabling motioneyebot-discord service")
    #enable_systemd_service_file()
    print_section("Text to Speech")
    setup_tts()
    print_section("Ready!!")
    print("\n")

    '''
    print(
        f"\n\nAssuming you have entered all of the required environment\n"
        f"variables, you may now start the service.\n\n"
        f"Start service:\n"
        f"\tsudo systemctl start motioneyebot-discord\n\n"
        f"Check the status:\n"
        f"\tsytemctl status motioneyebot-discord\n\n"
        f"Stop service:\n"
        f"\tsudo systemctl stop motioneyebot-discord\n\n"
        f"Enable service (currently enabled):\n"
        f"\tsudo systemctl enable motioneyebot-discord\n\n"
        f"Disable service:\n"
        f"\tsudo systemctl disable motioneyebot-discord\n\n"
    )
    '''


if __name__ == '__main__':
    main()
