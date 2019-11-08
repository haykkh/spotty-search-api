<template>
  <section class="hero is-success is-fullheight">
    <div class="hero-head">
      <header class="title">
        Spotty-Search
      </header>
    </div>

    <div class="hero-body">
      <div class="container has-text-centered">
        <h1 class="title">
          {{ msg }}
        </h1>
        <h2 class="subtitle">
          Not {{ msg }}
        </h2>
      </div>
    </div>

    <div class="hero-foot">
      <div class="is-fullwidth">
        <p>
          made with ❤ by <a class="red" href="https://hayk.io">Հայկ</a>
        </p>
      </div>
    </div>

  </section>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Ping',
  data() {
    return {
      msg: '',
    };
  },
  methods: {
    getMessage() {
      const path = 'http://localhost:5000/ping';
      axios.get(path)
        .then((res) => {
          this.msg = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getMessage();
  },
};
</script>
