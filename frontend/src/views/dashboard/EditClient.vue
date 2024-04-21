<template>
    <div class="page-add-client">
        <nav class="breadcrumb" aria-label="breadcrumbs">
            <ul>
                <li><router-link :to="{ name: 'Dashboard'}">Dashboard</router-link></li>
                <li><router-link :to="{ name: 'MyAccount'}">My account</router-link></li>
                <li class="is-active"><router-link :to="{ name: 'EditClient', params: { id: route.params.id }}" aria-current="true">Edit Profile</router-link></li>
            </ul>
        </nav>

        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title">Edit Profile - {{ client.first_name }}</h1>
            </div>

            <div class="column is-6">
                <div class="field">
                    <label>First Name</label>
                    
                    <div class="control">
                        <input type="text" name="first_name" class="input" v-model="client.first_name">
                    </div>
                </div>
                <div class="field">
                    <label>Last Name</label>
                    
                    <div class="control">
                        <input type="text" name="last_name" class="input" v-model="client.last_name">
                    </div>
                </div>
                <div class="field">
                    <label>Address 1</label>
                    
                    <div class="control">
                        <input type="text" name="address1" class="input" v-model="client.address1">
                    </div>
                </div>

                <div class="field">
                    <label>Address 2</label>
                    
                    <div class="control">
                        <input type="text" name="address2" class="input" v-model="client.address2">
                    </div>
                </div>
            </div>

            <div class="column is-6">
                <div class="field">
                    <label>Zipcode</label>
                    
                    <div class="control">
                        <input type="text" name="zipcode" class="input" v-model="client.zipcode">
                    </div>
                </div>

                <div class="field">
                    <label>Place</label>
                    
                    <div class="control">
                        <input type="text" name="place" class="input" v-model="client.place">
                    </div>
                </div>

                <div class="field">
                    <label>Country</label>
                    
                    <div class="control">
                        <input type="text" name="country" class="input" v-model="client.country">
                    </div>
                </div>
                <div class="field">
                    <label>Country</label>
                    
                    <div class="control">
                        <input type="text" name="number" class="input" v-model="client.number">
                    </div>
                </div>
            </div>

            <div class="column is-12">
                <div class="field">
                    <div class="control">
                        <button class="button is-success" @click="submitForm">Save changes</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


<script setup>
import { ref, onBeforeMount, computed } from 'vue';
import axios from 'axios';
import { toast } from 'bulma-toast';
import { useRouter, useRoute } from 'vue-router';
const router = useRouter();
const route = useRoute();

const client = ref({});
const getClient = async () => {
    const clientID = route.params.id;
    await axios.get(`/api/v1/clients/${clientID}`)
            .then(response => {
                client.value = response.data
            })
            .catch(error => {
                console.log(JSON.stringify(error))
            })
    };
onBeforeMount(getClient);

const submitForm = async () => {
    const clientID = route.params.id;

    try {
        await axios.patch(`/api/v1/clients/${clientID}/`, client.value);
        toast({
            message: 'The changes were saved',
            type: 'is-success',
            dismissible: true,
            pauseOnHover: true,
            duration: 2000,
            position: 'bottom-right',
        });
        router.push('/dashboard/clients');
    } catch (error) {
        console.log(JSON.stringify(error));
    }
};
</script>