define(["jquery", "knockout"], function($, ko) {
	var vm = this;
	vm.formats = ko.observableArray(['']);
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
			$.ajax({
				url: "/api/updateAccredited.py",
				type: "POST",
				contentType: "application/json",
				data: JSON.stringify(uploadListings),

				success: function(data) {
					console.log('Success');
				},

				error: function (jqXHR) {
					console.log("Error (" + jqXHR.status + ") " + jqXHR.statusText);
				},
			});
		}
	};
	return vm;

	function checkFiles() {
		var checkListings = true;
		for(var id = 0; id < vm.listings().length; id++) {
			if(!vm.listings()[id].fileData().base64String()) {
				checkListings = false;
			}
		}
		return checkListings;
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
