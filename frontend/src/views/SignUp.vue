<template>
    <div class="page-signup">
        <div class="columns">
            <div class="column is-4 is-offset-4">
                <h1 class="title">Sign up</h1>

                <form @submit.prevent="submitForm">
                   
                    <div class="field">
                        <label>E-mail</label>
                        <div class="control">
                            <input type="email" name="email" class="input" v-model="email">
                        </div>
                    </div>

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

                    <div class="field">
                        <label>Repeat Password</label>
                        <div class="control">
                            <input type="password" name="password" class="input" v-model="password2">
                        </div>
                    </div>

                    <div class="notification is-danger" v-if="errors.length">
                        <p 
                            v-for="error in errors" 
                            v-bind:key="error"
                        >
                            {{ error }}
                        </p>
                    </div>

                    <div class="field">
                        <div class="control">
                            <button class="button is-success">Sign up</button>
                        </div>
                    </div>
                </form>

                <hr>

                <router-link :to="{name:'LogIn'}">Click here</router-link> to log in!
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onBeforeMount, computed } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
const router = useRouter();

const client = ref({
    first_name: '',
    last_name: '',
    address1: '',
    address2: '',
    zipcode: '',
    place: '',
    country: '',
    number: ''
});
const email = ref('');
const username = ref('');
const password = ref('');
const password2 = ref('');
const errors = ref([]);

function submitForm(e) 
{
    if (password.value !== password2.value) {
        errors.value.push("Passwords do not match")
        return
    }
    const formData = {
        email: email.value,
        username: username.value,
        password: password.value
    }

    axios
        .post("/api/v1/users/", formData)
        .then(response => {
            console.log(response)
            router.push('/log-in')
        })
        .catch(error =>  {
        if (error.response) {
            errors.value = [];
            for (const property in error.response.data) {
                errors.value.push(`${property}: ${error.response.data[property]}`);
            }

            console.log(JSON.stringify(error.response.data));
        } else if (error.message) {
            console.log(JSON.stringify(error.message));
        } else {
            console.log(JSON.stringify(error));
        }
         
        })
}
</script>