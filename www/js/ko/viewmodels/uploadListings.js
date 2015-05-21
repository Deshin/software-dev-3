/**
*
* @author Deshin
* @author Anthony
*/

define(["jquery", "knockout", "bootbox"], function($, ko, bootbox) {
	var vm = this;
	vm.formats = ko.observableArray(['']);
	vm.errorMessage = ko.observable('');
	$.getJSON("/api/CSVFormats.py", function(data) {
		vm.formats(data);
	});
	vm.types = ko.observableArray(['Accredited', 'Predatory', 'H-Index']);
	vm.defaultListing = function() {
		return 	{
			format: ko.observable(vm.formats()[0]),
			type: ko.observable("Accredited"),
			fileData: ko.observable({
				base64String: ko.observable()
			})
		};
	};
	vm.listings = ko.observableArray([vm.defaultListing()]);
	vm.addListing = function() {
		vm.listings.unshift(vm.defaultListing());
	};
	vm.removeListing = function(index) {
		vm.listings.splice(index(), 1);
	};
	vm.upload = function() {
		if(checkFiles()) {
			var uploadListings = toJson();
			$('#submitListings').html('Submitting');
			$.ajax({
				url: "/api/updateAccredited.py",
				type: "POST",
				contentType: "application/json",
				data: JSON.stringify(uploadListings),

				success: function(data) {
					$('#submitListings').html('Success!');

					vm.listings.removeAll();
					vm.addListing();

					setTimeout(function() {
						$('#submitListings').html('Submit');
						window.location.href = "/#!/";
					}, 2000);
				},

				error: function (jqXHR) {
					console.log("Error (" + jqXHR.status + ") " + jqXHR.statusText);
					$('#submitListings').html('Submit');

					bootbox.dialog({
						message: "Error (" + jqXHR.status + ") " + jqXHR.statusText,
						title: "Error Uploading",
						buttons: {
							'OK': {
								className: "btn-success"
							}
						}});
				},
			});
		}
	};
	return vm;

	function checkFiles() {
		for(var id = 0; id < vm.listings().length; id++) {
			if(!vm.listings()[id].fileData().base64String()) {
				vm.errorMessage('Please upload files in ALL added fields.');
				return false;
			}
		}
		vm.errorMessage('');
		return true;
	}

	function toJson() {
		var subJson = [];
		for(var id = 0; id < vm.listings().length; id++) {
			subJson.push({
				type: vm.listings()[id].type(),
				format: vm.listings()[id].format(),
				data: vm.listings()[id].fileData().base64String()
			});
		}
		return subJson;
	}
});
