define(["jquery", "knockout"], function($, ko) {
	var vm = this;
	vm.publication = ko.observable(null);
	vm.pubId = ko.observable();
	vm.statusMsg = ko.observable('');

	vm.pubId.subscribe(function(newVal) {
		vm.publication(null);
		vm.statusMsg('Loading Publication.');
		$.getJSON('/api/publicationDetails.py?id=' + newVal, function(data) {
			// Fetch the publication information
		}).done(function(data) {
			var authors = "";
			for (var j = 0; j < data.Authors.length; j++) {
				authors += data.Authors[j][4] + " " + data.Authors[j][3];
				if(j != data.Authors.length - 1) {
					authors += ", ";
				}
			}
			data.Authors = authors;
			vm.publication(data);
			vm.statusMsg("Success!");
		}).fail(function(err) {
			vm.statusMsg("Error, Publication not found.");
		});
	});

	return vm;

	function parseAuthor(authors) {
		for(var i = 0; i < Authors.length; i++) {

		}
	}

});
