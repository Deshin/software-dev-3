define(["jquery", "knockout", "crypto.SHA", "bootbox"], function($, ko, crypto, bootbox) {
	var vm = this;

	vm.createAccount = createAccount;

	$('#createAccount').validate({
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

	function init() {
		var form = {};

		form.firstname = ko.observable("");
		form.surname = ko.observable("");
		form.initials = ko.observable("");
		form.username = ko.observable("");

		vm.password  = ko.observable("");
		vm.retypePassword = ko.observable("");

		vm.password.subscribe(function(newVal) {
			if(vm.password() === vm.retypePassword()) {
				$('#retypePassword').next().remove();
			}
		});
		vm.retypePassword.subscribe(function(newVal) {
			if(vm.password() === vm.retypePassword()) {
				$('#retypePassword').next().remove();
			}
		});

		vm.form = form;

	}

	function createAccount() {
		if(vm.password() === vm.retypePassword() && $('#createAccount').valid()) {
			$('#submitAccount').html('Submitting..');
			var submitForm = ko.toJS(vm.form);
			submitForm.password = CryptoJS.SHA256(vm.password()).toString();
			$.post('/api/createAccount.py', submitForm)
			.done(function(data) {
				// Program redirect.
				form.firstname("");
				form.surname("");
				form.initials("");
				form.username("");
				vm.password("");
				vm.retypePassword("");

				$('#submitAccount').html('Success!');
				setTimeout(function() {
					$('#submitAccount').html('Submit');
					window.location.href = "/#!/";
				}, 2000);
			})
			.error(function (jqXHR) {
				$('#submitAccount').html('Submit');
				bootbox.dialog({
					message: "Error (" + jqXHR.status + ") " + jqXHR.statusText,
					title: "Error",
					show: true,
					backdrop: true,
					closeButton: true,
					animate: true,
					className: "my-modal",
					buttons: {
						'Ok': {
							className: "btn-primary",
						},
					}
				});
			});
		} else if(vm.password() !== vm.retypePassword()) {
			$('#retypePassword').after('<p class="text-danger">Both passwords must match</p>');
		}
	}

	function publicationRules() {
		return {
			username: {
				required: true
			},
			password: {
				required: true
			},
			retypePassword: {
				required: true
			},
			initials: {
				required: true
			},
			clientName: {
				required: true
			},
			surname: {
				required: true
			},
		};
	}

	function publicationMessages() {
		return {
			username: {
				required: "Please enter a valid Username."
			},
			password: {
				required: "Please enter a valid Password."
			},
			retypePassword: {
				required: "Please enter a valid Password."
			},
			initials: {
				required: "Please enter valid Intials."
			},
			clientName: {
				required: "Please enter a valid Name."
			},
			surname: {
				required: "Please enter a valid Surname."
			},
		};
	}

});
