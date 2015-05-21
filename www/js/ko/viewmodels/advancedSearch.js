/**
*	Advanced search View Model.
* This view model loads with advancedSearch.html to facilitate
* the advanced search functionality.
*
* @requires jQuery
* @requires knockout.js
*
* @author Deshin
* @author Anthony
*/
define(["jquery", "knockout"], function($, ko) {
	var vm = this;
	//title, author, bookTitle, conferenceTitle, journalTitle, abstract
	vm.fields = ko.observableArray(['']);
	/**
	*	Get the advanced search fields from the advancedSearchFields python
	* endpoint
	* @requires jQuery
	*/
	$.getJSON("/api/advancedSearchFields.py", function(data) {
		vm.fields(data);
		vm.defaultSearch = function() {
			return 	{
				field: ko.observable(vm.fields()[0]),
				value: ko.observable(""),
				operator: ko.observable(vm.operators()[0])
			};
		};
		vm.addSearch();
	});
	vm.operators = ko.observableArray(['equals', 'contains']);
	/**
	* @method
	* Create default search parameters, field, value and operator
	* are all empty strings.
	*/
	vm.defaultSearch = function() {
		return 	{
			field: ko.observable(""),
			value: ko.observable(""),
			operator: ko.observable("")
		};
	};
	vm.searches = ko.observableArray([]);
	/**
	* @method addSearch
	* Add a new search window to the interface, displays
	* new input windows for parameter, field and value.
	*/
	vm.addSearch = function() {
		vm.searches.unshift(vm.defaultSearch());
	};
	/**
	* @method removeSearch
	* Remove a search window from the interface, will display
	* one less input window set.
	*/
	vm.removeSearch = function(index) {
		vm.searches.splice(index(), 1);
	};
	/**
	* @method searchHref
	* Search build the search string for sending to the publications
	* page, this will then be parsed as an advanced search by the
	* python endpoint. 
	*/
	vm.searchHref = ko.computed(function() {
		var srchs = [];
		for (var i = 0; i < vm.searches().length; i++) {
			if (vm.searches()[i].value()) {
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
