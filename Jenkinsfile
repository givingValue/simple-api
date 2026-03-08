pipeline {
    agent any

    parameters {
        string(name: 'DOCKERHUB_USERNAME', defaultValue: '', description: 'DockerHub username (e.g. myuser)')
        string(name: 'IMAGE_TAG', defaultValue: 'latest', description: 'Docker image tag')
        string(name: 'INGRESS_HOST', defaultValue: 'simple-api.local', description: 'Hostname for Ingress (e.g. 1.2.3.4.sslip.io or api.yourdomain.com)')
    }

    environment {
        IMAGE_NAME = "simple-api"
    }

    stages {
        stage('Build') {
            steps {
                script {
                    docker.build("${params.DOCKERHUB_USERNAME}/${IMAGE_NAME}:${params.IMAGE_TAG}")
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-credentials') {
                        docker.image("${params.DOCKERHUB_USERNAME}/${IMAGE_NAME}:${params.IMAGE_TAG}").push()
                        if (params.IMAGE_TAG != 'latest') {
                            docker.image("${params.DOCKERHUB_USERNAME}/${IMAGE_NAME}:${params.IMAGE_TAG}").push('latest')
                        }
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig-file', variable: 'KUBECONFIG_FILE')]) {
                    dir('k8s') {
                        sh """
                            export KUBECONFIG=\${KUBECONFIG_FILE}
                            sed -i 's|DOCKERHUB_USERNAME|${params.DOCKERHUB_USERNAME}|g' deployment.yaml
                            sed -i 's|:latest|:${params.IMAGE_TAG}|g' deployment.yaml
                            sed -i 's|simple-api.local|${params.INGRESS_HOST}|g' ingress.yaml
                            kubectl apply -f namespace.yaml
                            kubectl apply -f deployment.yaml
                            kubectl apply -f service.yaml
                            kubectl apply -f ingress.yaml
                            kubectl rollout status deployment/simple-api -n simple-api
                        """
                    }
                }
            }
        }
    }

    post {
        success {
            echo "Deployment successful! API available at https://${params.INGRESS_HOST}"
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
