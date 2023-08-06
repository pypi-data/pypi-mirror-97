#!/bin/bash
# Setup for recommended software

cmd__setup() {
    export OS=$1
    if [ $2 = True ]; then chrome_setup; fi
    if [ $3 = True ]; then chromedriver_setup; fi
    if [ $4 = True ]; then heroku_cli_setup; fi
}

redis() {
    # Start redis server
    apt install -f -y redis-server
    service redis-server start
}

chrome_setup() {
    # set chrome as the default browser
    # should only have to do this on WSL
    if [ $OS = win ]; then
        echo "This should not be necessary on Windows"
    elif [ $OS = wsl ]; then
        # https://www.gregbrisebois.com/posts/chromedriver-in-wsl2/
        apt-get install -f -y curl unzip xvfb libxi6 libgconf-2-4
        curl -o google-chrome.deb \
            https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
        apt install ./google-chrome.deb
        rm google-chrome.deb
        echo
        echo "Google chrome setup complete"
        echo "Verify your installation with"
        echo "$ google-chrome-stable --version"
    elif [ $OS = mac ]; then
        echo "This should not be necessary on Mac"
    elif [ $OS = linux ]; then
        echo "This should not be necessary on Linux"
    fi
}

chromedriver_setup() {
    echo "Installing Chromedriver"
    get_chromedriver_file
    if [ $OS = wsl ]; then
        # https://www.gregbrisebois.com/posts/chromedriver-in-wsl2/
        mv chromedriver /usr/bin/chromedriver
        chown root:root /usr/bin/chromedriver
        chmod +x /usr/bin/chromedriver
        echo
        echo "Chromedriver setup complete"
        echo "Verify your installation with"
        echo "$ chromedriver --version"
        return
    fi
    if [ ! -d $HOME/webdrivers ]; then mkdir $HOME/webdrivers; fi
    mv chromedriver $HOME/webdrivers
    TO_ADD="export PATH=\"$HOME/webdrivers:\$PATH\""
    if [ -n "$ZSH_VERSION" ]; then
        # add chromedriver to path for zsh profile
        python3 $DIR/add_profile.py zsh "$TO_ADD"
    fi
    if [ -n "$BASH_VERSION" ]; then
        # add chromedriver to path for bash profile
        python3 $DIR/add_profile.py bash "$TO_ADD"
    fi
    echo
    echo "Chromedriver setup complete"
    echo "Close and re-open your terminal, then verify your installation with"
    echo "$ chromedriver --version"
}

get_chromedriver_file() {
    # download and unzip the chromedriver file
    echo
    echo "1. Go to this URL: https://chromedriver.chromium.org/downloads"
    echo "2. Click the link to the download folder associated with your version of Google Chrome"
    echo "3. Copy the download URL associated with your OS. It should look like: https://chromedriver.storage.googleapis.com/86.0.4240.22/chromedriver_linux64.zip"
    echo "Note: If using WSL2, use the Linux download URL"
    echo -n "4. Paste the URL here: "
    read chromedriver_url
    curl -o chromedriver.zip $chromedriver_url
    apt install -f -y unzip
    unzip chromedriver.zip
    rm chromedriver.zip
}

heroku_cli_setup() {
    if [ $OS = win ]; then
        echo "Download heroku-cli from https://devcenter.heroku.com/articles/heroku-cli"
        return
    fi
    echo "Installing Heroku-CLI"
    curl https://cli-assets.heroku.com/install.sh | sh
    echo
    echo "Opening Heroku login page"
    echo "  NOTE: You may have to open this page manually"
    heroku login
    echo
    echo "Heroku-cli setup complete"
    echo "Verify your heroku-cli installation with"
    echo "heroku --version"
}