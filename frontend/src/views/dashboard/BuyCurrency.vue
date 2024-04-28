<template>
    <h1 class="title">Buy Currency {{ route.params.code }}</h1>
    <div>
        <label for="currency">Currency:</label>
          <select id="currency" v-model="fromCurrency">
          <option v-for="currency in exchanges" :key="currency.name" :value="currency.name">
            {{ currency.name }} - {{ currency.currency }}
          </option>
          </select>
          <label for="value">Value:</label>
          <input id="value" v-model.number="transactionValue" type="number" required>
          <p>Balance: {{ balance.value }} -> {{ balance.value - transactionValue }}</p>
          <p class="is-size-2 is-col-span-2 is-centered">
              {{transactionValue}} {{fromCurrency}} = {{ result }} {{ route.params.code }}
          </p>
          <button class="button is-success" @click="makeTransaction">Submit</button>
        <p>Time left: {{ timer }}</p>
    </div>
</template>
    
<script setup>
import { ref, onMounted, onBeforeMount, onUnmounted, computed, watch } from 'vue';
import axios from 'axios';
import { useStore } from 'vuex';
import { useRouter, useRoute } from 'vue-router';

const store = useStore();
const router = useRouter();
const route = useRoute();
const balances = ref([]);
const fromCurrency = ref('PLN');
const transactionStatus = ref('Pending');
let transactionTimer = null;
const transactionValue = ref(0);
const timer = ref(30);
let intervalId = null;
const exchanges = ref([]);
watch(fromCurrency, (newCurrency, oldCurrency) => {
    console.log(`Currency changed from ${oldCurrency} to ${newCurrency}`);
    fromRate.value = exchanges.value.find(currency => currency.name === newCurrency);
    balance.value = balances.value.find(balance => balance.currency === newCurrency);
});

watch(transactionValue, (newValue, oldValue) => {
    console.log(`Value changed from ${oldValue} to ${newValue}`);
    result.value = (newValue / toRate.value.bidValue * fromRate.value.askValue).toFixed(4);
});
const balance = ref({});
const fromRate = ref({});
const toRate = ref({ });
const result = ref(0.0);

onMounted(() => {
  intervalId = setInterval(() => {
    if (timer.value > 0) {
      timer.value--;
    } else {
      clearInterval(intervalId);
      if (transactionStatus.value === 'Started') {
        transactionStatus.value = 'Expired';
      }
      router.push({ name: 'Home' });
    }
  }, 1000);
});
const getBalance = async () => 
{
    await axios.get('/api/v1/balance/')
        .then(response => {
          balances.value = response.data;
          balance.value = balances.value.find(balance => balance.currency === fromCurrency.value);
        })
        .catch(error => {
          console.error(JSON.stringify(error));
        });
};

const getExchange = async () => {
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
              toRate.value = response.data[i];
              if(store.state.client.default_currency && toRate.value.name !== store.state.client.default_currency)
              { 
                fromCurrency.value = store.state.client.default_currency;
              }
            }
          }
          fromRate.value = exchanges.value.find(currency => currency.name === fromCurrency.value);
        }).catch(error => {
            console.error(JSON.stringify(error));
        });
      };
onBeforeMount(async()=>
{
    await getBalance();
    await getExchange();
});
onUnmounted(() => {
  clearInterval(intervalId);
});

function makeTransaction()
{
   
  // Implement your logic to check the balance here
  // If the balance is greater than the transaction value, send a request to the 'transaction' endpoint
  if (transactionValue.value>0 && balance.value.value - transactionValue.value >= 0) {
    axios.post('/api/v1/transactions/', {
        type: 'buy',
        value: transactionValue.value,
        from_currency: fromRate.value.id,
        to_currency: toRate.value.id
    })
    .then(() => {
      clearTimeout(transactionTimer);
      transactionStatus.value = 'Completed';
      router.push({ name: 'MyAccount' });
    })
    .catch(error => {
      console.error(JSON.stringify(error));
    });
  }
};
</script>