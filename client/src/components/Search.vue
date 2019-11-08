<template>
  <section class="hero is-success is-fullheight">
    <div class="hero-head">
      <header class="title">
        Spotty Search
      </header>
    </div>

    <div class="hero-body columns">
      <div class="column is-half is-offset-one-quarter">
        <b-field label="Artist" label-position="on-border" position="is-centered" type="is-danger">
          <b-input placeholder="Whitney Houston" v-model="searchForm.artist"></b-input>
        </b-field>

        <b-field label="Album" label-position="on-border">
          <b-input placeholder="The Bodyguard" v-model="searchForm.album"></b-input>
        </b-field>

        <b-field label="Track" label-position="on-border">
          <b-input placeholder="I Will Always Love You" v-model="searchForm.track"></b-input>
        </b-field>

        <b-field>
          <p class="control">
            <button class="button is-danger" native-type="submit" @submit="onSubmit">
              Search
            </button>
          </p>
        </b-field>
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
  name: 'Search',
  data() {
    return {
      msg: '',
      searchForm: {
        artist: '',
        album: '',
        track: '',
      },
    };
  },
  methods: {
    getMusic() {
      const path = 'http://localhost:5000/search';
      axios.get(path)
        .then((res) => {
          this.msg = res.data;
        })
        .catch((error) => {
          // eslint-diable-next-line
          console.error(error);
        });
    },
    searchMusic(payload) {
      const path = 'http://localhost:5000/search';
      axios.post(path, payload)
        .then(() => {
          this.getMusic();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getMusic();
        });
    },
    initForm() {
      this.searchForm.artist = '';
      this.searchForm.album = '';
      this.searchForm.track = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      const payload = {
        artist: this.searchForm.artist,
        album: this.searchForm.album,
        track: this.searchForm.track,
      };
      this.searchMusic(payload);
      this.initForm();
    },
  },
  created() {
    this.getMusic();
  },
};
</script>
