<template>
    <div v-if="currentTutorial" class="edit-form">
      <h4>Code lines</h4>
    </div>
  
    <div v-else>
      <br />
      <p>Please click on a Tutorial...</p>
    </div>

    <div v-if="blockList" class="edit-form">
      
      <ul class="list-group">
          <form id="cuadro">
            <li class="list-group-item"
              v-for="(bloque, index) in blockList"
              :key="index">
              <strong>Block: {{ bloque.distinct_bloques }}</strong>
              &nbsp;
              <input v-if="bloque.codigo" v-model="bloque.codigo[0].paralelo" type="checkbox" @change="setParalelBlock(bloque)">

              <ul>
                <li class="list-group-item"
                v-for="(codigo, index2) in bloque.codigo"
                :key="index2">
                  <div class="row">
                    <input @change="updateLinea(codigo)" type="checkbox" v-model="codigo.run_as_sudo">
                    &nbsp;

                    <input @change="updateLinea(codigo)" class="contform-rol col" type="text" v-model="codigo.linea">
                    &nbsp;
                    <a><button type="button" class="btn btn-danger col" @click="deleteLine(codigo.id)">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-dash-circle" viewBox="0 0 16 16">
                        <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
                        <path d="M4 8a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7A.5.5 0 0 1 4 8"/>
                      </svg>
                    </button></a>
                    <input type="hidden" v-model="codigo.id">
                  </div>
                </li>
                <li class="list-group-item">
                  <div class="input-group">
                    <input @keypress.enter="newLine(this.id_backup, bloque.distinct_bloques, index)" v-model="new_line_array[index]" type="text" class="form-control" placeholder="+ Añadir" aria-label="Username" aria-describedby="basic-addon1">
                  </div>
                </li>

              </ul>
            </li>
          </form>
      </ul>
    </div>
    <div class="pb-5">
      <p><strong>Añadir bloque:</strong></p>
      <input id="add-bloque" @keypress.enter="newBlockAndLine(this.id_backup)" v-model="new_line_block" type="text" class="form-control" placeholder="+ Añadir" aria-label="Username" aria-describedby="basic-addon1">
    </div>

  </template>
  
  <script>
  import TutorialDataService from "../services/BackupDataService";
  import CodigosDataService from "../services/CodigoDataService";
  
  export default {
    name: "backup-view",
    data() {
      return {
        id_backup: null,
        no_bloque: null,
        currentTutorial: null,
        blockList: null,
        message: '',
        auxBackupId: null,
        auxNoBloque: null,
        currentBlock: [],
        new_line_array: [],
        new_line_block: null,
        x: 0,
        y: 0
      };
    },

    methods: {
      scrollToItem(id){
        const targetItem = document.getElementById(id);
        targetItem.scrollIntoView();
      },

      setActive(id){
        console.log('Holi :)', id);
      },

      updateLinea(linea){
        CodigosDataService.update(linea.id, linea).then(response => {
            console.log(response.data);
          })
          .catch(e => {
            console.log(e);
        });
      },

      setParalelBlock(bloque){
        var data = {
          id_backup: bloque.codigo[0].id_backup,
          no_bloque: bloque.codigo[0].no_bloque,
          paralelo: bloque.codigo[0].paralelo
        }

        CodigosDataService.updateParallelism(data).then(response => {
            console.log(response.data);
          })
          .catch(e => {
            console.log(e);
        });
      },

      async newLine(id_backup, no_bloque, index){
        console.log(id_backup, no_bloque, this.new_line_array[index]);

        var data = {
            id_backup: id_backup,
            no_linea: null,
            linea: this.new_line_array[index],
            run_as_sudo: 0,
            paralelo: 0,
            no_bloque: no_bloque
        };
  
        await CodigosDataService.addLinea(data)
          .then(response => {
            console.log(response.data);
            this.new_line_array[index] = ""
            this.retreiveBlocks(this.$route.params.id);
          })
          .catch(e => {
            console.log(e);
        });

        
      },

      newBlockAndLine(id_backup){
        console.log(id_backup, this.new_line_block);
        
        var argumento = {
            id_backup: id_backup,
            linea: this.new_line_block
        };

        CodigosDataService.addBloque(argumento)
            .then(response => {
              console.log("Response del codigosdataservice.addBlk");
              console.log(response.data);
              this.new_line_block = "";
              this.scrollToItem('bottom');
              this.retreiveBlocks(this.$route.params.id);
            })
            .catch(e => {
              console.log(e);
          });
      },

      savePos(){
        this.x = window.scrollX;
        this.y = window.scrollY;
      },

      gotoPos(){
        console.log(this.x, this.y);
        window.scrollTo(this.x, this.y);
      },

      async deleteLine(id){
        //let el = document.getElementById('cuadro').lastElementChild;
        console.log('Borranding: ', id);
        await CodigosDataService.delete(id)
          .then(response => {
            console.log(response.data);
          })
          .catch(e => {
            console.log(e);
          });
        this.retreiveBlocks(this.id_backup);
        //el.scrollIntoView({behavior: 'smooth'});
      },

      async retreiveLinesOfBlock(id_backup, no_bloque){
        return await new Promise((resolve, reject) => {
          CodigosDataService.findLinesOfBlock(id_backup, no_bloque)
          .then(response => {
             resolve(response.data);
          })
          .catch(e => {
            reject(e);
            
          });
        })
      },

      async retreiveBlocks(id_backup){
        await CodigosDataService.findDifferentBackupBlocks(id_backup)
          .then(async response => {
            this.blockList = response.data;
            for (let i in this.blockList){
              let aux = await this.retreiveLinesOfBlock(this.id_backup, this.blockList[i].distinct_bloques);
              this.blockList[i].codigo = aux;
            }
            console.log(this.blockList);
          })
          .catch(e => {
            console.log(e);
          });
      },

      getTutorial(id) {
        TutorialDataService.get(id)
          .then(response => {
            this.currentTutorial = response.data;
            console.log(response.data);
          })
          .catch(e => {
            console.log(e);
          });
      },
  
      updatePublished(status) {
        var data = {
          id: this.currentTutorial.id,
          title: this.currentTutorial.title,
          description: this.currentTutorial.description,
          published: status
        };
  
        TutorialDataService.update(this.currentTutorial.id, data)
          .then(response => {
            console.log(response.data);
            this.currentTutorial.published = status;
            this.message = 'The status was updated successfully!';
          })
          .catch(e => {
            console.log(e);
          });
      },
  
      updateTutorial() {
        TutorialDataService.update(this.currentTutorial.id, this.currentTutorial)
          .then(response => {
            console.log(response.data);
            this.message = 'The tutorial was updated successfully!';
          })
          .catch(e => {
            console.log(e);
          });
      },
  
      deleteTutorial() {
        TutorialDataService.delete(this.currentTutorial.id)
          .then(response => {
            console.log(response.data);
            this.$router.push({ name: "tutorials" });
          })
          .catch(e => {
            console.log(e);
          });
      }
    },
    async mounted() {
      this.message = '';
      this.id_backup = this.$route.params.id;
      await this.retreiveBlocks(this.$route.params.id);
      this.getTutorial(this.$route.params.id);
    }
  };
  </script>
  
  <style>
  .edit-form {
    max-width: 100%;
    margin: auto;
  }
  </style>
  