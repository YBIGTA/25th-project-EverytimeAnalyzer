<script setup>
import { defineEmits } from 'vue'

var topic1 = '';
var topic2 = '';
var topic3 = '';

const emit = defineEmits(['getRecommendLectureCodes']);

function request() {
  // fetch
  // emit data
  emit('getRecommendLectureCodes', ['lecture1', 'lecture2', 'lecture3'])
}

</script>

<template>
  <input type="text" v-model="topic1">
  <input type="text" v-model="topic2">
  <input type="text" v-model="topic3">
  <button @click="request"> submit </button>
</template>

<style scoped>

</style>