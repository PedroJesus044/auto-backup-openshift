<template>
    <div class="list row">
      <div class="col-md-3">
        <h4>Backups list</h4>
        <ul class="list-group">

          <li class="list-group-item"
            :class="{ active: index == currentIndex }"
            v-for="(tutorial, index) in backups"
            :key="index"
            @click="setActiveTutorial(tutorial, index) ,this.retreiveMetadata()"
          >
          <div class="container">
              <div class="row">
                  <div class="col">
                    {{ tutorial.name }}
                  </div>
                  <div class="col-">

                    <div class="float-right spinner-grow spinner-grow-sm m-1" role="status" v-if="status[index]=='[RUNNING]'" :key="index"></div>

                    <div class="float-right sm mr-1" role="status" v-if="status[index]=='success'" :key="index">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-check-circle-fill" viewBox="0 0 16 16">
                        <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0m-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
                      </svg>
                    </div>

                    <div class="float-right sm mr-1" role="status" v-if="status[index]=='warning'" :key="index">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-exclamation-circle-fill" viewBox="0 0 16 16">
                        <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M8 4a.905.905 0 0 0-.9.995l.35 3.507a.552.552 0 0 0 1.1 0l.35-3.507A.905.905 0 0 0 8 4m.002 6a1 1 0 1 0 0 2 1 1 0 0 0 0-2"/>
                      </svg>
                    </div>

                    <div class="float-right sm mr-1" role="status" v-if="status[index]=='failure'" :key="index">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-circle-fill" viewBox="0 0 16 16">
                        <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293z"/>
                      </svg>
                    </div>

                  </div>
              </div>
          </div>
          </li>
          
          <li class="list-group-item">
            <div class="input-group">
              <input @keypress.enter="addBackup" v-model="name" id="name" name="name" type="text" class="form-control" placeholder="+ Añadir" aria-label="Username" aria-describedby="basic-addon1">
            </div>
          </li>
        </ul>
      </div>
      <div class="col-md-4">
        <div v-if="currentBackup">
            <h4>Metadata</h4>
            <div>
              <label><strong>Server hostname:</strong></label>
                <div class="input-group mb-3">
                  <input type="text" class="form-control" placeholder="hostname.com, 192.168.1.15, ..." aria-label="Username" aria-describedby="basic-addon1"
                    v-model="currentMetadata.ip_servidor" required>
                </div>

              <label><strong>NAS Hostname:</strong></label>
                <div class="input-group mb-3">
                  <input type="text" class="form-control" placeholder="nashostname.com, 192.168.1.14, ..." aria-label="Username" aria-describedby="basic-addon1"
                    v-model="currentMetadata.ip_nas">
                </div>
              <label><strong>NAS path:</strong></label>
                <div class="input-group mb-3">
                  <input type="text" class="form-control" placeholder="/path/of/your/backup/in/your/nas" aria-label="Username" aria-describedby="basic-addon1"
                    v-model="currentMetadata.ruta_respaldo">
                </div>
              
              <label><strong>Run As Sudo Header:</strong></label>
                <div v-if="currentMetadata.rash"></div>
                <div v-else>{{ currentMetadata.rash="echo <P4ssw0rd.> | sudo -S " }}</div>
                <div class="input-group mb-3">
                  <input type="text" class="form-control" placeholder="echo <password> | sudo -S " aria-label="Username" aria-describedby="basic-addon1"
                    v-model="currentMetadata.rash" required>
                </div>

              <label><strong>Server username:</strong></label>
                <div class="input-group mb-3">
                  <input type="text" class="form-control" placeholder="root, alice, bob, ..." aria-label="Username" aria-describedby="basic-addon1"
                    v-model="currentMetadata.user_servidor">
                </div>

              <label><strong>Server password:</strong></label>
                <div class="input-group mb-3">
                  <input type="password" class="form-control" placeholder="P4ssw0rd." aria-label="Username" aria-describedby="basic-addon1"
                    v-model="currentMetadata.pw_servidor">
                </div>

              <label><strong>Server SSH port:</strong></label>
                <div class="input-group mb-3">
                  <input type="number" class="form-control" placeholder="22" aria-label="Username" aria-describedby="basic-addon1" min="1"
                    v-model="currentMetadata.port" required>
                </div>

              <label><strong>Max retry attempts:</strong></label>
                <div class="input-group mb-3">
                  <input type="number" class="form-control" placeholder="2" aria-label="Username" aria-describedby="basic-addon1" min="1" max="5"
                    v-model="currentMetadata.reintentos_maximos" required>
                </div>
            </div>
            <div v-if="noMetadataExists">
              <div>
                <label><strong>Action:</strong></label><br>
                <button type="button" class="btn btn-success" @click="runBackup(currentIndex)">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-caret-right" viewBox="0 0 16 16">
                    <path d="M6 12.796V3.204L11.481 8zm.659.753 5.48-4.796a1 1 0 0 0 0-1.506L6.66 2.451C6.011 1.885 5 2.345 5 3.204v9.592a1 1 0 0 0 1.659.753"/>
                  </svg>
                </button>&nbsp;

                <router-link :to="'/backups/' + currentBackup.id">
                  <button type="button" class="btn btn-primary" @click="retreiveMetadata()">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-body-text" viewBox="0 0 16 16">
                      <path fill-rule="evenodd" d="M0 .5A.5.5 0 0 1 .5 0h4a.5.5 0 0 1 0 1h-4A.5.5 0 0 1 0 .5m0 2A.5.5 0 0 1 .5 2h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5m9 0a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5m-9 2A.5.5 0 0 1 .5 4h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5m5 0a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5m7 0a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5m-12 2A.5.5 0 0 1 .5 6h6a.5.5 0 0 1 0 1h-6a.5.5 0 0 1-.5-.5m8 0a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5m-8 2A.5.5 0 0 1 .5 8h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5m7 0a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5m-7 2a.5.5 0 0 1 .5-.5h8a.5.5 0 0 1 0 1h-8a.5.5 0 0 1-.5-.5m0 2a.5.5 0 0 1 .5-.5h4a.5.5 0 0 1 0 1h-4a.5.5 0 0 1-.5-.5m0 2a.5.5 0 0 1 .5-.5h2a.5.5 0 0 1 0 1h-2a.5.5 0 0 1-.5-.5"/>
                    </svg>
                  </button>
                </router-link>&nbsp;

                <button type="button" class="btn btn-warning" @click="updateMetadata()">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-floppy" viewBox="0 0 16 16">
                    <path d="M11 2H9v3h2z"/>
                    <path d="M1.5 0h11.586a1.5 1.5 0 0 1 1.06.44l1.415 1.414A1.5 1.5 0 0 1 16 2.914V14.5a1.5 1.5 0 0 1-1.5 1.5h-13A1.5 1.5 0 0 1 0 14.5v-13A1.5 1.5 0 0 1 1.5 0M1 1.5v13a.5.5 0 0 0 .5.5H2v-4.5A1.5 1.5 0 0 1 3.5 9h9a1.5 1.5 0 0 1 1.5 1.5V15h.5a.5.5 0 0 0 .5-.5V2.914a.5.5 0 0 0-.146-.353l-1.415-1.415A.5.5 0 0 0 13.086 1H13v4.5A1.5 1.5 0 0 1 11.5 7h-7A1.5 1.5 0 0 1 3 5.5V1H1.5a.5.5 0 0 0-.5.5m3 4a.5.5 0 0 0 .5.5h7a.5.5 0 0 0 .5-.5V1H4zM3 15h10v-4.5a.5.5 0 0 0-.5-.5h-9a.5.5 0 0 0-.5.5z"/>
                  </svg>
                </button>&nbsp;

                <button type="button" class="btn btn-danger" @click="deleteBackup()">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-dash-circle" viewBox="0 0 16 16">
                    <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
                    <path d="M4 8a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7A.5.5 0 0 1 4 8"/>
                  </svg>
                </button>
              </div>
          </div>
          <div v-else>
            <div>
                <label><strong>Action:</strong></label><br>
                <button type="submit" class="btn btn-info" @click="addMetadata()">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-floppy" viewBox="0 0 16 16">
                    <path d="M11 2H9v3h2z"/>
                    <path d="M1.5 0h11.586a1.5 1.5 0 0 1 1.06.44l1.415 1.414A1.5 1.5 0 0 1 16 2.914V14.5a1.5 1.5 0 0 1-1.5 1.5h-13A1.5 1.5 0 0 1 0 14.5v-13A1.5 1.5 0 0 1 1.5 0M1 1.5v13a.5.5 0 0 0 .5.5H2v-4.5A1.5 1.5 0 0 1 3.5 9h9a1.5 1.5 0 0 1 1.5 1.5V15h.5a.5.5 0 0 0 .5-.5V2.914a.5.5 0 0 0-.146-.353l-1.415-1.415A.5.5 0 0 0 13.086 1H13v4.5A1.5 1.5 0 0 1 11.5 7h-7A1.5 1.5 0 0 1 3 5.5V1H1.5a.5.5 0 0 0-.5.5m3 4a.5.5 0 0 0 .5.5h7a.5.5 0 0 0 .5-.5V1H4zM3 15h10v-4.5a.5.5 0 0 0-.5-.5h-9a.5.5 0 0 0-.5.5z"/>
                  </svg>
                </button>&nbsp;

                <button type="button" class="btn btn-danger" @click="deleteBackup()">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-dash-circle" viewBox="0 0 16 16">
                    <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
                    <path d="M4 8a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7A.5.5 0 0 1 4 8"/>
                  </svg>
                </button>
              </div>
          </div>
        </div>
    </div>
      <div v-if="currentBackup" class="col">
        <div v-if="backup_traces">
            <h4>Stats</h4>
            <div v-if="backup_traces">
              <h5>{{ currentBackup.name }}</h5><br>
              <table class="table">
                <thead>
                  <tr>
                    <th scope="col">Status</th>
                    <th scope="col">Time</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(backup_trace, index) in backup_traces"
                      :key="index">
                    <td>{{ backup_trace.last_status }}</td>
                    <td>{{ backup_trace.createdAt }}</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div v-if="chartArray">
              <div v-for="(item, index) in chartArray"
              :key="index">
                <Line
                  id="my-chart-id"
                  :options="item.chartOptions"
                  :data="item.chartData"
                />
              </div>
            </div>
        </div>
        <div v-else>
          <h3>Run this job to start...</h3>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import MetadataDataService from "../services/MetadataDataService";
  import BackupDataService from "../services/BackupDataService";
  import FileTracesDataService from "../services/FileTracesDataService";
  import BackupTracesDataService from "../services/BackupTracesDataService";
  import axios from "axios";
  import { Line } from 'vue-chartjs'
  import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement} from 'chart.js'
  ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement)

  
  export default {
    name: "backups-list",
    components: { Line },
    data() {
      return {
        chartArray: [],
        backup_traces: null,
        backups: [],
        status: [],
        currentBackup: null,
        currentIndex: -1,
        title: "",
        name: "",
        currentMetadata: {
              id_backup: null,
              ruta_respaldo: "",
              ip_servidor: "",
              ip_nas: "",
              rash: "",
              user_servidor: "",
              pw_servidor: "",
              port: null,
              reintentos_maximos: null
        },
        noMetadataExists: true,
        currentHistory: null
      };
    },
    methods: {
      async getBackupHistory(max){
        var data = {
          id_backup: this.currentBackup.id,
          max: max
        }

      this.backup_traces = await new Promise((resolve, reject) => {
          console.log(data);
          BackupTracesDataService.backupHistory(data)
          .then(response => {
             resolve(response.data);
          })
          .catch(e => {
            reject(e);
          });
        });

      },

      color_by_id(id){
        switch (id) {
          case 0:
            return "#007bff";
          case 1:
            return "#6610f2";
          case 2:
            return "#28a745";
          case 3:
            return "#dc3545";
          case 4:
            return "#ffc107";
          case 5:
            return "#fd7e14";
          case 6:
            return "#17a2b8";
          case 7:
            return "#e83e8c";
          case 8:
            return "#6f42c1";
          case 9:
            return "#20c997";
          default:
            return "#007bff";
        }
      },

      async retreiveHistoryFile(file){
        var data = {
          id_backup: this.currentBackup.id,
          file: file
        }
        
      return await new Promise((resolve, reject) => {
          console.log(data);
          FileTracesDataService.historyFile(data)
          .then(response => {
             resolve(response.data);
          })
          .catch(e => {
            reject(e);
          });
        });
      },

      async retreiveDiffFiles(){
        var data = {
          id_backup: this.currentBackup.id
        }
        await FileTracesDataService.diffFiles(data).then(async response => {
          let aux = await response.data;
          let listed_labels = [];
          let file_name = "";
          let file_sizes = [];
          let chartArrayItem = null;
          let auxArrayItem = [];
          let scale = 'KB'
          let max;
          for (let i in aux){
            file_name = aux[i].file;
            let local_history = await this.retreiveHistoryFile(file_name);
            file_sizes = [];
            listed_labels = [];
            scale = 'KB';
            for (let j in local_history){
              listed_labels.push(local_history[j].createdAt);
              file_sizes.push(local_history[j].size);
            }
            max = Math.max(...file_sizes)

            if(max>=1024**4){
              scale = "PB";
              file_sizes = file_sizes.map(x => x * (1/1024**4));
            }
            else if(max>=1024**3){
              scale = "TB";
              file_sizes = file_sizes.map(x => x * (1/1024**3));
            }
            else if(max>=1024**2){
              scale = "GB";
              file_sizes = file_sizes.map(x => x * (1/1024**2));
            }else if(max>=1024){
              scale = "MB";
              file_sizes = file_sizes.map(x => x * (1/1024));
            }

            console.log(max);
            console.log(i);
            let color = this.color_by_id(parseInt(i));

            chartArrayItem = {
              chartData: {
                labels: listed_labels,
                datasets: [
                  {label: file_name + " (" + scale + ")", data: file_sizes, tension: 0.3 , borderColor: color, backgroundColor: color, pointRadius: 3}
                ]
              },
              chartOptions: {
                responsive: true,
              }
            }
            auxArrayItem.push(chartArrayItem);
          }
          console.log(auxArrayItem);
          this.chartArray = auxArrayItem;
          
          })
          .catch(e => {
            console.log(e);
          });
      },

      retrievebackups() {
        console.log("Trayendo backups");
        BackupDataService.getAll()
          .then(response => {
            this.backups = response.data;

            console.log(response.data);
          })
          .catch(e => {
            console.log(e);
          });
      },

      async runBackup(index){
        this.status[index] = '[RUNNING]';
        
        let baseURL = `http://10.22.165.29:5000/?id=${this.currentBackup.id}`;
        axios.create({
            baseURL: baseURL,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'origin':'x-requested-with',
                'Access-Control-Allow-Headers': 'POST, GET, PUT, DELETE, OPTIONS, HEAD, Authorization, Origin, Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers, Access-Control-Allow-Origin',
                'Content-Type': 'application/json',
            }
          });
        await axios.get(baseURL).then((response) => {
          console.log(response.data);
          if(response.data === '[ALL OK]') this.status[index] = 'success';
          if(response.data === '[NOT OK]') this.status[index] = 'failure';
          if(response.data === '[FINISHED WITH ERRORS]') this.status[index] = 'warning';
          this.retreiveDiffFiles();
          this.getBackupHistory(5);
        });
      },
      
      retreiveMetadata(){
        MetadataDataService.getMetaBackup(this.currentBackup.id)
          .then(async response => {

            if (response.data !== '' && response.data.constructor === Object) {
              this.noMetadataExists = true;
              this.currentMetadata = response.data;
              await this.retreiveDiffFiles();
              await this.getBackupHistory(5);
            }else{
              this.currentMetadata = {
              id_backup: this.currentBackup.id,
              ruta_respaldo: "",
              ip_servidor: "",
              ip_nas: "",
              rash: "",
              user_servidor: "",
              pw_servidor: "",
              port: null,
              reintentos_maximos: null
              }
              this.noMetadataExists = false;
            }

          })
          .catch(e => {
            console.log(e);
          });
      },
  
      refreshList() {
        this.retrievebackups();
        this.currentBackup = null;
        this.currentIndex = -1;
      },
  
      setActiveTutorial(tutorial, index) {
        this.currentBackup = tutorial;
        this.currentIndex = tutorial ? index : -1;
      },

      displaySpinner(tutorial, index) {
        this.currentBackup = tutorial;
        this.currentIndex = tutorial ? index : -1;
      },
  
      removeAllbackups() {
        BackupDataService.deleteAll()
          .then(response => {
            console.log(response.data);
            this.refreshList();
          })
          .catch(e => {
            console.log(e);
          });
      },
      
      searchTitle() {
        BackupDataService.findByTitle(this.name)
          .then(response => {
            this.backups = response.data;
            this.setActiveTutorial(null);
            console.log(response.data);
          })
          .catch(e => {
            console.log(e);
          });
      },

      addBackup() {
        var data = {
          name: this.name
        };

        console.log(data);
  
        BackupDataService.create(data)
          .then(response => {
            this.backups.name = response.data.name;
            console.log(response.data);
            this.submitted = true;
            this.name = "";
            
            this.refreshList();
          })
          .catch(e => {
            console.log(e);
        });

      },

      deleteBackup() {
        BackupDataService.delete(this.currentBackup.id)
          .then(response => {
            console.log(response.data);
            this.$router.push({ name: "backups" });
            this.refreshList();
          })
          .catch(e => {
            console.log(e);
          });
      },

      addMetadata(){
        var data = this.currentMetadata;

        let auxCurrentBackup = this.currentBackup;
        let auxIndex = this.index;
          console.log(data);
    
        MetadataDataService.create(data)
          .then(response => {
            this.currentMetadata = response.data;
            console.log(response.data);
            this.submitted = true;

            this.retreiveMetadata();
            this.refreshList();
            this.setActiveTutorial(auxCurrentBackup, auxIndex);
          })
          .catch(e => {
            console.log(e);
        });
      },

      updateMetadata() {
        MetadataDataService.update(this.currentMetadata.id, this.currentMetadata)
          .then(response => {
            console.log(response.data);
            this.message = 'The metadata was updated successfully!';
          })
          .catch(e => {
            console.log(e);
          });
      }

    },
    mounted() {
      this.retrievebackups();
    }
  };
  
  </script>
  
  <style scoped>
  .legend-container {
    padding: 1em;
    display: flex;
    flex-wrap: wrap;
    width: 100%;
    gap: 14px;
    justify-content: center;
  }
  .badge {
    border-radius: 4.5px;
    padding: 0;
    width: 9px;
    height: 9px;
    display: inline-block;
    margin-right: 3px;
  }
  </style>
  