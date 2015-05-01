define(["jquery", "knockout"], function($, ko) {
	var vm = this;
	vm.message = ko.observable("Test Message");
	vm.getDocs = function() {
		console.log("clicked!");
		vm.message("Loading!");
		$.getJSON('/api/documents.py', function(data) {
			vm.message(data);
		});
	}
	return vm;
});