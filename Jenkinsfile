
pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'moj-rejestr/node-app'
        DOCKER_TAG = 'latest'
        DOCKER_CREDENTIALS = 'docker-hub-credentials'
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Pobieranie kodu z repozytorium...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Instalowanie zależności...'
                sh 'npm install'
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Uruchamianie testów...'
                sh 'npm test'
            }
        }

        stage('Build Application') {
            steps {
                echo 'Budowanie aplikacji...'
                sh 'npm run build'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Budowanie obrazu Docker...'
                sh 'docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .'
            }
        }

        stage('Push Docker Image') {
            steps {
                echo 'Publikowanie obrazu Docker...'

                script {
                    docker.withRegistry(
                        'https://index.docker.io/v1/',
                        DOCKER_CREDENTIALS
                    ) {
                        docker.image(
                            "${DOCKER_IMAGE}:${DOCKER_TAG}"
                        ).push()
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline zakończony sukcesem!'
        }

        failure {
            echo 'Pipeline zakończony błędem!'
        }

        always {
            echo 'Zakończono wykonywanie pipeline.'
        }
    }
}
