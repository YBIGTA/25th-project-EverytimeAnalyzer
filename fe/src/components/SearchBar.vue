<script setup>
import {defineEmits} from 'vue'

var topic1 = '';
var topic2 = '';
var topic3 = '';

const emit = defineEmits(['getRecommendLectureCodes']);

function request() {
  // fetch
  // emit data
  emit('getRecommendLectureCodes',
      ['MST2220-02-00',
        'UCB1105-01-00',
        'SOC1002-02-00',
        'UCG1125-01-00',
      ]
  )
}

</script>

<template>
  <input type="text" v-model="topic1">
  <input type="text" v-model="topic2">
  <input type="text" v-model="topic3">
  <button @click="request"> submit</button>
</template>

<style scoped>

</style>