define(["jquery", "knockout"], function($, ko) {
	var vm = this;

	vm.submitPublication = submitPublication;
	var publication = {};
	vm.categoryList = ko.observableArray(['Journal Article', 'Conference Paper', 'Book Chapter']);
	var formVM = {};

	$('#uploadPublication').validate({
		rules: publicationRules(),
		messages: publicationMessages()
	});

	init();

	return vm;

	function submitPublication(form) {
		console.log($('#uploadPublication').valid());
		vmToJson();
		console.log(publication);
	}

	function init() {
		formVM.Title = ko.observable("");
		formVM.Abstract = ko.observable("");
		formVM.Authors = ko.observable("");
		formVM.Category = ko.observable("");
		formVM.ConferenceTitle = ko.observable("");
		formVM.Country = ko.observable("");
		formVM.DocumentTitle = ko.observable("");
		formVM.MotivationForAccreditation = ko.observable("");
		formVM.PeerReviewProcess = ko.observable("");
		formVM.Publisher = ko.observable("");
		formVM.Year = ko.observable("");
		vm.formVM = formVM;
	}

	function publicationRules() {
		return {
			publicationTitle: "required"
		};
	}

	function publicationMessages() {
		return {
			publicationTitle: "Please enter a valid title."
		};
	}

	function vmToJson() {
		for (var id in formVM) {
			if(formVM[id]()) {
				publication[id] = formVM[id]();
			} else {
				delete publication[id];
			}
		}
	}

});
