<template>
  <div>
   <svg class="circle-container" viewBox="2 -2 28 36" xmlns="http://www.w3.org/2000/svg">
     <circle class="circle-container__background" r="16" cx="16" cy="16"></circle>
     <circle
       class="circle-container__progress"
       r="16"
       cx="16"
       cy="16"
       :style="{strokeDashoffset: updateProgress()}"
     ></circle>
   </svg>
  </div>
</template>

<script>

// style="stroke-dashoffset: 25"
 export default {
    name: "ProgressCircle",
    props: { 
      percent: Number 
    },
    data () {
      return {
        perent_svg: 100
      }
    },
    methods: {
      updateProgress(){
        let val = this.percent;
        if(val>100) val=100;
        if(val<0) val=0;
        val=100-val;
        console.log("val=",val);
        if(val==100) {
          console.log("TODO: make circle empty...");
        }

        return val;
      },
    }
 }



</script>

<style>
:root {
  --dot-diameter: 70px;
  --circle-border-width: 4px;
  --default-color: #ddd;
  --completion-color: #2222aa;
}

.circle-container {
  width: var(--dot-diameter);
  height: var(--dot-diameter);
  transform: rotate(-90deg);
}

.circle-container__background {
  fill: none;
  stroke: var(--default-color);
  stroke-width: var(--circle-border-width);
}

.circle-container__progress {
  fill: none;
  stroke-linecap: round;
  stroke: var(--completion-color);
  stroke-dasharray: 100 100;
  stroke-linecap: round;
  stroke-width: var(--circle-border-width);
  transition: stroke-dashoffset 0.2s ease-in-out;
  will-change: transform;
}

</style>

