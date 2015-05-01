define(["jquery", "knockout"], function($, ko) {
	var vm = this;
	vm.publications = ko.observableArray([{
		PublicationId: "",
		Title: "",
		Category: "",
		Year: "",
		Publisher: "",
		Authors: ""
	}]);
	$.getJSON('/api/documents.py', function(data) {
		console.log(data);
		for (var i = data.length - 1; i >= 0; i--) {
			var authors = "";
			for (var j = 0; j < data[i].Authors.length; j++) {
				authors += data[i].Authors[j].Initials + " " + data[i].Authors[j].Surname + ", ";
			};
			data[i].Authors = authors;
			vm.publications.push(data[i]);
		};
	});
	return vm;
});