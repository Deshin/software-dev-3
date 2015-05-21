/**
*
* @author Deshin
* @author Anthony
*/
define(["jquery", "jqueryvalidate", "knockout", "kofilebind", "bootbox"], function($, $valid, ko, kofilebind, bootbox) {
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
			$('#submitPublication').html('Submitting');
			$.ajax({
				url: "/api/insertions.py",
				type: "POST",
				contentType: "application/json",
				data: JSON.stringify(uploadPublication),

				success: function(data) {
					$('#submitPublication').html('Success!');
					clearForm();
					setTimeout(function() {
						$('#submitPublication').html('Submit');
						window.location.href = "/#!/";
					}, 2000);
				},

				error: function (jqXHR) {
					$('#submitPublication').html('Error (' + jqXHR.status + ')');
					if($('#submitPublication').hasClass('btn-primary')) {
						$('#submitPublication').removeClass('btn-primary');
						$('#submitPublication').addClass('btn-danger');
					}
					bootbox.dialog({
						message: "Error (" + jqXHR.status + ") " + jqXHR.statusText,
						title: "Error Uploading",
						buttons: {
							'OK': {
								className: "btn-success"
							}
						}});
						setTimeout(function() {
							$('#submitPublication').html('Submit');
							if($('#submitPublication').hasClass('btn-danger')) {
								$('#submitPublication').removeClass('btn-danger');
								$('#submitPublication').addClass('btn-primary');
							}
						}, 2000);
					},
				});
			} else if(!vm.AuthorString()) {
				$('#publicationAuthorsInitials').after('<p class="text-danger">Please enter a valid Author</p>');
			}
		}

		function init() {
			var formVM = {};
			formVM.Title = {
				sanatize: false,
				value: ko.observable("")
			};
			formVM.CategoryTitle = {
				sanatize: false,
				value: ko.observable("")
			};
			formVM.Abstract = {
				sanatize: false,
				value: ko.observable("")
			};
			formVM.Category = {
				sanatize: false,
				value: ko.observable("")
			};
			formVM.Country = {
				sanatize: false,
				value: ko.observable("")
			};
			formVM.MotivationForAccreditation = {
				sanatize: false,
				value: ko.observable("")
			};
			formVM.PeerReviewProcess = {
				sanatize: false,
				value: ko.observable("")
			};
			formVM.Volume = {
				sanatize: true,
				value: ko.observable("")
			};
			formVM.Issue = {
				sanatize: true,
				value: ko.observable("")
			};
			formVM.Publisher = {
				sanatize: false,
				value: ko.observable("")
			};
			formVM.Year = {
				sanatize: true,
				value: ko.observable("")
			};
			formVM.ISSN = {
				sanatize: true,
				value: ko.observable("")
			};
			formVM.ISBN = {
				sanatize: true,
				value: ko.observable("")
			};
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
			var initial = vm.AuthorInitials().replace(/[\.,-\/#!$%\^&\*;:{}=\-_`~()]/g,"").replace(/ /g, "");
			var firstname = vm.AuthorFirstName().replace(/[\.,-\/#!$%\^&\*;:{}=\-_`~()]/g,"").replace(/ /g, "");
			var surname = vm.AuthorSurname().replace(/[\.,-\/#!$%\^&\*;:{}=\-_`~()]/g,"").replace(/ /g, "");
			if(vm.AuthorInitials() && vm.AuthorSurname() && vm.AuthorFirstName()) {
				Authors.push({
					Initials: initial,
					Surname: surname,
					FirstName: firstname
				});
				var authorString = firstname + " " + surname + ", " + initial;
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
			vm.AuthorFirstName("");
			vm.AuthorSurname("");
			vm.AuthorInitials("");
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
				if(vm.formVM.hasOwnProperty(id)){
					if(vm.formVM[id].value()) {
						if(id === 'CategoryTitle') {
							if(vm.formVM.Category.value() === 'Journal Article') {
								publication.JournalTitle = vm.formVM[id].value();
							} else if (vm.formVM.Category.value() === 'Conference Paper') {
								publication.ConferenceTitle = vm.formVM[id].value();
							} else if (vm.formVM.Category.value() === 'Book Chapter') {
								publication.BookTitle = vm.formVM[id].value();
							}
						} else {
							if(vm.formVM[id].sanatize) {
								publication[id] = vm.formVM[id].value().replace(/[\.,-\/#!$%\^&\*;:{}=\-_`~()]/g,"").replace(/ /g, "");
							} else {
								publication[id] = vm.formVM[id].value();
							}
						}
					} else {
						delete publication[id];
					}
				}
			}

			for (var fileId in vm.fileVM) {
				if(vm.fileVM.hasOwnProperty(fileId)) {
					publication[fileId] = {
						data: "",
						file: {}
					};
					publication[fileId].data = vm.fileVM[fileId]().base64String();
					publication[fileId].file = vm.fileVM[fileId]().file();
				}
			}

			publication.SupportingDocumentation = SupportingDocs;
			publication.Authors = Authors;
			return publication;
		}

		function clearForm() {
			for (var id in vm.formVM) {
				if(vm.formVM[id].value()) {
					vm.formVM[id].value("");
				}
			}

			clearAuthors();
			clearSupportingDoc();

			fileVM.PublicationFile({
				base64String: ko.observable()
			});
			fileVM.PublicationToc({
				base64String: ko.observable()
			});
		}
	});
