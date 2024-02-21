
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
3. `micro-blog_micro-blog-backend` dizininde yer alan `docker-compose.yml` dosyasını ve `update-compose.sh` dosyasını`micro-blog` dizinine taşıyın
    ```bash
    mv micro-blog_micro-blog-backend/docker-compose.yml micro-blog/
    mv micro-blog_micro-blog-backend/update-compose.sh micro-blog/
    ```
4. Sonuç olarak `micro-blog_micro-blog-backend`, `micro-blog_micro-blog-frontend`, `docker-compose.yml` ve  `update-compose.sh` dosyaları aynı dizinde olmalıdır. 
6. `micro-blog` dizininde git bash terminalini açın.
7. Docker Desktop'ın açık olduğundan emin olun.
8. Script dosyası ile projeyi başlatın
    ```bash
    ./update-compose.sh
    ``` 
9. Proje geliştiricisinden Mongo_url isteyin ve kendi secret keyinizi giriniz.


