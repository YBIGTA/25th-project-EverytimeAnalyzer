<script setup>
import {reactive, ref} from 'vue'
import LectureTable from "@/components/LectureTable.vue";
import SearchBar from "@/components/SearchBar.vue";
import ReviewList from "@/components/ReivewList.vue";

const host = "http://localhost:8000"
// const sampleLectureCode = "UCE1105-01-00"

const lectureCodes = reactive({codes: []})
const reviewIdx = ref(-1)

function getRecommendLectureCodes(codes) {
  lectureCodes.codes = codes
}
</script>

<template>
  <SearchBar @getRecommendLectureCodes="getRecommendLectureCodes"/>

  <div class="lecture-table">
    <div v-for="(lectureCode, idx) in lectureCodes.codes" :key="idx">
      <LectureTable :host="host"
                    :path="'/lecture/'+lectureCode"
                    @click="reviewIdx=idx"
      />
    </div>
  </div>

  <div class="review-table">
    <div v-if="0 <= reviewIdx">
      <ReviewList :host="host"
                  :path="'/reviews/'+lectureCodes.codes[reviewIdx]"
<!--                  key값이 바뀌면 다시 랜더링한다.-->
                  :key="reviewIdx"
      />
    </div>
  </div>
</template>

<style>
.review-table {
  display: flex;
}

.lecture-table {
  display: flex;
}
</style>
