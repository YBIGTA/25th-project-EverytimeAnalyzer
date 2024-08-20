<script setup>
import {ref, onMounted, defineProps} from 'vue'

const props = defineProps({
  host: String,
  path: String,
})
const reviewList = ref([])

onMounted(async () => {
  reviewList.value = await fetch(props.host + props.path)
      .then(response => response.json())
  // .then(out => out.slice(0, 10))
  reviewList.value = reviewList.value.slice(0, 8)
})

</script>

<template>
  <div id="review-container">
    <div v-for="review in reviewList" :key="review">
      <div class="review-container">
        <p> {{ review }}</p>
      </div>
    </div>

  </div>
</template>

<style scoped>
#review-container {
  margin: 40px;
  border: 1px solid black;
  height: 500px ;
  overflow-y: scroll;
}

#review-container::-webkit-scrollbar-thumb {
  background: #000;
}
#review-container::-webkit-scrollbar {
  width: 5px;
  height: 8px;
  background-color: #aaa; /* or add it to the track */
}

.review-container {
  margin-top: 20px;
  border: 1px solid black;
}


</style>