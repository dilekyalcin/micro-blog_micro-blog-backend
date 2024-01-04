<template>
    <div class="login-container">
        <div class="login-content">
            <div class="login-image">
                <img src="../assets/login.png" alt="login">
            </div>
            <div class="login-space"></div>
            <div class="login-form">
                <h1>Login</h1>
                <form @submit.prevent="login" class="form">
                    <label for="username">Username:</label>
                    <input type="text" v-model="username" id="username" class="input-field" />

                    <label for="password">Password:</label>
                    <input type="password" v-model="password" id="password" class="input-field" />

                    <button type="submit" class="login-btn">Login</button>
                </form>
                <div class="alert-box" v-if="isError">
                    Your username or password is incorrect!
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    /**
     * LoginComponent - Component that provides user input.
     *
     * @name LoginComponent
     * @export
     */
    name: "LoginComponent",
    data() {
        /**
         * Component data fields.
         *
         * @return {Object} - Initial data object.
         */
        return {
            data: null,
            isError: false,
            username: '',
            password: '',
        };
    },
    methods: {
        /**
         * Manages user login.
         *
         * @method
         * @name login
         * @memberof LoginComponent
         */
        login() {
            var myHeaders = new Headers();
            myHeaders.append("Content-Type", "application/json");

            let raw = JSON.stringify({
                "username": this.username,
                "password": this.password
            })

            console.log(raw);
            var requestOptions = {
                method: 'POST',
                headers: myHeaders,
                body: raw,
                redirect: 'follow'
            };

            //If user is logged in, store token and redirect to home page
            fetch("http://localhost:5000/auth/login", requestOptions)
                .then(response => response.json())
                .then(result => {
                    if (result.access_token) {
                        sessionStorage.setItem("token", result.access_token)
                        this.$router.push("/")
                    } else {
                        this.isError = true
                        setTimeout(() => {
                            this.isError = false
                        }, 2000)

                        this.$router.push("/login");
                    }
                })
                .catch(error => console.log('error', error));
        }
    }
};
</script>

<style scoped>
.login-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 200px;
}

.login-content {
    display: flex;
    box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.1);
    padding: 20px;
}

.login-image {
    flex: 1;
}

.login-image img {
    width: 150%;
    height: 80%;
    padding-top: 40px
}

.login-space {
    width: 150px;
}

.login-form {
    flex: 1;
    padding: 100px;

}

.form {
    display: flex;
    flex-direction: column;
}

.input-field {
    padding: 10px;
    margin-bottom: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    width: 100%;
}

.login-btn {
    padding: 10px;
    background-color: #83C0BB;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    width: 110%;
}

.login-btn:hover {
    background-color: #088178;
}

.alert-box {
    margin-top: 1rem;
    background-color: red;
    padding: 1rem 1rem;
    width: 100%;
    color: white;
    font-weight: bold;
    font-size: 14px;
    border-radius: .25rem;
    font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
}
</style>
