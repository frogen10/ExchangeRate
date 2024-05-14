<template>
  <Line :data="chartData" :options="options" />
</template>

<script lang="ts">
import 'chartjs-adapter-moment';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  TimeScale,
} from 'chart.js';
import { Line } from 'vue-chartjs';
import * as chartConfig from './Chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  TimeScale
);

export default {
  name: 'Chart',
  components: {
    Line,
  },
  data() {
    return chartConfig;
  },
};
</script>