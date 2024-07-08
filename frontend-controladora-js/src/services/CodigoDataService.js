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
    return http.put(`/codigos/${id}`, data);
  }

  delete(id) {
    return http.delete(`/codigos/${id}`);
  }

  deleteAll() {
    return http.delete(`/tutorials`);
  }

  findByTitle(title) {
    return http.get(`/tutorials?title=${title}`);
  }

  findDifferentBackupBlocks(id){
    return http.get(`/codigos/diffblocksbkpid?id_backup=${id}`);
  }

  findLinesOfBlock(id_backup, no_bloque){
    return http.get(`/codigos/codebackupblock?id_backup=${id_backup}&no_bloque=${no_bloque}`);
  }

  addLinea(data){
    return http.post("/codigos/addlinetospecificblock", data);
  }

  addBloque(data){
    console.log(data);
    return http.post(`/codigos/addlinetospecificbackup`, data);
  }

  updateParallelism(data){
    console.log(data);
    return http.put(`/codigos/updateparallelism`, data);
  }

}

export default new TutorialDataService();
