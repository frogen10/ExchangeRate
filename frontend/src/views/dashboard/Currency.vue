<template>
    <h1>Currency {{ route.params.code }}</h1>
</template>
    
<script setup>
import { ref, onBeforeMount } from 'vue';
import axios from 'axios';
import { useStore } from 'vuex';
import { useRouter, useRoute } from 'vue-router';

const store = useStore();
const router = useRouter();
const route = useRoute();

</script>