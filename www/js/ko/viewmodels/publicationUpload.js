define(["jquery", "jqueryvalidate", "knockout", "kofilebind"], function($, $valid, ko, kofilebind) {
	var vm = this;

	vm.submitPublication = submitPublication;
	vm.categoryList = ko.observableArray(['', 'Journal Article', 'Conference Paper', 'Book Chapter']);
	vm.clearSupportingDoc = clearSupportingDoc;
	var SupportingDocs = [];
	vm.addAuthor = addAuthor;
	vm.clearAuthors = clearAuthors;
	var Authors = [];

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
		if($('#uploadPublication').valid() && vm.AuthorString()) {
			var uploadPublication = vmToJson();
			console.log(uploadPublication);
			$.ajax({
				url: "/api/insertions.py",
				type: "POST",
				contentType: "application/json",
				data: JSON.stringify(uploadPublication),

				success: function(data) {
					console.log("Success");
				},

				error: function (jqXHR) {
					console.log("Error: " + jqXHR.status + " - " + jqXHR.statusText);
				},
			});
		} else if(!vm.AuthorString()) {
			$('#publicationAuthorsInitials').after('<p class="text-danger">Please enter a valid Author</p>');
		}
	}

	function init() {
		var formVM = {};
		formVM.Title = ko.observable("");
		formVM.CategoryTitle = ko.observable("");
		formVM.Abstract = ko.observable("");
		formVM.Category = ko.observable("");
		formVM.Country = ko.observable("");
		formVM.DocumentTitle = ko.observable("");
		formVM.MotivationForAccreditation = ko.observable("");
		formVM.PeerReviewProcess = ko.observable("");
		formVM.Volume = ko.observable("");
		formVM.Issue = ko.observable("");
		formVM.Publisher = ko.observable("");
		formVM.Year = ko.observable("");
		formVM.ISSN = ko.observable("");
		formVM.ISBN = ko.observable("");
		vm.formVM = formVM;

		vm.AuthorInitials = ko.observable("");
		vm.AuthorFirstName = ko.observable("");
		vm.AuthorSurname = ko.observable("");

		vm.AuthorString = ko.observable("");

		var fileVM = {};
		fileVM.PublicationFile = ko.observable({
			base64String: ko.observable()
		});
		fileVM.PublicationToc = ko.observable({
			base64String: ko.observable()
		});

		vm.SupportingDocumentation = ko.observable({
			base64String: ko.observable()
		});

		vm.SupportingDocumentationFiles = ko.observable("");
		vm.SupportingDocumentation().base64String.subscribe(function(newVal) {
			if(vm.SupportingDocumentationFiles()) {
				vm.SupportingDocumentationFiles(vm.SupportingDocumentationFiles() + ", " + vm.SupportingDocumentation().file().name);
			} else {
				vm.SupportingDocumentationFiles(vm.SupportingDocumentation().file().name);
			}
			SupportingDocs.push({
				data: vm.SupportingDocumentation().base64String(),
				file: vm.SupportingDocumentation().file()
			});
		});

		vm.fileVM = fileVM;
	}

	function clearSupportingDoc() {
		vm.SupportingDocumentationFiles("");
		SupportingDocs = [];
	}

	function addAuthor() {
		if(vm.AuthorInitials() && vm.AuthorSurname() && vm.AuthorFirstName()) {
			Authors.push({
				Initials: vm.AuthorInitials(),
				Surname: vm.AuthorSurname(),
				FirstName: vm.AuthorFirstName()
			});
			var authorString = vm.AuthorFirstName() + " " + vm.AuthorSurname() + ", " + vm.AuthorInitials();
			if(vm.AuthorString()) {
				vm.AuthorString(vm.AuthorString() + "; " + authorString);
			} else {
				vm.AuthorString(authorString);
			}
			vm.AuthorFirstName("");
			vm.AuthorSurname("");
			vm.AuthorInitials("");

			$('#publicationAuthorsInitials').next().remove();
		}
	}

	function clearAuthors() {
		Authors = [];
		vm.AuthorString("");
	}

	function publicationRules() {
		return {
			publicationTitle: {
				required: true
			},
			publicationAbstract: {
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
			},
			publicationFile: {
				required: true
			},
			publicationToc: {
				required: true
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
			},
			publicationFile: {
				required: "Please upload a publication file."
			},
			publicationToc: {
				required: "Please upload a table of contents file."
			}
		};
	}

	function vmToJson() {
		var publication = {};
		for (var id in vm.formVM) {
			if(vm.formVM[id]()) {
				if(id === 'CategoryTitle') {
					if(vm.formVM.Category() === 'Journal Article') {
						publication.JournalTitle = vm.formVM[id]();
					} else if (vm.formVM.Category() === 'Conference Paper') {
						publication.ConferenceTitle = vm.formVM[id]();
					} else if (vm.formVM.Category() === 'Book Chapter') {
						publication.BookTitle = vm.formVM[id]();
					}
				} else {
					publication[id] = vm.formVM[id]();
				}
			} else {
				delete publication[id];
			}
		}

		for (var fileId in vm.fileVM) {
			publication[fileId] = {
				data: "",
				file: {}
			};
			publication[fileId].data = vm.fileVM[fileId]().base64String();
			publication[fileId].file = vm.fileVM[fileId]().file();
		}

		publication.SupportingDocumentation = SupportingDocs;
		publication.Authors = Authors;

		return publication;
	}

});
