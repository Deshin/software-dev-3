define(["jquery", "knockout"], function($, ko) {
	var vm = this;
	vm.publication = ko.observable(null);
	vm.pubId = ko.observable();
	vm.statusMsg = ko.observable('');
	vm.pdfUrl = ko.observable('');

	vm.pubId.subscribe(function(newVal) {
		vm.publication(null);
		vm.statusMsg('Loading Publication.');
		$.getJSON('/api/publicationDetails.py?id=' + newVal)
		.done(function(data) {
			var authors = "";
			for (var j = 0; j < data.Authors.length; j++) {
				authors += data.Authors[j].Initials + " " + data.Authors[j].Surname;
				if(j != data.Authors.length - 1) {
					authors += ", ";
				}
			}
			data.Authors = authors;
			vm.publication(data);
			console.log(data);
			vm.pdfUrl("files/" + vm.publication().ScanPath.replace(/\\/g, "/"));
			vm.statusMsg("Success!");
		}).fail(function(jqxhr) {
			vm.statusMsg("Error " + jqxhr.status + " - " + jqxhr.statusText);
		});
	});

	return vm;

});
