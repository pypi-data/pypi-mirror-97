#!/bin/bash
# Initialize Hemlock project

cmd__init() {
    # Initialize Hemlock project
    export project=$1
    export username=$2
    export token=$3
    export template_repo=$4
    export project_repo=https://github.com/$username/$project.git
    echo "Initializing hemlock project"
    clone_template
    create_repo
    echo
    echo "RUN THE FOLLOWING TO SETUP YOUR VIRTUAL ENVIRONMENT"
    echo "  $ cd $project"
    echo "  $ hlk setup-venv YOUR-OPERATING-SYSTEM"
    echo "replace YOUR-OPERATING-SYSTEM with win, mac, linux, or wsl"
}

clone_template() {
    echo
    echo "Cloning hemlock template from $template_repo"
    git clone $template_repo $project
    cd $project
    git remote rm origin
}

create_repo() {
    echo
    echo "Creating new hemlock project repo at $project_repo"
    curl -H "Authorization: token $token" https://api.github.com/user/repos \
        -d '{"name": "'"$project"'", "private": true}'
    git init
    git add .
    git commit -m "first commit"
    git remote add origin $project_repo
    git push origin master
}

cmd__setup_venv() {
    export OS=$1
    export name=$2
    if [ -z "$name" ]; then
        # kernel name is the name of the project folder
        export name=${PWD##*/}
    fi
    if [ $OS = win ]; then
        py -m venv hemlock-venv
        . hemlock-venv/scripts/activate
    else
        python3 -m venv hemlock-venv
        . hemlock-venv/bin/activate
    fi
    python3 -m pip install -r local-requirements.txt
    python3 -m ipykernel install --user --name $name
}

cmd__gcloud_bucket() {
    # Create gcloud project associated with Hemlock project
    echo
    echo "Creating gcloud project"
    project=${PWD##*/}
    project_id=`python3 $DIR/gcloud/gen_id.py $project`
    gcloud projects create $project_id --name $project
    gcloud alpha billing projects link $project_id \
        --billing-account $gcloud_billing_account
    create_gcloud_service_account
    create_gcloud_buckets
    python3 $DIR/env/update_yml.py env/local-env.yml BUCKET $local_bucket
    python3 $DIR/env/update_yml.py env/local-env.yml \
        GOOGLE_APPLICATION_CREDENTIALS 'env/gcp-credentials.json'
    python3 $DIR/env/update_yml.py env/production-env.yml BUCKET $bucket
    python3 $DIR/env/update_yml.py env/production-env.yml \
        GOOGLE_APPLICATION_CREDENTIALS 'env/gcp-credentials.json'
}

create_gcloud_service_account() {
    # Create gcloud project owner service account
    echo
    echo "Creating gcloud project service account"
    owner=$project-owner
    echo "  Creating service account $owner as owner of project $project_id"
    gcloud iam service-accounts create $owner --project $project_id
    gcloud projects add-iam-policy-binding $project_id \
        --member "serviceAccount:$owner@$project_id.iam.gserviceaccount.com" \
        --role "roles/owner"
    gcloud iam service-accounts keys create env/gcp-credentials.json \
        --iam-account $owner@$project_id.iam.gserviceaccount.com
}

create_gcloud_buckets() {
    # Create gcloud buckets
    echo
    echo "Creating gcloud buckets"
    local_bucket=`python3 $DIR/gcloud/gen_id.py $project-local-bucket`
    echo "  Making local bucket $local_bucket"
    gsutil mb -p $project_id gs://$local_bucket
    gsutil cors set $DIR/gcloud/cors.json gs://$local_bucket
    bucket=`python3 $DIR/gcloud/gen_id.py $project-bucket`
    echo "  Making production bucket $bucket"
    gsutil mb -p $project_id gs://$bucket
}