<template>
    <div class="page-my-account">
        <nav class="breadcrumb" aria-label="breadcrumbs">
            <ul>
                <li><router-link :to="{name:'Dashboard'}">Dashboard</router-link></li>
                <li class="is-active"><router-link :to="{name:'MyAccount'}" aria-current="true">My account</router-link></li>
            </ul>
        </nav>
        <div class="columns">
            <div class="column">
                <h1 class="title">My account</h1>
                <p><strong>Id: </strong>{{ store.state.user.id }}</p>
                <p><strong>Username: </strong>{{ store.state.user.username }}</p>
                <template v-if="client">
                    <p><strong>First Name: </strong>{{ client.first_name }}</p>
                    <p><strong>Last Name: </strong>{{ client.last_name }}</p>    
                    <p><strong>Address 1: </strong>{{ client.address1 }}</p> 
                    <p><strong>Address 2: </strong>{{ client.address2 }}</p>
                    <p><strong>Zipcode: </strong>{{ client.zipcode }}</p>
                    <p><strong>Place: </strong>{{ client.place }}</p>
                    <p><strong>Country: </strong>{{ client.country }}</p>
                    <p><strong>Number: </strong>{{ client.number }}</p>
                </template>
            </div>
            <div class="column">
                <h1 class = "title"> My balance </h1>
                <div v-for="balance in balances" v-bind:key="balance.id">
                    <p v-if="client.default_currency === balance.currency">
                        <strong>{{ balance.currency }}: {{ balance.value.toFixed(4) }}</strong></p>
                    <p v-else>{{ balance.currency }}: {{ balance.value.toFixed(4) }}</p>
                </div>
            </div>
        </div>
        <hr>

        <div class="buttons">
            <router-link :to="client ? { name: 'EditClient' } : { name: 'AddClient' }" class="button is-light">
                Edit Profile
            </router-link>
            <router-link :to="{ name: 'ChangeBalance' }" class="button is-light">
                Change Balance
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
const balances = ref([]);
const client = ref({});

const GetClient = async () => 
{
    await axios.get(`/api/v1/clients/`)
        .then(response => {
            client.value = response.data[0];
            localStorage.setItem('clientid', response.data[0].id);
            localStorage.setItem('default_currency', response.data[0].default_currency);
            store.commit('setClient', { 'id': response.data[0].id, 'default_currency': response.data[0].default_currency});
        })
        .catch(error => {
            console.error(JSON.stringify(error));
        });
};
const getBalance = async () => 
{
    await axios.get('/api/v1/balance/')
        .then(response => {
          balances.value = response.data;
        })
        .catch(error => {
          console.error(JSON.stringify(error));
        });
};

onBeforeMount(async()=>
{
    await getBalance();
    await GetClient();
});
function logout ()
{
    try
    {
        axios.post("/api/v1/token/logout/");
        axios.defaults.headers.common["Authorization"] = ""
        localStorage.removeItem("username")
        localStorage.removeItem("userid")
        localStorage.removeItem("token")
        localStorage.removeItem("clientid")
        localStorage.removeItem("default_currency")
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