/**
* The view account view model and partial is used for displaying account
* information and submitted publications of a particular user,
* if the user is a registered user it is their credentials shown.
* If an admin navigates to the page they can fetch any user's information
* and delete a user if necessary.
*
* @requires jQuery
* @requires knockout.js
*
* @author Deshin
* @author Anthony
*/

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

	/**
	* Configure the jquery validation for the search box, with custom
	* rules and messages defined.
	* @requires jQuery.validate
	*/
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

	/**
	* @method accountSkip
	* The account skip function is used for calculating the skip amount
	* when querying the endpoint.
	*/
  vm.accountSkip = ko.computed(function() {
    return (vm.accountPage()-1)*vm.accountPageSize();
  });

	/**
	* @callback accountGotData
	* Once the data has been fetched this callback is
	* called, it converts data from the server into observables
	* on th vm.
	*/
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

	/**
	* @callback accountUpdateList
	* The update list function is called if any of the observed query options
	* are called, it will build a query string and pass it to the get function.
	* On successful get the date is shown.
	*/
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

	/**
	* @method accountNext
	* Get the next page for pagination.
	*/
  vm.accountNext = function() {
    vm.accountPage(vm.accountPage()+1);
  };

	/**
	* @method accountPrevious
	* Get the previous page for pagination.
	*/
  vm.accountPrevious = function() {
    vm.accountPage(vm.accountPage()-1);
  };

	/**
	* @method accountFirst
	* Get the first page for pagination.
	*/
  vm.accountFirst = function() {
    vm.accountPage(1);
  };

	/**
	* @method accountSorting
	* The sorting method which is called when the table columns are
	* reorganized, causes a callback that will get data from the
	* database using the query string.
	*/
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

	/**
	* @method accountSortIcon
	* Determines the icon that is shown on the table depending on whether
	* the fields are sorted by ascending or descending.
	*/
  vm.accountSortIcon = ko.computed(function() {
    if (vm.accountSort() === "ASC") {
      return "glyphicon glyphicon-triangle-top";
    } else{
      return "glyphicon glyphicon-triangle-bottom";
    }
  });

	/**
	* If the permission level of the user is not admin then just get
	* the account of the current user.
	*/
	if(vm.permission() !== 'admin') {
		vm.username(rootViewModel.loginUsername());

		sendAccountRequest();
	}

	return vm;

	/**
	* @method findAccount
	* Search for a particular account to display the information and
	* owned publications of.
	*/
  function findAccount() {
    if($('#searchAccount').valid()) {
			sendAccountRequest();
    }
  }

	/**
	* @method sendAccountRequest
	* Fetch the account data for a particular user.
	*/
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

	/**
	* @method
	* Remove the account of the user currently displayed, this function is
	* limited to admin.
	*/
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

	/**
	* @method publicationRules
	* Configure rules for search box validation.
	*/
  function publicationRules() {
    return {
      username: {
        required: true
      },
    };
  }

	/**
	* @method publicationMessages
	* Configure the messages for search box validation.
	*/
  function publicationMessages() {
    return {
      username: {
        required: "Please enter a valid Username."
      },
    };
  }

});
