migrate((db) => {
  const collection = new Collection({
    "id": "lwcmr4xo3fiou91",
    "created": "2023-05-25 22:50:18.098Z",
    "updated": "2023-05-25 22:50:18.098Z",
    "name": "messages",
    "type": "base",
    "system": false,
    "schema": [
      {
        "system": false,
        "id": "1fvs8rt6",
        "name": "role",
        "type": "text",
        "required": true,
        "unique": false,
        "options": {
          "min": null,
          "max": null,
          "pattern": ""
        }
      },
      {
        "system": false,
        "id": "u5djzh15",
        "name": "body",
        "type": "text",
        "required": true,
        "unique": false,
        "options": {
          "min": null,
          "max": null,
          "pattern": ""
        }
      }
    ],
    "indexes": [],
    "listRule": null,
    "viewRule": null,
    "createRule": null,
    "updateRule": null,
    "deleteRule": null,
    "options": {}
  });

  return Dao(db).saveCollection(collection);
}, (db) => {
  const dao = new Dao(db);
  const collection = dao.findCollectionByNameOrId("lwcmr4xo3fiou91");

  return dao.deleteCollection(collection);
})
