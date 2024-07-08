import axios from "axios";

export default axios.create({
  //baseURL: process.env.ABKP_AXIOS_BASEURL,
  baseURL: "http://10.22.165.29:8080/api",
  //baseURL: "http://auto-backup-express-1:8080/api",
  
  headers: {
    "Content-type": "application/json"
  }
});
