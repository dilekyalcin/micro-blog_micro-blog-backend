
# Micro-Blog Projesi Kurulumu

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
3. `micro-blog_micro-blog-backend` dizininde yer alan `docker-compose.yml` dosyasını `micro-blog` dizinine taşıyın
    ```bash
    mv micro-blog_micro-blog-backend/docker-compose.yml micro-blog/
    ```
4. Sonuç olarak `micro-blog_micro-blog-backend`, `micro-blog_micro-blog-frontend` ve `docker-compose.yml` dosyaları aynı dizinde olmalıdır.
5. `micro-blog` dizininde terminali açın.
6. Docker Desktop'ın açık olduğundan emin olun.
7. Docker Compose ile projeyi başlatın
    ```bash
    docker-compose up --build
    ```


