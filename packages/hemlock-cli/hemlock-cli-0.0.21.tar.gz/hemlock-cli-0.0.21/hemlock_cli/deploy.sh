#!/bin/bash
# Deploy, scale, and destroy project

cmd__deploy() {
    # Deploy application
    echo
    echo "Deploying algorithm"
    git add .
    git commit -m "deploying algorithm"
    git push origin master
    remote_url=$(git remote get-url origin)
    python3 -m webbrowser "https://heroku.com/deploy?template=$remote_url"
}

# set_bucket_cors() {
#     # Set production bucket CORS permissions
#     # make sure gcp-credentials.json in repo
#     echo
#     if [ -z "$BUCKET" ]; then
#         echo "No bucket detected"
#         return
#     fi
#     echo "Setting CORS permissions on bucket $BUCKET for origin $URL_ROOT"
#     python3 $DIR/gcloud/create_cors.py $URL_ROOT
#     gsutil cors set cors.json gs://$BUCKET
#     rm cors.json
# }

cmd__update() {
    # Update application
    echo "Updating application"
    # set_bucket_cors
    git add .
    git commit -m "updating application"
    git push heroku master
    git push origin master
}

cmd__restart() {
    # Restart application
    echo "Restarting application"
    # set_bucket_cors
    heroku restart
}

cmd__destroy() {
    # Destroy applicaiton
    echo "Preparing to destroy application"
    # set_bucket_cors
    echo
    echo "Destroying application"
    heroku apps:destroy
}