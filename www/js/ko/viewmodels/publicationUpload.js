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
			$.ajax({
				url: "/api/insertions.py",
				type: "POST",
				contentType: "application/json",
				data: JSON.stringify(publication),

				success: function(data) {
					console.log("Success");
				},

				error: function (jqXHR) {
					console.log("Error: " + jqXHR.status + " - " + jqXHR.statusText);
				},
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
		formVM.ISSN = ko.observable("");													// #
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
				required: true,
				number: true
			},
			publicationISBN: {
				required: true,
				number: true
			},
			publicationPublisher: {
				required: true
			},
			publicationYear: {
				required: true,
				number: true,
				minlength: 4,
				min: 1000
			},
			publicationCountry: {
				required: true
			},
			publicationPeerReview: {
				required: true
			},
			publicationMotivation: {
				required: true
			},
			publicationIssue: {
				number: true
			},
			publicationVolume: {
				number: true
			}
		};
	}

	function publicationMessages() {
		return {
			publicationTitle: {
				required: "Please enter a valid Title."
			},
			publicationAbstract: {
				required: "Please enter a valid Abstract."
			},
			publicationAuthors: {
				required: "Please enter a valid Author(s)."
			},
			publicationCategory: {
				required: "Please enter a valid Category."
			},
			publicationJournalTitle: {
				required: "Please enter a valid Journal Title."
			},
			publicationConferenceTitle: {
				required: "Please enter a valid Conference Title."
			},
			publicationBookTitle: {
				required: "Please enter a valid Book Title."
			},
			publicationISSN: {
				required: "Please enter a valid ISSN.",
				number: "The ISSN must be a number."
			},
			publicationISBN:{
				required:  "Please enter a valid ISBN.",
				number: "The ISBN must be a number."
			},
			publicationPublisher: {
				required: "Please enter a valid Publisher."
			},
			publicationYear: {
				required: "Please enter a valid Year.",
				number: "The Year must be a number."
			},
			publicationCountry: {
				required: "Please enter a valid Country."
			},
			publicationPeerReview: {
				required: "Please enter the peer review process for this Conference."
			},
			publicationVolume: {
				number: "The Volume must be a number."
			},
			publicationIssue: {
				number: "The Issue must be a number."
			}
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
