<template>
  <div>
    <b-table striped hover :items="items"></b-table>
  </div>
</template>

<script>
  import axios from 'axios'
  var item;


  export default {
    
    data() {
      return {
        items: [
          {location: 'loading...',moonset_time: 'loading...'}
        ]
      }
    },
    mounted() {
      axios({
        method: 'GET',
        url: 'http://localhost:3000/time'
      }).then(res => {
        this.items = res.data
      }).catch(res => {
        this.items = [
          {location: 'loading...',moonset_time: 'loading...3'}
        ]
        console.log(res)
      });
    }
  }
</script>