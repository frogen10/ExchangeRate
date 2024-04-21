<template>
    <div class="page-my-account">
        <nav class="breadcrumb" aria-label="breadcrumbs">
            <ul>
                <li><router-link :to="{name:'Dashboard'}">Dashboard</router-link></li>
                <li class="is-active"><router-link :to="{name:'MyAccount'}" aria-current="true">My account</router-link></li>
            </ul>
        </nav>

        <h1 class="title">My account</h1>
        <p><strong>Id: </strong>{{ store.state.user.id }}</p>
        <p><strong>Username: </strong>{{ store.state.user.username }}</p>
        <template v-if="client.length>0">
            <p><strong>First Name: </strong>{{ client[0].first_name }}</p>
            <p><strong>Last Name: </strong>{{ client[0].last_name }}</p>    
            <p><strong>Address 1: </strong>{{ client[0].address1 }}</p> 
            <p><strong>Address 2: </strong>{{ client[0].address2 }}</p>
            <p><strong>Zipcode: </strong>{{ client[0].zipcode }}</p>
            <p><strong>Place: </strong>{{ client[0].place }}</p>
            <p><strong>Country: </strong>{{ client[0].country }}</p>
            <p><strong>Number: </strong>{{ client[0].number }}</p>
                                    
        </template>
        <hr>

        <div class="buttons">
            <router-link :to="client.length > 0 ? { name: 'EditClient', params: { id: client[0].id } } : { name: 'AddClient' }" class="button is-light">
                Edit Profile
            </router-link>
            <button @click="logout()" class="button is-danger">Log out</button>
        </div>
    </div>
</template>

<script setup>
import { ref, onBeforeMount, computed } from 'vue';
import axios from 'axios';
import { toast } from 'bulma-toast';
import { useRouter, useRoute } from 'vue-router';
import { useStore } from 'vuex';

const store = useStore();
const router = useRouter();

const route = useRoute();

const client = ref([]);
const getClient = async () => {
    await axios.get(`/api/v1/clients/`)
            .then(response => {
                client.value = response.data
            })
            .catch(error => {
                console.log(JSON.stringify(error))
                client.value = null
            })
    };
onBeforeMount(getClient);
function logout ()
{
    try
    {
        axios.post("/api/v1/token/logout/");
        axios.defaults.headers.common["Authorization"] = ""
        localStorage.removeItem("username")
        localStorage.removeItem("userid")
        localStorage.removeItem("token")
        store.commit('removeToken')
        router.push('/')
    }
    catch (error)
    {
        if (error.response)
        {
            console.log(JSON.stringify(error.response.data))
        }
        else if (error.message)
        {
            console.log(JSON.stringify(error.message))
        }
        else
        {
            console.log(JSON.stringify(error))
        }
    }
};
</script>