#!/bin/bash

GREEN='\033[0;32m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m' # No Color

spinner() {
    PID=$!
    i=1
    sp="/-\|"
    echo -n ' '
    while [ -d /proc/$PID ]; do
        printf "\b${sp:i++%${#sp}:1}"
        sleep 0.2
    done
    echo -n '    '
}

print_header() {
    echo -e "${CYAN}=============================="
    echo -e "           Homecloud          "
    echo -e "==============================${NC}"
    echo -e "version 0.1 (${RED}ALPHA${NC})\n\n"
}

upgrade_system() {
    sudo apt-get update -y
    sudo apt-get upgrade -y
}

install_python_tkinter() {
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}Python not found. Installing...${NC}"
        sudo apt-get install -y python3
    fi

    python3 -c 'import tkinter' 2>/dev/null
    if [ $? -ne 0 ]; then
        echo -e "${RED}Tkinter module not found. Installing...${NC}"
        sudo apt-get install -y python3-tk
    fi
}

install_pip() {
    if ! command -v pip3 &> /dev/null; then
        echo -e "${RED}pip not found. Installing...${NC}"
        sudo apt-get install -y python3-pip
    fi
}

install_venv() {
    if ! python3 -m venv --help &> /dev/null; then
        echo -e "${RED}venv module not found. Installing...${NC}"
        sudo apt-get install -y python3-venv
    fi
    # Force venv installation to prevent false positives
    sudo apt-get install -y python3-venv
}

install_git() {
    if ! command -v git &> /dev/null; then
        echo -e "${RED}Git not found. Installing...${NC}"
        sudo apt-get install -y git
    fi
}

check_existing() {
    if [ -d "./application" ]; then
        echo -e "${RED}Application folder already exists.${NC}"
        echo -e "${GREEN}Cleaning envrionment...${NC}"
        rm -rf "./application"
    fi
}

clone_repo() {
    echo -e "${CYAN}Installing required application files...${NC}"
    mkdir application && cd application
    if git clone -n --depth=1 --filter=tree:0 https://github.com/mario26rgl/homecloud-iot/ ./ &> /dev/null; then
        git sparse-checkout set --no-cone application
        git checkout
        chmod +x ./application/scripts/init.sh
        echo -e "${GREEN}Files installed successfully!${NC}"
    else
        echo -e "${RED}Failed to install application files! Please check your internet connection.${NC}"
fi
}

create_shortcut() {
    echo -e "${CYAN}Creating a Desktop shortcut...${NC}"
    CURRENT_DIR=$(pwd)
    ICON_PATH="${CURRENT_DIR}/application/images/icon.png"

    echo "[Desktop Entry]" > /home/pi/Desktop/HomeCloud.desktop
    echo "Name=HomeCloud" >> /home/pi/Desktop/HomeCloud.desktop
    echo "Comment=This is the HomeCloud application launcher" >> /home/pi/Desktop/HomeCloud.desktop
    echo "Exec=python3 login.py" >> /home/pi/Desktop/HomeCloud.desktop
    echo "Icon=${ICON_PATH}" >> /home/pi/Desktop/HomeCloud.desktop
    echo "Terminal=false" >> /home/pi/Desktop/HomeCloud.desktop
    echo "Type=Application" >> /home/pi/Desktop/HomeCloud.desktop
    echo "Categories=Utility;" >> /home/pi/Desktop/HomeCloud.desktop
    echo "Path=${CURRENT_DIR}/application" >> /home/pi/Desktop/HomeCloud.desktop

    chmod +x /home/pi/Desktop/HomeCloud.desktop
}

print_header

echo -e "${GREEN}Please wait while we install the required modules and application files...${NC}"
{
upgrade_system
install_python_tkinter
install_pip
install_venv
install_git
check_existing
clone_repo
create_shortcut
} & spinner

echo -e "\033[1m${CYAN}Application installation ${GREEN}COMPLETE\033[0m${NC}"


