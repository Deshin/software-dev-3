define(["jquery", "knockout"], function($, ko) {
	var vm = this;

  var publication = {};

  vm.Title = ko.observable(publication.Title);
  vm.Abstract = ko.observable(publication.Abstract);
  vm.Authors = ko.observable(publication.Authors);
  vm.Category = ko.observable(publication.Category);
  vm.ConferenceTitle = ko.observable(publication.ConferenceTitle);
  vm.Country = ko.observable(publication.Country);
  vm.DocumentTitle = ko.observable(publication.DocumentTitle);
  vm.MotivationForAccreditation = ko.observable(publication.MotivationForAccreditation);
  vm.PeerReviewProcess = ko.observable(publication.PeerReviewProcess);
  vm.Publisher = ko.observable(publication.Publisher);
  vm.Year = ko.observable(publication.Year);

	return vm;

  function submitPublication() {

  }

});
