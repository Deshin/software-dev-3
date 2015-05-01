define(["jquery", "knockout"], function($, ko) {
	var vm = this;
	vm.publication = ko.observable({});
	vm.getDocs = getDocs;

	getDocs(1);

	return vm;

	function getDocs(ID) {
		vm.publication("Loading!");

		$.getJSON('/api/publicationDetails.py?id=' + ID, function(data) {
			vm.publication(data);
			console.log(data);
		});

	}

});
