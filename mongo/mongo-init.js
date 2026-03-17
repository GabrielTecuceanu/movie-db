db = db.getSiblingDB("data");

db.createUser({
  user: "root",
  pwd: "root",
  roles: [
    { role: "readWrite", db: "data" }
  ]
});
