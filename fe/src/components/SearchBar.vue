<script setup>

var topic1 = '';
var topic2 = '';
var topic3 = '';

function showTopic() {
  console.log(topic1)
  console.log(topic2)
  console.log(topic3)
}

</script>

<template>
  <input type="text" v-model="topic1">
  <input type="text" v-model="topic2">
  <input type="text" v-model="topic3">
  <button @click="showTopic"> submit </button>
</template>

<style scoped>

</style>