# Micro-Blog Projesi Docker Kurulumu

Önce 'micro-blog' adlı bir klasör oluşturun ve terminali bu dizinde açın:

   ```bash
   mkdir micro-blog
   cd micro-blog
   ```
1. Backend'i klonlayın ve geliştirme branch'ine geçin
    ```bash
    git clone https://github.com/dilekyalcin/micro-blog_micro-blog-backend.git
    cd micro-blog_micro-blog-backend
    git checkout dev
    cd ..
    ````
2. Frontend'i klonlayın ve geliştirme branch'ine geçin
    ```bash
    git clone https://github.com/dilekyalcin/micro-blog_micro-blog-frontend.git
    cd micro-blog_micro-blog-frontend
    git checkout dev
    cd ..
    ```
3. `micro-blog_micro-blog-backend` dizininde yer alan `docker-compose.yml` dosyasını ve `update-compose.sh` dosyasını`micro-blog` dizinine taşıyın
    ```bash
    mv micro-blog_micro-blog-backend/docker-compose.yml micro-blog/
    mv micro-blog_micro-blog-backend/update-compose.sh micro-blog/
    ```
4. Sonuç olarak `micro-blog_micro-blog-backend`, `micro-blog_micro-blog-frontend`, `docker-compose.yml` ve  `update-compose.sh` dosyaları aynı dizinde olmalıdır. 
5. `micro-blog` dizininde git bash terminalini açın.
6. Docker Desktop'ın açık olduğundan emin olun.
7. Script dosyası ile projeyi başlatın
    ```bash
    ./update-compose.sh
    ``` 
8. Proje geliştiricisinden Mongo_url isteyin ve kendi secret keyinizi giriniz.


# Micro-Blog Projesi Kubernetes Kurulumu

Önce 'micro-blog' adlı bir klasör oluşturun ve terminali bu dizinde açın:

   ```bash
   mkdir micro-blog
   cd micro-blog
   ```
1. Backend'i klonlayın ve geliştirme branch'ine geçin
    ```bash
    git clone https://github.com/dilekyalcin/micro-blog_micro-blog-backend.git
    cd micro-blog_micro-blog-backend
    git checkout dev
    cd ..
    ````
2. Frontend'i klonlayın ve geliştirme branch'ine geçin
    ```bash
    git clone https://github.com/dilekyalcin/micro-blog_micro-blog-frontend.git
    cd micro-blog_micro-blog-frontend
    git checkout dev
    cd ..
    ```
3. `micro-blog_micro-blog-backend` dizininde yer alan `k8s` klasörünü `micro-blog` dizinine taşıyın
    ```bash
    mv micro-blog_micro-blog-backend/k8s micro-blog/
    ```
4. Sonuç olarak `micro-blog_micro-blog-backend`, `micro-blog_micro-blog-frontend`, `k8s` klasörleri aynı dizinde olmalıdır.
5. Docker Desktop'ın açık olduğundan emin olun.
6. `minikube start` ile minikube başlatın ve `minikube addons enable ingress` komutunu çalıştırın.
7. `k8s` Klasörünün olduğu dizinde terminalde `backend-deployment.yaml`,`frontend-deployment.yaml`, `backend-service.yaml`,`frontend-service.yaml`, `app-ingress.yaml` dosyalarını create edin:
    ```bash
        kubectl apply -f backend-deployment.yaml
   ```
8. Aşağıdaki komut ile secret dosyası oluşturulmalı ve mongo_url doğru url ile değiştirilmeli
    ```bash
        kubectl create secret generic my-secrets `
    --from-literal=MONGO_URL="mongo_url" `
    --from-literal=JWT_SECRET_KEY="your_secret_key" `
    --from-literal=JWT_BLACKLIST_ENABLED="true" `
    --from-literal=JWT_BLACKLIST_TOKEN_CHECKS="access,refresh" `
    --from-literal=IMAGE_UPLOADS="uploads" `
    --from-literal=JWT_ACCESS_TOKEN_EXPIRES="86400"
    ```
9. `myblog.local/` ---> frontend ve `api.myblog.local/` ---> backend  ile sayfalara erişim sağlayabilirsiniz.
