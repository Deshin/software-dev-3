define(["jquery", "knockout"], function($, ko) {
	var vm = this;

	vm.permission = ko.observable(rootViewModel.loginState());

  vm.findAccount = findAccount;
  vm.removeAccount = removeAccount;

  vm.sortBy=ko.observable(null);
	vm.sort=ko.observable(null);
	vm.pageSize = ko.observable(null);
  vm.page = ko.observable(null);

  vm.username = ko.observable('');
	vm.firstname = ko.observable('');
	vm.surname = ko.observable('');
	vm.initials = ko.observable('');
  vm.userPublications = ko.observableArray([]);

  $('#searchAccount').validate({
    rules: publicationRules(),
    messages: publicationMessages(),
    errorPlacement: function(error, element) {
      error.appendTo(element.parent());
    },
    onfocusout: false,
    errorElement: "p",
    errorClass: "text-danger"
  });

  vm.skip = ko.computed(function() {
    return (vm.page()-1)*vm.pageSize();
  });

  vm.gotData = function(data) {
    vm.userPublications.removeAll();
		if(data !== '200') {
			for (var i = 0; i < data.length; i++) {
	      var authors = "";
	      for (var j = 0; j < data[i].Authors.length; j++) {
	        authors += data[i].Authors[j].Initials + " " + data[i].Authors[j].Surname;
	        if(j != data[i].Authors.length - 1) {
	          authors += ", ";
	        }
	      }
	      data[i].Authors = authors;
	      vm.userPublications.push(data[i]);
	    }
		}
  };

  vm.updateList = function(newVal) {
    if (vm.page() === null || vm.pageSize() === null || vm.sort() === null || vm.sortBy() === null) {
      return;
    }
    var getUrl = '/api/publications.py';
		var advSearch = [
			{
				field: 'First Name',
				value: vm.firstname(),
				operator: 'equals'
			},
			{
				field: 'Surname',
				value: vm.surname(),
				operator: 'equals'
			},
			{
				field: 'Initials',
				value: vm.initials(),
				operator: 'equals'
			},
		];
    var query = {
      skip: vm.skip().toString(),
      length: vm.pageSize().toString(),
      sortBy: vm.sortBy(),
      sort: vm.sort(),
			advancedSearch: JSON.stringify(advSearch)
    };
    $.getJSON(getUrl, query)
    .done(vm.gotData)
    .fail(function(jqXHR) {
      console.log("Error (" + jqXHR.status + ") " + jqXHR.statusText);
    });
  };

  vm.next = function() {
    vm.page(vm.page()+1);
  };

  vm.previous = function() {
    vm.page(vm.page()-1);
  };

  vm.first = function() {
    vm.page(1);
  };

  vm.sorting = function(item){
    if (vm.sortBy() === item) {
      if (vm.sort() === "ASC") {
        vm.sort("DESC");
      } else{
        vm.sort("ASC");
      }
    } else{
      vm.sortBy(item);
      vm.sort("ASC");
    }
  };

  vm.sortIcon = ko.computed(function() {
    if (vm.sort() === "ASC") {
      return "glyphicon glyphicon-triangle-top";
    } else{
      return "glyphicon glyphicon-triangle-bottom";
    }
  });

	if(vm.permission() !== 'admin') {
		vm.username(rootViewModel.username());

		sendAccountRequest();
	}

	return vm;

  function findAccount() {
    if($('#searchAccount').valid()) {
			sendAccountRequest();
    }
  }

	function sendAccountRequest() {
		vm.userPublications.removeAll();

		vm.firstname('');
		vm.surname('');
		vm.initials('');

		vm.page(1);
		vm.pageSize(20);
		vm.sort('ASC');
		vm.sortBy('Title');

		vm.page.subscribe(updateList);
		vm.pageSize.subscribe(updateList);
		vm.sortBy.subscribe(updateList);
		vm.sort.subscribe(updateList);

		$.getJSON('/api/authorDocs.py', {username: vm.username()})
			.done(function(data) {
				vm.firstname(data.firstname);
				vm.surname(data.surname);
				vm.initials(data.initials);

				updateList();
			})
			.fail(function(jqXHR) {
				console.log("Error (" + jqXHR.status + ") " + jqXHR.statusText);
			});
	}

  function removeAccount() {
		$.post('/api/deleteAccount.py', {username: vm.username})
			.done(function(data) {
				vm.username('');
				vm.firstname('');
				vm.surname('');
				vm.initials('');

				vm.userPublications.removeAll();
			})
			.fail(function(jqXHR) {
				console.log("Error (" + jqXHR.status + ") " + jqXHR.statusText);
			});
  }

  function publicationRules() {
    return {
      username: {
        required: true
      },
    };
  }

  function publicationMessages() {
    return {
      username: {
        required: "Please enter a valid Username."
      },
    };
  }

});
