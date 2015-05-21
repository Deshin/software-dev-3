define(["jquery", "knockout"], function($, ko) {
	var vm = this;

	vm.permission = ko.observable(rootViewModel.loginState());

  vm.findAccount = findAccount;
  vm.removeAccount = removeAccount;

  vm.accountSortBy=ko.observable(null);
	vm.accountSort=ko.observable(null);
	vm.accountPageSize = ko.observable(null);
  vm.accountPage = ko.observable(null);

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

  vm.accountSkip = ko.computed(function() {
    return (vm.accountPage()-1)*vm.accountPageSize();
  });

  vm.accountGotData = function(data) {
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

  vm.accountUpdateList = function(newVal) {
    if (vm.accountPage() === null || vm.accountPageSize() === null || vm.accountSort() === null || vm.accountSortBy() === null) {
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
      skip: vm.accountSkip().toString(),
      length: vm.accountPageSize().toString(),
      sortBy: vm.accountSortBy(),
      sort: vm.accountSort(),
			advancedSearch: JSON.stringify(advSearch)
    };
    $.getJSON(getUrl, query)
    .done(vm.accountGotData)
    .fail(function(jqXHR) {
      console.log("Error (" + jqXHR.status + ") " + jqXHR.statusText);
    });
  };

  vm.accountNext = function() {
    vm.accountPage(vm.accountPage()+1);
  };

  vm.accountPrevious = function() {
    vm.accountPage(vm.accountPage()-1);
  };

  vm.accountFirst = function() {
    vm.accountPage(1);
  };

  vm.accountSorting = function(item){
    if (vm.accountSortBy() === item) {
      if (vm.accountSort() === "ASC") {
        vm.accountSort("DESC");
      } else{
        vm.accountSort("ASC");
      }
    } else{
      vm.accountSortBy(item);
      vm.accountSort("ASC");
    }
  };

  vm.accountSortIcon = ko.computed(function() {
    if (vm.accountSort() === "ASC") {
      return "glyphicon glyphicon-triangle-top";
    } else{
      return "glyphicon glyphicon-triangle-bottom";
    }
  });

	if(vm.permission() !== 'admin') {
		vm.username(rootViewModel.loginUsername());

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

		vm.accountPage(1);
		vm.accountPageSize(20);
		vm.accountSort('ASC');
		vm.accountSortBy('Title');

		vm.accountPage.subscribe(vm.accountUpdateList);
		vm.accountPageSize.subscribe(vm.accountUpdateList);
		vm.accountSortBy.subscribe(vm.accountUpdateList);
		vm.accountSort.subscribe(vm.accountUpdateList);

		$.getJSON('/api/authorDocs.py', {username: vm.username()})
			.done(function(data) {
				vm.firstname(data.firstname);
				vm.surname(data.surname);
				vm.initials(data.initials);

				vm.accountUpdateList();
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
