define(["jquery", "knockout"], function($, ko) {
	var vm = this;

  vm.findAccount = findAccount;
  vm.removeAccount = removeAccount;
  vm.username = ko.observable("");
  vm.sortBy=ko.observable(null);
	vm.sort=ko.observable(null);

  vm.userDetails = ko.observable({});
  vm.publications = ko.observableArray([]);

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

  vm.pageSize = ko.observable(null);
  vm.page = ko.observable(null);
  vm.sortBy=ko.observable(null);
  vm.sort=ko.observable(null);

  vm.skip = ko.computed(function() {
    return (vm.page()-1)*vm.pageSize();
  });

  vm.gotData = function(data) {
    vm.publications.removeAll();
    vm.userDetails(data.userDetails);
    console.log(data);
    for (var i = 0; i < data.documentDetails.length; i++) {
      var authors = "";
      for (var j = 0; j < data.documentDetails[i].Authors.length; j++) {
        authors += data.documentDetails[i].Authors[j].Initials + " " + data.documentDetails[i].Authors[j].Surname;
        if(j != data.documentDetails[i].Authors.length - 1) {
          authors += ", ";
        }
      }
      data.documentDetails[i].Authors = authors;
      vm.publications.push(data.documentDetails[i]);
    }
  };

  vm.updateList = function(newVal) {
    if (vm.page() === null || vm.pageSize() === null || vm.sort() === null || vm.sortBy() === null) {
      return;
    }
    var getUrl = '/api/authorDocs.py';
    var query = {
      username: vm.username,
      skip: vm.skip().toString(),
      length: vm.pageSize().toString(),
      sortBy: vm.sortBy(),
      sort: vm.sort()
    };
    $.getJSON(getUrl, query)
    .done(vm.gotData)
    .fail(function(jqXHR) {
      console.log("Error (" + jqXHR.status + ") " + jqXHR.statusText);
    });
  };

  vm.publications = ko.observableArray([]);

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

	return vm;

  function findAccount() {
    if($('#searchAccount').valid()) {
      vm.page(1);
      vm.pageSize(20);
      vm.sort('ASC');
      vm.sortBy('Title');

      vm.page.subscribe(updateList, vm, 'change');
      vm.pageSize.subscribe(updateList, vm, 'change');
      vm.sortBy.subscribe(updateList, vm, 'change');
      vm.sort.subscribe(updateList, vm, 'change');

      updateList();
    }
  }

  function removeAccount() {

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
