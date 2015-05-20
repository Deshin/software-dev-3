define(["jquery", "knockout"], function($, ko) {
	var vm = this;
	vm.publication = ko.observable(null);
	vm.pubId = ko.observable();
	vm.statusMsg = ko.observable('');
	vm.pdfUrl = ko.observable('');
	vm.tocUrl = ko.observable('');
	vm.suppDocs = ko.observableArray([]);
	vm.pubId.subscribe(function(newVal) {
		vm.publication(null);
		vm.statusMsg('Loading Publication.');
		$.getJSON('/api/publicationDetails.py?id=' + newVal)
		.done(function(data) {
			console.log(data);
			var authors = "";
			for (var j = 0; j < data.Authors.length; j++) {
				authors += data.Authors[j].Initials + " " + data.Authors[j].Surname;
				if(j !== data.Authors.length - 1) {
					authors += ", ";
				}
			}
			data.Authors = authors;
			vm.publication(data);
			vm.pdfUrl("files/" + vm.publication().ScanPath);
			vm.tocUrl("files/" + vm.publication().TableOfContentsPath);
			for (var i = 0; i < vm.publication().PeerReviewDocumentation.length; i++) {
				var fileDetail = {
					name: vm.publication().PeerReviewDocumentation[i].DocumentTitle,
					path: vm.publication().PeerReviewDocumentation[i].PathToFile
				}
				vm.suppDocs.push(fileDetail);
			};
			vm.statusMsg("Success!");
		}).fail(function(jqxhr) {
			vm.statusMsg("Error " + jqxhr.status + " - " + jqxhr.statusText);
		});
	});

	return vm;

});
