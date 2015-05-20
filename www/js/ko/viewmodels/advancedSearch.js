define(["jquery", "knockout"], function($, ko) {
	var vm = this;
	//title, author, bookTitle, conferenceTitle, journalTitle, abstract
	vm.fields = ko.observableArray(['title', 'author', 'bookTitle', 'conferenceTitle', 'journalTitle', 'abstract']);
	vm.operators = ko.observableArray(['equals', 'contains']);
	vm.defaultSearch = function() {
		return 	{
			field: "title",
			value: "",
			operator: "equals"
		};
	};
	vm.searches = ko.observableArray([vm.defaultSearch()]);
	vm.addSearch = function() {
		vm.searches.unshift(vm.defaultSearch());
	};
	vm.removeSearch = function(index) {
		console.log(index());
		vm.searches.splice(index(), 1);
	};
	vm.searchHref = ko.computed(function() {
		var srchs = [];
		for (var i = 0; i < vm.searches().length; i++) {
			if (!(vm.searches()[i].value)) {
				srchs.push(vm.searches()[i]);
			};
		};
		return '/#!/publications?search='+JSON.stringify(srchs);
	})
	return vm;
});