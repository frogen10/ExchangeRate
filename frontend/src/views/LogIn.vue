<template>
    <div class="page-login">
        <div class="columns">
            <div class="column is-4 is-offset-4">
                <h1 class="title">Log in</h1>

                <form @submit.prevent="submitForm">
                    <div class="field">
                        <label>Username</label>
                        <div class="control">
                            <input type="text" name="username" class="input" v-model="username">
                        </div>
                    </div>

                    <div class="field">
                        <label>Password</label>
                        <div class="control">
                            <input type="password" name="password" class="input" v-model="password">
                        </div>
                    </div>

                    <div class="notification is-danger" v-if="errors.length">
                        <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                    </div>

                    <div class="field">
                        <div class="control">
                            <button class="button is-success">Log in</button>
                        </div>
                    </div>
                </form>

                <hr>

                <router-link :to="{name:'SignUp'}">Click here</router-link> to sign up!
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onBeforeMount, computed } from 'vue';
import axios from 'axios';
import { toast } from 'bulma-toast';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';

const store = useStore();
const router = useRouter();
const username = ref('');
const password = ref('');
const errors = ref([]);
async function submitForm(e) 
{
    axios.defaults.headers.common["Authorization"] = ""

    localStorage.removeItem("token")

    const formData = {
        username: username.value,
        password: password.value
    }

    try {
        const response = await axios.post("/api/v1/token/login/", formData);
        const token = response.data.auth_token;
        store.commit('setToken', token);
        axios.defaults.headers.common["Authorization"] = `Token ${token}`;
        localStorage.setItem("token", token);
        const userResponse = await axios.get("/api/v1/users/me");
        const userData = userResponse.data;

        store.commit('setUser', { 'username': userData.username, 'id': userData.id });

        localStorage.setItem('username', userData.username);
        localStorage.setItem('userid', userData.id);

        router.push('/dashboard');
    } catch (error) {
        if (error.response) {
            for (const property in error.response.data) {
                errors.value.push(`${property}: ${error.response.data[property]}`);
            }

            console.log(JSON.stringify(error.response.data));
        } else if (error.message) {
            console.log(JSON.stringify(error.message));
        } else {
            console.log(JSON.stringify(error));
        }
    }
}
</script>