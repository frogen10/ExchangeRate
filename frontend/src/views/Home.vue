<template>
  <div class="home">
    <h1 class="title">Welcome to ExchangeRate</h1>
    <template v-if="exchanges.length>0">
    <div v-for="exchange in exchanges" v-bind:key="exchange.id">
        <router-link :to="{ name:'Currency', params: { code:exchange.name }}">
            <div class="box columns is-mobile is-multiline is-centered mb-4">
                <div class="column is-narrow">
                    <p class="is-size-4 mb-4">{{ exchange.name }}</p>
                    <p class="is-size-2 mb-2">{{ exchange.midValue }}</p>
                </div>
                <div class="column is-narrow">
                    <router-link :to="{ name:'SellCurrency', params: { code:exchange.name }}" class="button box is-size-4 mb-4">Sell {{ exchange.bidValue }}</router-link>
                    <router-link :to="{ name:'BuyCurrency', params: { code:exchange.name }}" class="button box is-size-4 mb-4">Buy {{ exchange.askValue }}</router-link>
                </div>
            </div>
        </router-link>
    </div>
    </template>
    <template v-else>
        <p> Something went wrong </p>
    </template>
  </div>
</template>

<script setup>
import { ref, onBeforeMount } from 'vue';
import axios from 'axios';
import { useStore } from 'vuex';

const store = useStore();

const exchanges = ref([]);

const getExchange = async () => {
    try {
        const response = await axios.get('/api/v1/exchange/?top=1', {
            credentials: 'omit'
        });
        const default_currency = ref('PLN');
        if(store.state.client && store.state.client.default_currency)
        {
            console.log('Default currency found: '+store.state.client.default_currency);
            default_currency.value = store.state.client.default_currency;
        }
        else
        {
            console.log('Default currency not found');
        }
        for (let i = 0; i < response.data.length; i++) {
            if(response.data[i].name !== default_currency.value)
            {
                exchanges.value.push(response.data[i]);
            }
            else
            {
                console.log('Default currency: '+default_currency.value);
            }
        }
    } catch (error) {
        console.log(JSON.stringify(error));
    }
};

onBeforeMount(getExchange);
</script>