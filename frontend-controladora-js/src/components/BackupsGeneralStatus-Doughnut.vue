<template>
    <div class="d-flex justify-content-around flex-wrap">
        <div style="width: 100px; height: 100px;"
        v-for="(item, index) in doughnut_data"
        :key="index"
        class="p-1">
            <Doughnut :data="item.data" :options="item.options" />
        </div>
        
    </div>
</template>
<script>
import BackupTracesDataService from "../services/BackupTracesDataService";

import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import { Doughnut } from 'vue-chartjs'
ChartJS.register(ArcElement, Tooltip, Legend)

export default {
    name: "general-status",
    components: {
        Doughnut
    },
    data() {
        return {
            backup_states: [],
            doughnut_data: []
        };
      },
      methods: {
        getStatus(){
            BackupTracesDataService.generalStatus()
            .then(response => {
                this.backup_states = response.data.reverse();
            })
            .catch(e => {
                console.log(e);
            });
        },
        update_doughnuts(item){
            let color, value;
            switch(item.last_status) {
                case "[ALL OK]":
                    color = "#70bd4a";
                    value = 100;
                    break;
                case "[RUNNING]":
                    color = "#435ee6";
                    value = 200;
                    break;
                case "[NOT OK]":
                    color = "#e64343";
                    value = 50;
                    break;
                case "[FINISHED WITH ERRORS]":
                    color = "#ffca38";
                    value = 25;
                    break;
                default:
                    color = "currentColor";
                    value = 0;
            }
            return {
                    data: {
                        labels: [item.name],
                        datasets: [
                            {
                                backgroundColor: [color],
                                data: [value]
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        elements: {
                            arc: {
                                borderWidth: 0
                            }
                        },
                        plugins: {
                            legend: {
                                display: true,
                                labels: {
                                    color: 'black',
                                    textAlign: 'center',
                                    padding: 0,
                                    boxWidth: 0,
                                    boxHeight: 0,
                                    boxPadding: 0
                                }
                            }
                        }
                    }
                }
        }
      },
      mounted() {
        this.getStatus();
        this.timer = setInterval(() => {
            this.getStatus();
            this.doughnut_data = this.backup_states.map(this.update_doughnuts);
        }, 300)
      }
}
</script>
<style>
    
</style>