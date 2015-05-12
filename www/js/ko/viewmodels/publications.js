define(["jquery", "knockout"], function($, ko) {
	var vm = this;
	vm.publications = ko.observableArray([]);
	$.getJSON('/api/publications.py', function(data) {
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
	});
	return vm;
});
