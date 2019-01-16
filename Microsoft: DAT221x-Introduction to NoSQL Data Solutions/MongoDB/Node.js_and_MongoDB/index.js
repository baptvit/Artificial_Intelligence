var MongoClient = require('mongodb').MongoClient;
		
		var url = 'mongodb://nosqledx.eastus2.cloudapp.azure.com:27017/local';
		MongoClient.connect(url, function (error, database) {
		    console.log("Successfully connected to: " + url);
				
		    var cursor = database.collection('school').find(query);
		    cursor.each(function (err, doc) {
		        console.dir(doc);
		    });
		
		    database.close();
		});