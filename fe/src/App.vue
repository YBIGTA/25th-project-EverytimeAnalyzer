<script setup>
import {reactive, ref} from 'vue'
import LectureTable from "@/components/LectureTable.vue";
import SearchBar from "@/components/SearchBar.vue";
import ReviewList from "@/components/ReivewList.vue";
import LLMSummary from "@/components/LLMSummary.vue";

const host = "http://localhost:8000"
// const sampleLectureCode = "UCE1105-01-00"

const lectureCodes = reactive({codes: []})
const reviewIdx = ref(-1)

function getRecommendLectureCodes(codes) {
  lectureCodes.codes = codes
}
</script>

<template>
  <div class="container">
    <article>
      <SearchBar
          :host="host"
          path="/model"
          @getRecommendLectureCodes="getRecommendLectureCodes"/>
      <div v-if="0 <= reviewIdx">
        <LLMSummary
            :lectureCode="lectureCodes.codes[reviewIdx]"
            :key="reviewIdx"
        />
      </div>
    </article>
    <article :key="lectureCodes.codes">
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
                      :key="reviewIdx"
          />
        </div>
      </div>
    </article>
  </div>
</template>

<style>
.container {
  width: 100%;
  border: 1px solid blue;
  display: flex;
  justify-content: space-between;

}
article {
  width: 50%;
  border: 1px solid red;
}

article .lecture-table {
  display: flex;
}

article .review-table {
  border: 1px solid chocolate;
}
</style>
