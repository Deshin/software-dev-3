define(["jquery", "knockout"], function($, ko) {
	var vm = this;

  vm.submitPublication = submitPublication;
  var publication = {};
  vm.categoryList = ko.observableArray(['Journal Article', 'Conference Paper', 'Other']);

  init();
	console.log("VM loaded - publicationUpload");
	return vm;

  function submitPublication() {
    console.log("Submit the form");
    vmToJson();
    console.log(publication);
  }

  function init() {
    vm.Title = ko.observable("");
    vm.Abstract = ko.observable("");
    vm.Authors = ko.observable("");
    vm.Category = ko.observable("");
    vm.ConferenceTitle = ko.observable("");
    vm.Country = ko.observable("");
    vm.DocumentTitle = ko.observable("");
    vm.MotivationForAccreditation = ko.observable("");
    vm.PeerReviewProcess = ko.observable("");
    vm.Publisher = ko.observable("");
    vm.Year = ko.observable("");
  }

  function vmToJson() {
    publication.Title = vm.Title();
    publication.Abstract = vm.Abstract();
    publication.Authors = vm.Authors();
    publication.Category = vm.Category();
    publication.ConferenceTitle = vm.ConferenceTitle();
    publication.Country = vm.Country();
    publication.DocumentTitle = vm.DocumentTitle();
    publication.MotivationForAccreditation = vm.MotivationForAccreditation();
    publication.PeerReviewProcess = vm.PeerReviewProcess();
    publication.Publisher = vm.Publisher();
    publication.Year = vm.Year();
  }

});
