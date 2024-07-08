import http from "../http-common";

class TutorialDataService {
  getAll() {
    return http.get("/backups");
  }

  get(id) {
    return http.get(`/backups/${id}`);
  }

  create(data) {
    return http.post("/backups", data);
  }

  update(id, data) {
    return http.put(`/backups/${id}`, data);
  }

  delete(id) {
    return http.delete(`/backups/${id}`);
  }

  deleteAll() {
    return http.delete(`/tutorials`);
  }

  backupHistory(data){
    return http.post("/backup_traces/retrieve_limit", data);
  }

  historyFile(data){
    return http.get("/file_traces/historyfile", data);
  }

  generalStatus(){
    return http.get("/backup_traces/last_status");
  }
}

export default new TutorialDataService();
