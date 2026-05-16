pipeline {
agent any

stages {

stage('Install Dependencies') {
steps {
bat 'pip install -r requirements.txt'
}
}

// stage('Test') {
// steps {
// bat 'pytest'
// }
// }

stage('Build Docker Image') {
steps {
bat 'docker build -t airbnb-python .'
}
}

stage('Deploy Container') {
steps {
bat '''
docker stop airbnb || exit 0
docker rm airbnb || exit 0
docker run -d -p 5000:5000 ^
-v airbnb_data:/app ^
--name airbnb ^
airbnb-clone
'''
}
}
}
}