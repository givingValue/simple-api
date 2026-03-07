pipeline { 

    agent any 

    stages { 
        stage('Hola') { 
            steps { 
                echo 'Hola Mundo desde Jenkins!' 
                echo 'El pipeline está funcionando correctamente.' 
            } 
        } 
        stage('Fecha y Hora') { 
            steps { 
                sh 'date' 
                sh 'whoami' 
            } 
        }
        stage('Verificar Ambiente') { 
            steps { 
                sh 'java -version' 
                sh 'echo Pipeline completado exitosamente' 
            } 
        } 
    } 
} 