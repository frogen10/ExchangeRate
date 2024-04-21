<script setup>
import { ref, onBeforeMount, computed } from 'vue';
import axios from 'axios';

const amount = ref(0);
const fromCurrency = ref('PLN');
const toCurrency = ref('PLN');
const currencies = ref([{ name: 'PLN', currency:"polski złoty", midValue: 1 }]);

const fetchData = async () => {
  try {
    const response = await axios.get('/api/v1/exchange/?top=1', {
            credentials: 'omit'
        });
    currencies.value = [...currencies.value, ...response.data];
  } catch (error) {
    console.error(error);
  }
};

const result = computed(() => {
  const fromRate = currencies.value.find(currency => currency.name === fromCurrency.value).midValue;
  const toRate = currencies.value.find(currency => currency.name === toCurrency.value).midValue;
  return (amount.value / toRate * fromRate).toFixed(4);
});

onBeforeMount(fetchData);
</script>

<template>
  <div class="box fixed-grid is-mobile is-centered mb-4">
  <div class="grid">
    <label class="is-size-2 mb-4" for="kwota">Kwota </label>
    <input class="is-size-4 mb-4" id="kwota" type="number" v-model="amount">
    <label class="is-size-2 mb-4" for="wwalucie">W walucie </label>
    <select class="is-size-4 mb-4" name="currency" v-model="fromCurrency">
      <option v-for="currency in currencies" :key="currency.name" :value="currency.name">
        {{ currency.name }} - {{ currency.currency }}
      </option>
    </select>
    <label class="is-size-2 mb-4" for="dlawaluty">Dla waluty</label>
    <select class="is-size-4 mb-4" name="toCurrency" v-model="toCurrency">
      <option v-for="currency in currencies" :key="currency.name" :value="currency.name">
        {{ currency.name }} - {{ currency.currency }}
      </option>
    </select>
    <p class="is-size-2 is-col-span-2 is-centered">
      {{amount}} {{fromCurrency}} = {{ result }} {{ toCurrency }}
    </p>
  </div>
</div>
</template>