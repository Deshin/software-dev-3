/**
* Upload listing view model will load with the upload listing partial.
* this page is used for uploading new .csv files to update the
* accredited information within the database.
*
* @requires jQuery
* @requires knockout.js
* @requires bootbox
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
	/**
	* @method defaultListing
	* The default listing method will create the default object that is pushed
	* onto the array of objects, when one is added another input window is displayed
	* on the page.
	*/
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
	/**
	* @method addListing
	* Add a listing to the view (and the view model)
	*/
	vm.addListing = function() {
		vm.listings.unshift(vm.defaultListing());
	};
	/**
	* @method removeListing
	* Remove a listing from the list, also removes the object within the vm.
	*/
	vm.removeListing = function(index) {
		vm.listings.splice(index(), 1);
	};
	/**
	* @method upload
	* The upload method converts the view model objects to the objects expected
	* by the end point. Displays messages upon success and will redirect. If the
	* page failes a notification with the reason is shown.
	*/
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

	/**
	* @method checkFiles
	* Check that the files are valid for every object in the array
	* where upload file is an option.
	*/
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

	/**
	* @method toJson
	* Convert the view model to JSON expected by the server.
	*/
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
