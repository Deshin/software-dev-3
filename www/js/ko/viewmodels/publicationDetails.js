define(["jquery", "knockout"], function($, ko) {
	var vm = this;
	vm.publication = ko.observable({});
	vm.pubId = ko.observable({});

	vm.pubId.subscribe(function(newVal) {
		$.getJSON('/api/publicationDetails.py?id=' + newVal, function(data) {
			vm.publication(data);
		});
	});

	return vm;

});
