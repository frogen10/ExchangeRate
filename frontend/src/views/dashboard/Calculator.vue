<script setup>
import { ref, onBeforeMount, computed } from 'vue';
import axios from 'axios';
import { useStore}  from 'vuex';

const store = useStore();
const amount = ref(0);
const fromCurrency = ref('PLN');
const toCurrency = ref('PLN');
const currencies = ref([]);

const fetchData = async () => {
  try {
    const response = await axios.get('/api/v1/exchange/?top=1', {
            credentials: 'omit'
        });
    if(store.state.client.default_currency)
    {
      fromCurrency.value = store.state.client.default_currency;
      toCurrency.value = store.state.client.default_currency;
    }
    currencies.value = response.data.sort((a, b) => a.name.localeCompare(b.name));
    // Set fromCurrency as the first option in the select dropdown
    const fromCurrencyIndex = currencies.value.findIndex(currency => currency.name === fromCurrency.value);
    if (fromCurrencyIndex !== -1) {
      const [fromCurrencyOption] = currencies.value.splice(fromCurrencyIndex, 1);
      currencies.value.unshift(fromCurrencyOption);
    }
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
    <label class="is-size-2 mb-4" for="price">Price</label>
    <input class="is-size-4 mb-4" id="price" type="number" v-model="amount">
    <label class="is-size-2 mb-4" for="incurrency">In currency</label>
    <select class="is-size-4 mb-4" name="in_currency" v-model="fromCurrency">
      <option v-for="currency in currencies" :key="currency.name" :value="currency.name">
        {{ currency.name }} - {{ currency.currency }}
      </option>
    </select>
    <label class="is-size-2 mb-4" for="toCurrency">To currency</label>
    <select class="is-size-4 mb-4" name="to_Currency" v-model="toCurrency">
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