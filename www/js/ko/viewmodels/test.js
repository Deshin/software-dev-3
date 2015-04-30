define(["knockout"], function(ko) {
	var vm = {};
	vm.message = ko.observable("Test Message");
	return vm;
});