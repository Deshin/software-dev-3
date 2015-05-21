define(["jquery", "knockout"], function($, ko) {
	var vm = this;
	vm.publication = ko.observable(null);
	vm.permission = ko.observable(rootViewModel.loginState());

	vm.permission.subscribe(function() {
		getData();
	});

	vm.pubId = ko.observable();
	vm.statusMsg = ko.observable('');
	vm.pdfUrl = ko.observable('');
	vm.tocUrl = ko.observable('');
	vm.suppDocs = ko.observableArray([]);
	vm.pubId.subscribe(function(newVal) {
		getData();
	});
	vm.accredit = function() {
		$.get('/api/accreditPublication.py', {publicationID: vm.pubId().toString()})
		.done(function(data){
			getData();
		});
	};

	return vm;

	function getData() {
		vm.publication(null);
		vm.statusMsg('Loading Publication.');
		$.getJSON('/api/publicationDetails.py?id=' + vm.pubId())
		.done(function(data) {
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
			vm.suppDocs.removeAll();
			for (var i = 0; i < vm.publication().PeerReviewDocumentation.length; i++) {
				var fileDetail = {
					name: vm.publication().PeerReviewDocumentation[i].DocumentTitle,
					path: "files/" + vm.publication().PeerReviewDocumentation[i].PathToFile
				};
				vm.suppDocs.push(fileDetail);
			}
			vm.statusMsg("Success!");
		}).fail(function(jqxhr) {
			vm.statusMsg("Error " + jqxhr.status + " - " + jqxhr.statusText);
		});
	}

});
