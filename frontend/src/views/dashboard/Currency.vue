<template>
    <h1>Currency {{ route.params.code }}</h1>
    <div class="row is-narrow">
        <router-link :to="{ name:'SellCurrency', params: { code:currentCurrency.name }}" class="button box is-size-4 mb-4">Sell {{ currentCurrency.bidValue }}</router-link>
        <router-link :to="{ name:'BuyCurrency', params: { code:currentCurrency.name }}" class="button box is-size-4 mb-4">Buy {{ currentCurrency.askValue }}</router-link>
    </div>
    <select class="is-size-4 mb-4" name="selectedPeriod" v-model="selectedPeriod">
      <option v-for="period in periods">
        {{ period }}
      </option>
    </select>
</template>
    
<script setup>
import { ref, onBeforeMount, watch } from 'vue';
import axios from 'axios';
import { useStore } from 'vuex';
import { useRouter, useRoute } from 'vue-router';

const store = useStore();
const router = useRouter();
const route = useRoute();
const currentCurrency = ref({});
const periods = ['1D', '1W', '1M', '1Y', '5Y'];
const exchanges = ref([]);
const selectedPeriod = ref('1D');

watch(selectedPeriod, (newPeriod, oldPeriod) => {
    console.log(`Period changed from ${oldPeriod} to ${newPeriod}`);
    getDataToChart();
});


onBeforeMount(() => {
    getExchange();
});

const getExchange = async () => {
    try {
        const response = await axios.get(`/api/v1/exchange/?top=1&name=${route.params.code}`, {
            credentials: 'omit'
        });
        currentCurrency.value = response.data[0];
    } catch (error) {
        console.log(JSON.stringify(error));
    }
};

const getDataToChart = async () => {
    try {
        const response = await axios.get(`/api/v1/exchange/?period=${selectedPeriod}&name=${route.params.code}`, {
            credentials: 'omit'
        });
        exchanges.value = response.data;
    } catch (error) {
        console.log(JSON.stringify(error));
    }
};

</script>