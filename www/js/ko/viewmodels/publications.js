define(["jquery", "knockout"], function($, ko) {
	var vm = this;
	vm.search = ko.observable(null);
	vm.pageSize = ko.observable(null);
	vm.page = ko.observable(null);
	vm.sortBy=ko.observable(null);
	vm.sort=ko.observable(null);
	vm.skip = ko.computed(function() {
		return (vm.page()-1)*vm.pageSize();
	});
	vm.sortIcon = ko.computed(function() {
		if (vm.sort() === "ASC") {
			return "glyphicon glyphicon-hand-up";
		} else{
			return "glyphicon glyphicon-hand-down";
		};
	});
	vm.gotData = function(data) {
		console.log("Got: ",data);
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
	vm.next = function() {
		vm.page(vm.page()+1);
	};
	vm.previous = function() {
		vm.page(vm.page()-1);
	};
	vm.first = function() {
		vm.page(1);	
	};
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
