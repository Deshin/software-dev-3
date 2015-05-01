define(["jquery", "knockout"], function($, ko) {
	var vm = this;
	vm.message = ko.observable("Test Message");
	vm.publicationID = ko.observable(null);
	vm.getDocs = getDocs;

	return vm;

	function getDocs() {
		console.log("clicked!");
		vm.message("Loading!");
		$.getJSON('/api/publicationDetails.py?id=' + vm.publicationID(), function(data) {
			vm.message(data);
		});
	}

});
