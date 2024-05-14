<template>
    <h1 class="title">Sell Currency {{ route.params.code }}</h1>
    <div class="columns">
      <div class="column is-half">
        <label class="m-2" for="currency">Currency:</label>
        <div class="m-2">
          <label for="currency">Currency:</label>
          <select id="currency" v-model="toCurrency">
            <option v-for="currency in exchanges" :key="currency.name" :value="currency.name">
              {{ currency.name }} - {{ currency.currency }}
            </option>
          </select>
        </div>
        <div style="clear: both;"></div>
        <div class="m-2">
          <label for="value">Value:</label>
          <input id="value" v-model.number="transactionValue" type="number" required>
        </div>
        <p class="m-2">Balance: {{ balance.value }} -> {{ balance.value - transactionValue }}</p>
        <p class="m-2">
          {{transactionValue}} {{ route.params.code }} = {{ result }} {{toCurrency}} 
        </p>
        <button class="button is-success" @click="makeTransaction">Submit</button>
        <p class="m-2">Time left: {{ timer }}</p>
        </div>
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
const toCurrency = ref('PLN');
const transactionStatus = ref('Pending');
let transactionTimer = null;
const transactionValue = ref(0);
const timer = ref(30);
let intervalId = null;
const exchanges = ref([]);
watch(toCurrency, (newCurrency, oldCurrency) => {
    console.log(`Currency changed from ${oldCurrency} to ${newCurrency}`);
    toRate.value = exchanges.value.find(currency => currency.name === newCurrency);
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
          balance.value = balances.value.find(balance => balance.currency === route.params.code);
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
                fromRate.value = response.data[i];
              if(store.state.client.default_currency && fromRate.value.name !== store.state.client.default_currency)
              { 
                toCurrency.value = store.state.client.default_currency;
              }
            }
          }
          toRate.value = exchanges.value.find(currency => currency.name === toCurrency.value);
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
        type: 'sell',
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