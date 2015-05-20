define(["jquery", "knockout"], function($, ko) {
	var vm = this;
	//title, author, bookTitle, conferenceTitle, journalTitle, abstract
	vm.fields = ko.observableArray(['title', 'author', 'bookTitle', 'conferenceTitle', 'journalTitle', 'abstract']);
	$.getJSON("/api/advancedSearchFields.py", function(data) {
		vm.fields(data);
	});
	vm.operators = ko.observableArray(['equals', 'contains']);
	vm.defaultSearch = function() {
		return 	{
			field: ko.observable("title"),
			value: ko.observable(""),
			operator: ko.observable("equals")
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
			if (vm.searches()[i].value) {
				var newVal = {
					field: vm.searches()[i].field(),
					value: vm.searches()[i].value(),
					operator: vm.searches()[i].operator()
				}
				srchs.push(newVal);
			};
		};
		return '/#!/publications?search='+JSON.stringify(srchs);
	})
	return vm;
});