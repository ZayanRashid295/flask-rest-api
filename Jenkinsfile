pipeline {
    agent {
        label 'docker-agent' // Node with Docker installed
    }

    environment {
        DOCKER_CREDENTIALS_ID = 'your-dockerhub-credentials-id'
        DOCKER_IMAGE = 'zayan/flask-api'
        DOCKER_REGISTRY_URL = 'https://index.docker.io/v1/'
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${env.BUILD_NUMBER}")
                }
            }
        }

        stage('Push Docker image') {
            steps {
                script {
                    docker.withRegistry(DOCKER_REGISTRY_URL, DOCKER_CREDENTIALS_ID) {
                        docker.image("${DOCKER_IMAGE}:${env.BUILD_NUMBER}").push()
                    }
                }
            }
        }

        stage('Deploy Docker containers') {
            steps {
                sshagent (credentials: ['your-ssh-credentials-id']) {
                    sh '''
                    ssh -o StrictHostKeyChecking=no zayan@your-vps-ip << EOF
                    cd /path/to/your/project
                    docker-compose down
                    docker-compose pull
                    docker-compose up -d
                    EOF
                    '''
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
