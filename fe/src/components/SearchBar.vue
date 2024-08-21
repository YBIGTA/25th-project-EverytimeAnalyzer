<script setup>
import {defineEmits} from 'vue'

// var topic1 = '';
// var topic2 = '';
// var topic3 = '';

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
  <div id="form-container">
    <div v-for="idx in 1" :key="idx">
      <div class="input-container">
        <label :v-for="'topic'+idx+'-form'">topic{{ idx }}</label>
        <input type="text" :id="'topic'+idx+'-form'">
      </div>
    </div>
    <button id="input-submit" @click="request"> submit</button>
  </div>

<!--  </div>-->
</template>

<style scoped>
#form-container {
  width: 50%;
  border: 1px solid aqua;
}
#input-submit {
  border-radius: 12px;
  width: 100px;
  height: 30px;
  background-color: #303245;
  color: white;

  position: relative;
  left: 600px;
  top: 10px;

}
.input-container {
  height: 50px;
  width: 700px;
  margin-top: 10px;
  display: flex;
}

input {
  box-sizing: border-box;
  height: 100%;
  width: 100%;
  padding: 4px 20px 0;
  border-radius: 12px;
  border: 0;
  background-color: #303245;
  color: #eee;
  font-size: 18px;
}
label {
  color: #65657b;
  font-size: 20px;
  line-height: 14px;

  position: relative;
  top: 20px;
  margin-right: 10px;
}

</style>