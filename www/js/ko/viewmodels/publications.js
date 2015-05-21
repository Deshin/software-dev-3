/**
* Load this view model with the publications partial
* it will load a list of publications from the restful endpoint
* and will display them to the user.
*
* @requires jQuery
* @requires knockout.js
*
* @author Deshin
* @author Anthony
*/
define(["jquery", "knockout"], function($, ko) {
	var vm = this;
	vm.search = ko.observable(null);
	vm.pageSize = ko.observable(null);
	vm.page = ko.observable(null);
	vm.sortBy=ko.observable(null);
	vm.sort=ko.observable(null);
	/**
	* @method skip
	* determine the skip value for pagination.
	*/
	vm.skip = ko.computed(function() {
		return (vm.page()-1)*vm.pageSize();
	});
	/**
	* @method sortIcon
	* determine the sort of icon that is shown depending on how
	* the publications are sorted.
	*/
	vm.sortIcon = ko.computed(function() {
		if (vm.sort() === "ASC") {
			return "glyphicon glyphicon-triangle-top";
		} else{
			return "glyphicon glyphicon-triangle-bottom";
		};
	});
	/**
	* @callback gotData
	* This callback is used to parse the data received from the
	* server, and puts it into a form for display to the user.
	*/
	vm.gotData = function(data) {
		vm.publications.removeAll();
		for (var i = 0; i < data.length; i++) {
			var authors = "";
			for (var j = 0; j < data[i].Authors.length; j++) {
				authors += data[i].Authors[j].Initials + " " + data[i].Authors[j].Surname;
				if(j != data[i].Authors.length - 1) {
					authors += ", ";
				}
			}
			data[i].Authors = authors;
			data[i].link = "#!/publicationDetails?pubId="+data[i].PublicationId.toString();
			vm.publications.push(data[i]);
		}
	};
	/**
	* @callback updateList()
	* Update the list if any of the query strings are passed into the page
	* or if entered on the DOM, will trigger listen events that trigure this callback.
	*/
	vm.updateList = function(newVal) {
		if (vm.page() === null || vm.pageSize() === null || vm.search() === null || vm.sort() === null || vm.sortBy() === null) {
			return;
		}
		var getUrl = '/api/publications.py?skip='+vm.skip().toString()+'&length='+vm.pageSize().toString()+'&sortBy='+vm.sortBy()+'&sort='+vm.sort();
		if (vm.search() !== ""){
			if (vm.search().charAt(0) === "[") {
				rootViewModel.search("");
				getUrl += '&advancedSearch='+vm.search();
			} else {
				rootViewModel.search(vm.search());
				getUrl += '&simpleSearch='+vm.search();
			};
		} else {
			rootViewModel.search("");
		}
		$.getJSON(getUrl, vm.gotData);
	};
	vm.search.subscribe(updateList, vm, 'change');
	vm.page.subscribe(updateList, vm, 'change');
	vm.pageSize.subscribe(updateList, vm, 'change');
	vm.sortBy.subscribe(updateList, vm, 'change');
	vm.sort.subscribe(updateList, vm, 'change');
	vm.publications = ko.observableArray([]);
	/**
	* @method next
	* Get the next page for pagination.
	*/
	vm.next = function() {
		vm.page(vm.page()+1);
	};
	/**
	* @method previous
	* Get the previous page for pagination.
	*/
	vm.previous = function() {
		vm.page(vm.page()-1);
	};
	/**
	* @method first
	* Get the first page for pagination.
	*/
	vm.first = function() {
		vm.page(1);
	};
	/**
	* @method sorting
	* Set the order of a particular column displayed on the DOM,
	* will call the method and request new set of publications.
	*/
	vm.sorting = function(item){
		if (vm.sortBy() === item) {
			if (vm.sort() === "ASC") {
				vm.sort("DESC");
			} else{
				vm.sort("ASC");
			}
		} else{
			vm.sortBy(item);
			vm.sort("ASC");
		}
	};
	return vm;
});
