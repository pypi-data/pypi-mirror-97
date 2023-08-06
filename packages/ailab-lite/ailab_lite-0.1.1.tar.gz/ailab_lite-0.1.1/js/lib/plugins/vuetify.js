import Vue from 'vue';
import Vuetify from 'vuetify';
import 'vuetify/dist/vuetify.min.css';

Vue.use(Vuetify);

const opts = {
    theme: {
      dark: true,
      themes: {
        light: {
          white: "#FFFFFF",
          primary: "#e67345", // #E53935 // 489acc
          secondary: "#489acc", // #FFCDD2
          accent: "#6eb552", // #3F51B5
          fathomRed: "#d93840",
          fathomGreen: "#d93840",
          fathomBlack: "#3a3a3a",
          fathomPurple: "#3a3a3a",
          fathomWhite: "#eee",
          fathomBlue: "#489acc",
          fathomOrange: "#e67345",
          fathomYellow: "#f6ec4c",
          fathomGrey: "#3a3a3a",
          fathomLightGrey: "#bebebe"
        }
      }
    }
  };

export default new Vuetify(opts);