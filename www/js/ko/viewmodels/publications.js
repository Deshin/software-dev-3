define(["jquery", "knockout"], function($, ko) {
	var vm = this;
	vm.pageSize = ko.observable(null);
	vm.page = ko.observable(null);
	vm.skip = ko.computed(function() {
		return (vm.page()-1)*vm.pageSize();
	});
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
	vm.search = ko.observable(null);
	vm.updateList = function(newVal) {
		if (vm.page() === null || vm.pageSize() === null || vm.search() === null) {
			return;
		}
		var getUrl = '/api/publications.py?skip='+vm.skip().toString()+'&length='+vm.pageSize().toString();
		if (vm.search() !== ""){
			rootViewModel.search(vm.search());
			getUrl += '&simpleSearch='+vm.search();
		} else {
			rootViewModel.search("");
		}
		$.getJSON(getUrl, vm.gotData);
	};
	vm.search.subscribe(updateList, vm, 'change');
	vm.page.subscribe(updateList, vm, 'change');
	vm.pageSize.subscribe(updateList, vm, 'change');
	vm.publications = ko.observableArray([]);
	vm.next = function() {
		vm.page(vm.page()+1);
	};
	vm.previous = function() {
		vm.page(vm.page()-1);
	};
	vm.first = function() {
		vm.page(1);
	};
	return vm;
});
