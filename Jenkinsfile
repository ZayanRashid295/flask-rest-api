pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS_ID = 'dockerhub-credentials' // Docker credentials ID from Jenkins
        DOCKER_IMAGE = 'your-dockerhub-username/flask-api' // Docker Hub image name
        DOCKER_REGISTRY_URL = 'https://index.docker.io/v1/'
    }

    stages {
        stage('Clone repository') {
            steps {
                dir('/Users/Zayan Rashid/Desktop/Flask') {
                    script {
                        // Assuming git clone has already been done locally
                        sh 'git pull'
                    }
                }
            }
        }

        stage('Build Docker image') {
            steps {
                dir('/Users/Zayan Rashid/Desktop/flask') {
                    script {
                        docker.build("${DOCKER_IMAGE}:${env.BUILD_NUMBER}")
                    }
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
                sshagent (credentials: ['vps-ssh-credentials']) { // SSH credentials ID from Jenkins
                    sh '''
                    ssh -o StrictHostKeyChecking=no user@your-vps-ip << EOF
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
