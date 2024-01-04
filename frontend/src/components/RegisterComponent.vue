<template>
    <div class="register-container">
        <div class="register-content">
            <div class="register-image">
                <img src="../assets/register.png" alt="register" />
            </div>
            <div class="login-space"></div>
            <div class="register-form">
                <h1>Register</h1>
                <form @submit.prevent="register" class="form">
                    <label for="firstname">First Name:</label>
                    <input type="text" v-model="firstname" id="firstname" class="input-field" />

                    <label for="lastname">Last Name:</label>
                    <input type="text" v-model="lastname" id="lastname" class="input-field" />

                    <label for="newUsername">Username:</label>
                    <input type="text" v-model="newUsername" id="newUsername" class="input-field" />

                    <label for="newPassword">Password:</label>
                    <input type="password" v-model="newPassword" id="newPassword" class="input-field" />

                    <label for="email">Email:</label>
                    <input type="text" v-model="email" id="email" class="input-field" />

                    <button type="submit" class="register-btn">Register</button>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
/**
 * RegisterComponent - A component for user registration.
 */
export default {
    name: "RegisterComponent",
    data() {
        /**
         * Component data properties.
         * @return {Object} - Initial data object.
         */
        return {
            firstname: "",
            lastname: "",
            newUsername: "",
            newPassword: "",
            email: "",
        };
    },
    methods: {
        /**
         * The user completes the registration process.
         * @method
         * @name register
         * @memberof RegisterComponent
         */
        register() {
            // Creating headers and request body for the API call
            var myHeaders = new Headers();
            myHeaders.append("Content-Type", "application/json");

            var raw = JSON.stringify({
                "firstname": this.firstname,
                "lastname": this.lastname,
                "username": this.newUsername,
                "password": this.newPassword,
                "email": this.email
            });

            // Configuring the Fetch API request options
            var requestOptions = {
                method: 'POST',
                headers: myHeaders,
                body: raw,
                redirect: 'follow'
            };

            // Making the API call to register the user
            fetch("http://localhost:5000/auth/register", requestOptions)
                .then(response => response.json())
                .then(result => {
                    console.log('res: ', result);

                    // Redirect to login page after successful registration
                    this.$router.push("/login");
                })
                .catch(error => console.log('error', error));

        },
    },
};
</script>
  
<style scoped>
.register-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 100px;
}

.register-content {
    display: flex;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    padding: 50px;
}

.register-image {
    flex: 1;
}

.register-image img {
    width: 100%;
    height: auto;
    padding-top: 80px;
}

.register-form {
    flex: 1;
    padding: 20px;
}

.login-space {
    width: 100px;
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

}

.register-btn {
    padding: 10px;
    background-color: #83C0BB;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    width: 100%;
}

.register-btn:hover {
    background-color: #088178;
}
</style>
  