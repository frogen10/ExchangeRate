<template>
  <div class="home">
    <h1 class="title">Welcome to ExchangeRate</h1>
    <template v-if="exchanges.length>0">
    <div
                class="box columns is-mobile is-multiline is-centered mb-4"
                v-for="exchange in exchanges"
                v-bind:key="exchange.id"
            >
                    <div class="column is-narrow">
                        <p class="is-size-4 mb-4">{{ exchange.name }}</p>
                        <p class="is-size-2 mb-2">{{ exchange.midValue }}</p>
                    </div>
                    <div class="column is-narrow">
                        <button class="button box is-size-4 mb-4" >Sell {{ exchange.bidValue }}</button>
                        <button class="button box is-size-4 mb-4">Buy {{ exchange.askValue }}</button>
                    </div>
    </div>
    </template>
    <template v-else>
        <p> Something went wrong </p>
    </template>
  </div>
</template>

<script>
import axios from 'axios'
import LogIn from './LogIn.vue';
import { computed } from 'vue';

export default {
  name: 'Home',
  data() {
    return {
        exchanges: [],
        exchanges2: [],
        groups: {}
        }
    },
    mounted() {
        this.getExchange()
    },
    methods: {
        getExchange() {
            axios
                .get('/api/v1/exchange/?top=1',{ 
                credentials: 'omit'
                })
                .then(response => {
                    for (let i = 0; i < response.data.length; i++) {
                        this.exchanges.push(response.data[i])
                    }
                })
                .catch(error => {
                    console.log(JSON.stringify(error))
                })
        }
        
    }
}
</script>
