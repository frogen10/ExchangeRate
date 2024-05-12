<template>
    <div class="page-dashboard">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title">Dashboard</h1>
            </div>

            <div class="column is-12">
                <div class="box">
                    <h2 class="subtitle">Transactions</h2>

                    <table class="table is-fullwidth">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Buy/Sell</th>
                                <th>Amount</th>
                                <th>Due date</th>
                                <th>From currency</th>
                                <th>To currency</th>
                                <th>Value</th>
                            </tr>
                        </thead>
                        <tr
                        v-for="(transaction, index) in transactions"
                        v-bind:key="transaction.id">
                            <th>{{ index + 1 }}</th>
                            <th>{{ transaction.type }}</th>
                            <th>{{ transaction.value }}</th>
                            <th>{{ moment(String(transaction.created_at)).format('YYYY-MM-DD HH:mm') }}</th>
                            <th>{{ transaction.from_currency.name }}</th>
                            <th>{{ transaction.to_currency.name }}</th>
                            <th>{{ (transaction.value * transaction.from_currency.bidValue/transaction.to_currency.askValue).toFixed(4) }}</th>
                    </tr>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onBeforeMount, computed } from 'vue';
import axios from 'axios';
import moment from 'moment';

const transactions = ref([]);
const getTransactions = async () => {
    try {
        const response = await axios.get(`/api/v1/transactions/`);
        for (let i = 0; i < response.data.length; i++) {
            const from_currency = await GetCurrency(response.data[i].from_currency);
            const to_currency = await GetCurrency(response.data[i].to_currency);
            transactions.value.push({
                id: response.data[i].id,
                type: response.data[i].type,
                value: response.data[i].value,
                created_at: response.data[i].created_at,
                from_currency: from_currency,
                to_currency: to_currency
            });
        }
    } catch (error) {
        console.log(JSON.stringify(error));
    }
};

async function GetCurrency(id) {
    const response = await axios.get(`/api/v1/exchange/${id}`, {
        credentials: 'omit'
    });
    return response.data;
}

onBeforeMount(getTransactions);
</script>