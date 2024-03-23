<template>
  <div class="home">
    <h1 class="title">Welcome to Invoicely</h1>
    <div
                class="column is-3"
                v-for="exchange in exchanges"
                v-bind:key="exchange.id"
            >
                <div class="box">
                    <h3 class="is-size-4 mb-4">{{ exchange.name }}</h3>

                </div>
            </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Home',
  data() {
    return {
      exchanges: [

      ]
        }
    },
    mounted() {
        this.getExchange()
    },
    methods: {
        getExchange() {
            axios
                .get('/api/v1/exchange/')
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
