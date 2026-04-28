pipeline {
    agent any

    environment {
        AWS_REGION = 'ap-south-1'
        ECR_REPO = 'cloudkart'
        EKS_CLUSTER = 'cloudkart-cluster'
        AWS_ACCOUNT_ID = '071564565553'
        IMAGE_TAG = "${BUILD_NUMBER}"
        IMAGE_URI = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}:${IMAGE_TAG}"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/Varun85535/cloudkart-devops.git'
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t $IMAGE_URI .'
            }
        }

        stage('Login to ECR') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'aws-creds', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    sh '''
                    aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
                    aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
                    aws configure set default.region $AWS_REGION
                    aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
                    '''
                }
            }
        }

        stage('Push Image to ECR') {
            steps {
                sh 'docker push $IMAGE_URI'
            }
        }

        stage('Deploy to EKS using Helm') {
            steps {
                sh '''
                aws eks update-kubeconfig --name $EKS_CLUSTER --region $AWS_REGION

                helm upgrade --install cloudkart ./helm/cloudkart \
                  --set image.repository=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO \
                  --set image.tag=$IMAGE_TAG

                kubectl rollout status deployment/cloudkart-deployment
                '''
            }
        }
    }

    post {
        success {
            echo 'CloudKart deployment completed successfully.'
        }
        failure {
            echo 'CloudKart deployment failed.'
        }
    }
}
