pipeline {
    agent any

    parameters {
        string(name: 'IMAGE_TAG', defaultValue: 'latest', description: 'Docker image tag')
    }

    environment {
        IMAGE_NAME = "simple-api"
        // DOCKERHUB_USERNAME and INGRESS_HOST: set in Manage Jenkins → System → Global properties → Environment variables
    }

    stages {
        stage('Validate') {
            steps {
                script {
                    if (!env.DOCKERHUB_USERNAME?.trim()) {
                        error 'DOCKERHUB_USERNAME is not set. Configure it in Manage Jenkins → System → Global properties → Environment variables'
                    }
                    if (!env.INGRESS_HOST?.trim()) {
                        error 'INGRESS_HOST is not set. Configure it in Manage Jenkins → System → Global properties → Environment variables'
                    }
                }
            }
        }
        stage('Build') {
            steps {
                script {
                    docker.build("${env.DOCKERHUB_USERNAME}/${IMAGE_NAME}:${params.IMAGE_TAG}")
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-credentials') {
                        docker.image("${env.DOCKERHUB_USERNAME}/${IMAGE_NAME}:${params.IMAGE_TAG}").push()
                        if (params.IMAGE_TAG != 'latest') {
                            docker.image("${env.DOCKERHUB_USERNAME}/${IMAGE_NAME}:${params.IMAGE_TAG}").push('latest')
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
                            sed -i 's|DOCKERHUB_USERNAME|${env.DOCKERHUB_USERNAME}|g' deployment.yaml
                            sed -i 's|:latest|:${params.IMAGE_TAG}|g' deployment.yaml
                            sed -i 's|simple-api.local|${env.INGRESS_HOST}|g' ingress.yaml
                            kubectl apply -f namespace.yaml
                            kubectl apply -f deployment.yaml
                            kubectl apply -f service.yaml
                            kubectl apply -f ingress.yaml
                            kubectl rollout restart deployment/simple-api -n simple-api
                            kubectl rollout status deployment/simple-api -n simple-api
                        """
                    }
                }
            }
        }
    }

    post {
        success {
            echo "Deployment successful! API available at https://${env.INGRESS_HOST}"
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
