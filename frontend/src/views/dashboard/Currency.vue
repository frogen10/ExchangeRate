<template>
    <title>Currency {{ route.params.code }}</title>
    <div class="row is-narrow">
        <router-link :to="{ name:'SellCurrency', params: { code:currentCurrency.name }}" class="button box is-size-4 mb-4">Sell {{ currentCurrency.bidValue }}</router-link>
        <router-link :to="{ name:'BuyCurrency', params: { code:currentCurrency.name }}" class="button box is-size-4 mb-4">Buy {{ currentCurrency.askValue }}</router-link>
    </div>
    <select class="is-size-4 mb-4" name="selectedPeriod" v-model="selectedPeriod">
      <option v-for="period in periods">
        {{ period }}
      </option>
    </select>
    <select class="is-size-4 mb-4 mx-4" name="toCurrency" v-model="toCurrency">
        <option v-for="currency in exchanges" :key="currency.name" :value="currency.name">
            {{ currency.name }} - {{ currency.currency }}
        </option>
    </select>
    <template v-if="loading">
        <div class="notification is-info">
            Loading...
        </div>
    </template>
    <template v-else>
        <Line :data="chartData" :options="options" ref="chartRef" />
    </template>
</template>
    
<script setup lang="ts">
import { ref, onBeforeMount, watch, computed } from 'vue';
import axios from 'axios';
import { useStore } from 'vuex';
import { useRouter, useRoute } from 'vue-router';
import { Line } from 'vue-chartjs'
import {chartData,options} from '../../components/Chart.js';
import 'chartjs-adapter-moment';
import moment from 'moment'
import { 
  CategoryScale, 
  LineElement, 
  LinearScale, 
  PointElement, 
  TimeScale,
  Legend,
  Title,
  Chart,
  Tooltip,
  update
} from 'chart.js';
Chart.register(
  CategoryScale,
  LinearScale,
  PointElement, 
  LineElement,
  Title,
  TimeScale,
  Legend,
  Tooltip
);

const store = useStore();
const router = useRouter();
const route = useRoute();
const currentCurrency = ref({});
const toCurrency = ref("PLN");
const periods = ['1D', '1W', '1M', '1Y', '5Y'];
const selectedPeriod = ref('1D');
const loading = ref(true);
const exchanges = ref([]);
if(store.state.client.default_currency && route.params.code !== store.state.client.default_currency)
{
    toCurrency.value = store.state.client.default_currency;
}
else if(route.params.code  == toCurrency.value)
{
    toCurrency.value = 'EUR';
}
watch(selectedPeriod, async (newPeriod, oldPeriod) => {
    console.log(`Period changed from ${oldPeriod} to ${newPeriod}`);
    await getDataToChart(newPeriod, toCurrency.value);
});

watch(toCurrency, async (newCurrency, oldCurrency) => {
    console.log(`Currency changed from ${oldCurrency} to ${newCurrency}`);
    await getDataToChart(selectedPeriod.value, newCurrency);
});

const chartRef = ref(null)
onBeforeMount(async() => {
    await getExchanges();
    await getDataToChart(selectedPeriod.value, toCurrency.value);
});

const getExchanges = async () => {
        exchanges.value = [];
        await axios.get('/api/v1/exchange/?top=1', {
            credentials: 'omit'
        }).then(response => 
        {
          for (let i = 0; i < response.data.length; i++) {
            if(response.data[i].name !== route.params.code)
            {
                exchanges.value.push(response.data[i]);
            }
            else
            {
                currentCurrency.value = response.data[i];
            }
          }
        }).catch(error => {
            console.error(JSON.stringify(error));
        });
};

async function getDataToChart(newPeriod, newCurrency) {
    loading.value = true;
    try {
        const response = await axios.get(`/api/v1/exchange/?day=${newPeriod}&from=${route.params.code}&to=${newCurrency}`, {
            credentials: 'omit'
        });
        chartData.labels = [];
        chartData.datasets[0].data = [];
        response.data.forEach(element => {
            chartData.labels.push(moment(String(element.date)).format('YYYY-MM-DD HH:mm:ss'));
            chartData.datasets[0].data.push(element.midValue)
        });
        chartData.datasets[0].label = response.data[0].currency
        if(newPeriod === '1D') {
            options.scales.x.time.unit = 'hour';
        } else if(newPeriod === '1W' || newPeriod === '1M') {
            options.scales.x.time.unit = 'day';
        }
        else
        {
            options.scales.x.time.unit = 'month';
        }
        loading.value = false;
    } catch (error) {
        console.log(JSON.stringify(error));
    }
};

</script>