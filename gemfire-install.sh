curl --user admin:admin -H 'X-Requested-By:Pivotal' -X POST http://c6401.ambari.apache.org:8080/api/v1/blueprints/blueprint-gemfire-3-node -d @blueprint-gemfire-3-node.json

curl --user admin:admin -H 'X-Requested-By:Pivotal' -X POST http://c6401.ambari.apache.org:8080/api/v1/clusters/gemfire_ambari -d @hostmapping-gemfire-3-node.json