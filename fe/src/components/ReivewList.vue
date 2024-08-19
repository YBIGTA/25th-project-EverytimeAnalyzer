<script setup>
import { ref, onMounted } from 'vue'
const reviewList = ref([])

onMounted(async () => {
  reviewList.value = await fetch("http://localhost:8000/reviews/UCE1105-01-00")
      .then(response => response.json())
      // .then(out => out.slice(0, 10))
  reviewList.value = reviewList.value.slice(0, 8)
})

</script>

<template>
  <div class="container">
    <div v-for="review in reviewList" :key="review">
      <p> {{ review }}</p>
      <p> ==== </p>
    </div>

  </div>
</template>

<style scoped>
.container {
  width: 300px;
}
</style>