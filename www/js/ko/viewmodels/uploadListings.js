define(["jquery", "knockout"], function($, ko) {
	var vm = this;
	vm.formats = ko.observableArray(['']);
	$.getJSON("/api/CSVFormats.py", function(data) {
		vm.formats(data);
		vm.defaultListing = function() {
			return 	{
				format: ko.observable(vm.formats()[0]),
				type: ko.observable("Accredited"),
				data: ko.observable(""),
				name: ko.observable("Choose File...")
			};
		};
	});
	vm.types = ko.observableArray(['Accredited', 'Predatory', 'H-Index']);
	vm.defaultListing = function() {
		return 	{
			format: ko.observable(vm.formats()[0]),
			type: ko.observable("Accredited"),
			data: ko.observable(""),
			name: ko.observable("Choose File...")
		};
	};
	vm.listings = ko.observableArray([vm.defaultListing()]);
	vm.addListing = function() {
		vm.listings.unshift(vm.defaultListing());
	};
	vm.removeListing = function(index) {
		vm.listings.splice(index(), 1);
	};
	return vm;
});