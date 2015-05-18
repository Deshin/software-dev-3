define(["jquery", "knockout"], function($, ko) {
	var vm = this;

	vm.submitPublication = submitPublication;
	var publication = {};
	vm.categoryList = ko.observableArray(['Journal Article', 'Conference Paper', 'Book Chapter']);
	var formVM = {};

	$('#uploadPublication').validate({
		rules: publicationRules(),
		messages: publicationMessages(),
		errorPlacement: function(error, element) {
			error.appendTo(element.parent());
		},
		onfocusout: false,
		errorElement: "p",
		errorClass: "text-danger"
	});

	init();

	return vm;

	function submitPublication(form) {
		if($('#uploadPublication').valid()) {
			vmToJson();
			console.log(publication);
			$.post("/api/insertions.py", publication)
			.success(function() {
				console.log("Success");
			}).fail(function () {
				console.log("Failed");
			});
		}
	}

	function init() {
		formVM.Title = ko.observable("");												// #
		formVM.BookTitle = ko.observable("");										// #
		formVM.JournalTitle = ko.observable("");								// #
		formVM.ConferenceTitle = ko.observable("");							// #
		formVM.Abstract = ko.observable("");										// #
		formVM.Authors = ko.observable("");											// # - Form to object.
		formVM.Category = ko.observable("");										// #
		formVM.Country = ko.observable("");											// #
		formVM.DocumentTitle = ko.observable("");								// #
		formVM.MotivationForAccreditation = ko.observable("");	//
		formVM.PeerReviewProcess = ko.observable("");						//
		formVM.Volume = ko.observable("");											// #
		formVM.Issue = ko.observable("");												// #
		formVM.Publisher = ko.observable("");										// #
		formVM.Year = ko.observable("");												// #
		formVM.ISSN = ko.observable("");												// #
		formVM.ISBN = ko.observable("");												// #
		vm.formVM = formVM;
	}

	function publicationRules() {
		return {
			publicationTitle: {
				required: true
			},
			publicationAbstract: {
				required: true
			},
			publicationAuthors: {
				required: true
			},
			publicationCategory: {
				required: true
			},
			publicationJournalTitle: {
				required: true
			},
			publicationBookTitle: {
				required: true
			},
			publicationConferenceTitle: {
				required: true
			},
			publicationISSN: {
				required: true
			},
			publicationISBN: {
				required: true
			},
			publicationPublisher: {
				required: true
			},
			publicationYear: {
				required: true
			},
			publicationCountry: {
				required: true
			},
			publicationPeerReview: {
				required: true
			},
			publicationMotivation: {
				required: true
			}
		};
	}

	function publicationMessages() {
		return {
			publicationTitle: "Please enter a valid Title.",
			publicationAbstract: "Please enter a valid Abstract.",
			publicationAuthors: "Please enter a valid Author(s).",
			publicationCategory: "Please enter a valid Category.",
			publicationJournalTitle: "Please enter a valid Journal Title.",
			publicationConferenceTitle: "Please enter a valid Conference Title.",
			publicationBookTitle: "Please enter a valid Book Title.",
			publicationISSN: "Please enter a valid ISSN.",
			publicationISBN: "Please enter a valid ISBN.",
			publicationPublisher: "Please enter a valid Publisher.",
			publicationYear: "Please enter a valid Year.",
			publicationCountry: "Please enter a valid Country.",
			publicationPeerReview: "Please enter the peer review process for this Conference."
		};
	}

	function vmToJson() {
		for (var id in formVM) {
			if(formVM[id]()) {
				if(id === 'Authors') {
					publication[id] = [{Initials: 'SR', FirstName: 'Sarah', Surname: 'Chen'}];
				} else {
					publication[id] = formVM[id]();
				}
			} else {
				delete publication[id];
			}
		}
	}

});
