define(["jquery", "knockout"], function($, ko) {
	var vm = this;
	vm.search = ko.observable(null);
	vm.search.subscribe(function(newVal) {
		if (newVal != "") {
			rootViewModel.search(newVal);
			$.getJSON('/api/publications.py?simpleSearch='+vm.search, vm.gotData);
		} else {
			$.getJSON('/api/publications.py', vm.gotData);
		};
	}, vm, 'change');
	vm.publications = ko.observableArray([]);
	vm.gotData = function(data) {
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
	}
	return vm;
});
