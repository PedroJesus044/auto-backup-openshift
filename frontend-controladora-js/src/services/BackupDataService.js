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
}

export default new TutorialDataService();
