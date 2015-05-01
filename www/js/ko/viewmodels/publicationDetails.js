define(["jquery", "knockout"], function($, ko) {
	var vm = this;
	vm.publication = ko.observable(null);
	vm.pubId = ko.observable();
	vm.statusMsg = ko.observable('');

	vm.pubId.subscribe(function(newVal) {
		vm.publication(null);
		vm.statusMsg('Loading Publication.');
		$.getJSON('/api/publicationDetails.py?id=' + newVal, function(data) {
			vm.publication(data);
		}).done(function() {
			vm.statusMsg("Success!");
		}).fail(function() {
			vm.statusMsg("Error, Publication not found.");
		});
	});

	return vm;

});
