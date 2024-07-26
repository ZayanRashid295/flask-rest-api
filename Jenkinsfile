pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS_ID = 'your-dockerhub-credentials-id' // Docker credentials ID from Jenkins
        DOCKER_IMAGE = 'zayan/flask-api' // Docker Hub image name
        DOCKER_REGISTRY_URL = 'https://index.docker.io/v1/'
    }

    stages {
        stage('Checkout Code') {
            steps {
                script {
                    // Set the correct directory for cloning the repository
                    dir('/var/jenkins_home/workspace/Deploy-Flask-API') {
                        checkout scm
                    }
                }
            }
        }

        stage('Build Docker image') {
            steps {
                dir('/var/jenkins_home/workspace/Deploy-Flask-API') {
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
                sshagent (credentials: ['your-ssh-credentials-id']) { // SSH credentials ID from Jenkins
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
