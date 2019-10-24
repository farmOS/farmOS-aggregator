import Vue from 'vue';
import Vuetify from 'vuetify';

Vue.use(Vuetify);

export default new Vuetify({
  icosn: {
    iconfont: 'mdi',
  },
  theme: {
    dark: false,
    themes: {
      light: {
        primary: '#336633', // farmos-green-dark: #336633;
        secondary: '#4e8b31', // farmos-green: #4e8b31;
        accent: '#60af32', // farmos-green-light: #60af32;
      },
      dark: {
        primary: '#336633', // farmos-green-dark: #336633;
        secondary: '#4e8b31', // farmos-green: #4e8b31;
        accent: '#60af32', // farmos-green-light: #60af32;
      },
    },
  },
});
