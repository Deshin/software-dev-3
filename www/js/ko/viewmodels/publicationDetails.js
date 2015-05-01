define(["jquery", "knockout"], function($, ko) {
	var vm = this;
	vm.message = ko.observable("Test Message");
	vm.publicationID = ko.observable(0);
	vm.getDocs = function() {
		console.log("clicked!");
		vm.message("Loading!");
		$.getJSON('/api/publicationDetails.py?id=' + vm.publicationID(), function(data) {
			vm.message(data);
		});
	};
	return vm;
});
