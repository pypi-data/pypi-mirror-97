#!/bin/bash
# Commands used during survey creation

cmd__install() {
    # Install Python package
    activate_venv
    python3 -m pip install -U "$@"
    python3 $DIR/update_requirements.py "$@"
}

cmd__serve() {
    # Run Hemlock app locally
    echo "Prepare to get served."
    echo
    if [ $1 = False ]; then
        rm data.db
    fi
    export_env
    python3 app.py
}

cmd__rq() {
    # Run Hemlock Redis Queue locally
    export_env
    rq worker -u $REDIS_URL hemlock-task-queue
}

cmd__debug() {
    # Run debugger
    code="from hemlock.debug import AIParticipant, debug; \\
        debug($2, $3)"
    if [ $1 = True ]; then
        heroku run python -c"$code"
    else
        export_env
        python3 -c"$code"
    fi
}

activate_venv() {
    # Activate virtual environment and export local environment variables
    [ -d "hemlock-venv/bin" ] && . hemlock-venv/bin/activate
    [ -d "hemlock-venv/scripts" ] && . hemlock-venv/scripts/activate
}

export_env() {
    # Activate venv and export local environment variables
    activate_venv
    export `python3 $DIR/env/export_yaml.py env.yaml`
}