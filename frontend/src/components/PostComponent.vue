<template>
    <div>
        <div class="container">
            <div class="content">
                <div class="new-post" v-if="isLoggedIn">
                    <h2>Create a new post</h2>
                    <div class="form-group">
                        <label for="newPostTitle">Title:</label>
                        <input id="newPostTitle" v-model="newPostTitle" placeholder="Enter the title">
                    </div>
                    <div class="form-group">
                        <label for="newPostContent">Content:</label>
                        <textarea id="newPostContent" v-model="newPostContent" placeholder="Write your post..."></textarea>
                    </div>
                    <button @click="createPost">Publish</button>
                </div>
                <div v-if="isLoggedIn">
                    <div class="card" v-for="item in posts" :key="item.id">
                        <p class="post-info">{{ item.author }}</p>
                        <p class="post-info"> Title: {{ item.title }}</p>
                        <p>{{ item.content }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    /**
     * BlogPage - Component for displaying blog posts and creating new posts.
     *
     * @name BlogPage
     * @export
     */
    name: "BlogPage",
    data() {
        return {
            posts: null,
            newPostContent: "",
            newPostTitle: "",
            author: "",
            isLoggedIn: false,
        };
    },
    mounted() {
        // When the page loads, check if the user is logged in and fetch all posts
        this.checkLoginStatus();
        this.getAllPosts();
    },
    methods: {
        /**
        * Checks user login status.
        *
        * @method
        * @name checkLoginStatus
        * @memberof BlogPage
        */
        checkLoginStatus() {
            var token = sessionStorage.getItem("token");
            this.isLoggedIn = !!token;
        },
        /**
         * Returns all texts.
         *
         * @method
         * @name getAllPosts
         * @memberof BlogPage
         */
        getAllPosts() {
            var token = sessionStorage.getItem("token");
            var myHeaders = new Headers();
            myHeaders.append("Authorization", "Bearer " + token);

            var requestOptions = {
                method: 'GET',
                headers: myHeaders,
                redirect: 'follow'
            };

            fetch("http://localhost:5000/post/get_all_posts", requestOptions)
                .then(response => response.json())
                .then(result => {
                    console.log('result get all posts: ', result);
                    this.posts = result;
                })
                .catch(error => console.log('error', error));

        },
        /**
        * Creates a new post.
        *
        * @method
        * @name createPost
        * @memberof BlogPage
        */
        createPost() {
            var token = sessionStorage.getItem("token");
            var myHeaders = new Headers();
            myHeaders.append("Authorization", "Bearer " + token);
            myHeaders.append("Content-Type", "application/json");

            var raw = JSON.stringify({
                title: this.newPostTitle,
                content: this.newPostContent,
                author: this.author
            });

            var requestOptions = {
                method: 'POST',
                headers: myHeaders,
                body: raw,
                redirect: 'follow',
            };
            fetch("http://localhost:5000/post/add_post", requestOptions)
                .then(response => response.json())
                .then(result => {
                    console.log('result create post: ', result);
                    this.newPostTitle = "";
                    this.newPostContent = "";
                    this.getAllPosts();
                })
                .catch(error => console.log('error', error));
        },
    }
};
</script>

<style scoped>
.container {
    width: 80%;
    margin: 0 auto;
}

.content {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
}

.new-post {
    width: 70%;
    margin: 2rem 0;
    padding: 3.5rem;
    border: 1px solid #ccc;
    border-radius: 5px;
    background-color: #f9f9f9;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
}

.form-group {
    margin-bottom: 1rem;
}

label {
    display: block;
    margin-bottom: 0.5rem;
}

input,
textarea {
    width: 100%;
    padding: 1rem;
    margin-bottom: 1rem;
    border: 1px solid #ccc;
    border-radius: 3px;
}

button {
    background-color: #248E87;
    color: white;
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 3px;
    cursor: pointer;
}

.card {
    background-color: #248E87;
    box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    width: 70%;
    min-height: 10rem;
    margin: 1rem 0;
    padding: 1rem;
}

.post-info {
    color: #fff;
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 0.5rem;
}
</style>