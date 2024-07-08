import http from "../http-common";

class MetadataDataService {
  getAll() {
    return http.get("/metadatas");
  }

  get(id) {
    return http.get(`/metadatas/${id}`);
  }

  create(data) {
    return http.post("/metadatas", data);
  }

  update(id, data) {
    return http.put(`/metadatas/${id}`, data);
  }

  delete(id) {
    return http.delete(`/metadatas/${id}`);
  }

  deleteAll() {
    return http.delete(`/metadatas`);
  }

  getMetaBackup(data){
    return http.get(`/metadatas/metabackup`,  { params: { id_backup: data } });
  }
}

export default new MetadataDataService();
