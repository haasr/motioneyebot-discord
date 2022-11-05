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


def print_section(text):
    print(f"\n\n{text}..\n", end='='*40)


def main():
    cwd = os.getcwd()
    print_section("Installing requirements")
    install_requirements()
    print_section("Writing start.bash file")
    write_start_bash_file(cwd)
    print_section("Applying execute permission")
    chmod_start_bash_file(cwd)
    print_section("Writing systemd service file")
    write_systemd_service_file(cwd)
    print_section("Copying service file to system folder")
    cp_systemd_service_file_to_sys(cwd)
    print_section("Enabling motioneyebot-discord service")
    enable_systemd_service_file()
    print_section("Ready!!")

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


if __name__ == '__main__':
    main()
