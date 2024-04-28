<template>
    <div>
      <h1 class="title">Change Balance</h1>
      <form @submit.prevent="changeBalance">
        <div v-for="balance in balances" v-bind:key="balance.id">
            <p>{{ balance.currency }}: </p>
            <input id="value" v-model="balance.value" type="number" required>
        </div>
        
  
        <button class="button" type="submit">Submit</button>
      </form>
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

onBeforeMount(async()=>
{
    await getBalance();
});

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

function changeBalance()
{
    balances.value.forEach(element => {
        axios.patch(`/api/v1/balance/${element.id}/`, { value: element.value, currency: element.currency})
        .then(response => {
            toast({
                message: 'Balance changed',
                type: 'is-success',
                dismissible: true,
                pauseOnHover: true,
                duration: 5000,
            });
            router.push({ name: 'MyAccount' });
        })
        .catch(error => {
            console.error(JSON.stringify(error));
            toast({
                message: 'Error changing balance',
                type: 'is-danger',
                dismissible: true,
                pauseOnHover: true,
                duration: 5000,
            });
        });
    });
    
}

</script>